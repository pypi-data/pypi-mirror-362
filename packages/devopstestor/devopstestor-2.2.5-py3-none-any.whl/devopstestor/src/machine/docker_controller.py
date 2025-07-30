import docker
import os
import shutil
import random
from core_utils import get_global_path
from abstract_machine_controller import AbstractMachineController
from abstract_source_accessor import AbstractSourceAccessor
from log_manager import logging
logger = logging.getLogger('machine.DockerController')
import tarfile
from config import Config
class DockerController(AbstractMachineController):
    """
    Initialise, creer et controle un conteneur docker
    """
    @staticmethod
    def pre_initialize(global_config, machine_configuration, source_manager):
        """
        permet de pre initialise la machine
        Construit l'image docker presente dans le dockerfile dockerfile_dir_path/Dockerfile
        """
        ## Chargement des presets des machines herites, il faut les build
        ## L'image cible peut avoir besoin des images herites
        for mc in machine_configuration.get('extends_presets'):
            DockerController._build_image(Config.create_from_dict(mc), global_config)

        ## Compilation de l'image cible
        DockerController._build_image(machine_configuration, global_config)

    @staticmethod
    def _build_image(machine_configuration, global_config):
        logger.debut('build', 'Debut build image')
        client = docker.from_env()
        dockerfile_path = get_global_path(
            global_config=global_config,
            in_path=machine_configuration.get('dockerfile_path')
        )
        context_path = os.path.dirname(dockerfile_path)
        filename = os.path.basename(dockerfile_path)
        image_name = machine_configuration.get('docker_run_args::image')
        tag = machine_configuration.get('docker_run_args::tag')
        logger.info('Build config', context_path=context_path, filename=filename, image_name=image_name, tag=tag)
        build_kwargs = {}
        if global_config.get('machine::proxy') is not False:
            # Activate proxy config in docker build
            proxy_url = global_config.get('machine::proxy')
            build_kwargs['use_config_proxy'] = True 
            if not 'buildargs' in build_kwargs:
                build_kwargs['buildargs'] = {}            
            build_kwargs['buildargs']['http_proxy'] = proxy_url
            build_kwargs['buildargs']['https_proxy'] = proxy_url
            build_kwargs['buildargs']['HTTP_PROXY'] = proxy_url
            build_kwargs['buildargs']['HTTPS_PROXY'] = proxy_url

        # if pull failure, build
        do_build=True
        try:
            logger.info('Trying to pull image ', repository=image_name, tag=tag)
            pullres = client.images.pull(
                repository=image_name,
                tag=tag
            )
            do_build=False
        except docker.errors.APIError as e:
            logger.info('pull failed', e=str(e))
        except docker.errors.NotFound as e:
            logger.info('pull failed NotFound', e=str(e))
        except Exception as e:
            logger.info('pull failed', e=str(e))
        except TypeError as e:
            logger.info('pull failed', e=str(e))

        if do_build:
            logger.info('Pull failed, trying to build docker image')
            (image, logs) = client.images.build(
                tag=image_name + ':' + tag,
                path=context_path,
                dockerfile=filename,
                rm=True,
                **build_kwargs
            )
            for entry in logs:
                logger.debug(entry.get('stream',str(entry)).rstrip())
            logger.fin('build', 'Build image finish')
        logger.debut('network')
        try:
            client.api.inspect_network("testauto")
        except docker.errors.NotFound as e:
            logger.info("Network not exist, create")
            client.api.create_network("testauto", driver="bridge")
        logger.fin('network')

    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.directories_to_clean = []

    def create_machine(self, global_config, machine_configuration, machine_name, source_manager):
        """
        Initialise et lance le conteneur Docker
        """
        self.container =  None
        client = docker.from_env(timeout=1000)
        config_docker = machine_configuration.get_node('docker_run_args').config
        config_docker['name'] = self.machine_name
        if not 'hostname' in config_docker:
            config_docker['hostname'] = self.machine_name.replace('testauto_','')
        if not 'volumes' in config_docker:
            config_docker['volumes'] = []
        binds_host_config = {}
        for name, accessor in list(source_manager.get_accessors().items()):          
            self.share_source_accessor(accessor=accessor, config_docker=config_docker, binds_host_config=binds_host_config)

        logger.debut("container_"+machine_name, "Creation d'un conteneur", container_name=machine_name, config_docker=config_docker, binds_host_config=binds_host_config)
        config_docker['host_config'] = client.api.create_host_config(binds=binds_host_config, **machine_configuration.config.get('host_config',{}))
        config_docker['environment'] = machine_configuration.config.get('run',{}).get('env', {})
        if global_config.get('machine::proxy') is not False:
            # Activate proxy config in docker build
            proxy_url = global_config.get('machine::proxy')     
            config_docker['environment']['http_proxy'] = proxy_url
            config_docker['environment']['https_proxy'] = proxy_url
            config_docker['environment']['HTTP_PROXY'] = proxy_url
            config_docker['environment']['HTTPS_PROXY'] = proxy_url
        # Low level api, tag is in image name
        config_docker['image'] += ':'+config_docker['tag']
        del config_docker['tag']
        container_id = client.api.create_container(**config_docker)
        client.api.connect_container_to_network(container=container_id, net_id="testauto")
        self.container = client.containers.get(machine_name)
        self.container.start()

    def share_source_accessor(self, accessor:AbstractSourceAccessor, config_docker, binds_host_config, **kwargs):
        """
        Permet de copier les donnes d'un accessor sur la machine (conteneur)
        :param accessor: accessor a monter         
        """
        # Create docker volume
        config_docker['volumes'].append(accessor.machine_path)
        binds_host_config[accessor.local_path] = {
            "bind" : accessor.machine_path,
            "mode" : 'rw' if accessor.readonly == False else 'ro'
        }


    def is_aldready_exists(self, machine_configuration, machine_name):
        """
        Retoure True si la machine est deja existante
        """
        try:
            client = docker.from_env(timeout=1000)
            client.containers.get(machine_name)
        except Exception as e:
            logger.warn('is_aldready_exists exception', exception=str(e))
            return False
        return True

    def resume_machine(self, global_config, machine_configuration, machine_name, source_manager):
        """
        Se connecte a une machine existante
        A surcharger si necessaire
        """
        self.container = docker.from_env(timeout=1000).containers.get(machine_name)

    def put_in_file(self, content, file_path, makedir=False):
        """
        Permet de copier du contenu dans un fichier sur la machine
        :param content: Contenu a copier
        :param file_path: nom du fichier
        :return: code retour
        """
        if makedir:
            self.run_cmd('mkdir -p {}'.format(os.path.dirname(file_path)))

        # Creation d'un fichier local
        localfiledir = os.path.join("/tmp/devopstestor/", file_path.replace('/', '_SLASH_') + str(random.randrange(999)))
        filename = os.path.basename(file_path)
        localfile_path =  os.path.join(localfiledir, filename)
        filedir_dest = os.path.dirname(file_path) + '/'

        # Memorisation du dossier temporaire pour nettoyage futur
        if not os.path.exists(localfiledir):
            self.directories_to_clean.append(localfiledir)
            ret = os.makedirs(localfiledir, exist_ok=True)

        # Creation / update reference local du fichier
        with open(localfile_path, "w+") as f:
            f.write(content)

        # Creation d'une archive local
        tar = tarfile.open(localfile_path + '.tar', mode='w')
        try:
            tar.add(name=localfile_path, arcname=filename)
        finally:
            tar.close()

        # Envoi vers conteneur
        data = open(localfile_path + '.tar', 'rb').read()
        self.container.put_archive(path=filedir_dest, data=data)

        return 0, ""

    def get_file_content(self, file_path):
        """
        Permet de recuperer le contenu d'un fichier sur la machine
        :param file_path: Chemin vers le fichier
        :return: contenu du fichier (string)
        """
        logger.debug('get_filecontent', file_path=file_path, machine_name=self.machine_name)

        return self.run_cmd('cat ' + file_path)

    def run_cmd(self, command, workdir=None):
        '''
        Lance une commande sur le conteneur.
        '''
        kwargs = {}
        if workdir is not None:
            kwargs['workdir'] = workdir

        logger.debut('commande', "Lancement d'une commande sur le conteneur", machine_name=self.machine_name, command=command)
        ret_code, output = self.container.exec_run(
            command,
            stream=False,
            **kwargs
        )
        logger.fin('commande', command=command, machine_name=self.machine_name, ret_code=ret_code)
        return ret_code, str(output, 'utf-8') #convert bytes to str

    def logs(self, **kwargs):
        '''
        Lance une commande sur le conteneur.
        '''
        return True, self.container.logs(**kwargs)

    def destroy_machine(self, global_config, machine_configuration, machine_name, source_manager):
        """
        Stop et supprime le conteneur
        """
        logger.fin("container_"+machine_name, "Fin de vie du conteneur", machine_name=machine_name)
        if self.container is not None:
            try:
                self.container.stop()
            except Exception as e:
                logger.error(f'Error when stopped container {machine_name}', e=str(e))
            try:
                self.container.remove()
            except Exception as e:
                logger.error(f'Error when removed container {machine_name}', e=str(e))
            del self.container

            for path in self.directories_to_clean:
                logger.debug('Nettoyage du chemin temporaire', path=path)
                shutil.rmtree(path)
