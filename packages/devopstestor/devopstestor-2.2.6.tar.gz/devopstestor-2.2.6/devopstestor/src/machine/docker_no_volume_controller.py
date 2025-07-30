import docker
from docker_controller import DockerController
from log_manager import logging
from abstract_source_accessor import AbstractSourceAccessor
import os, random
logger = logging.getLogger('machine.DockerNoVolumeController')
import tarfile, shutil

class DockerNoVolumeController(DockerController):        
    def create_machine(self, global_config, machine_configuration, machine_name, source_manager):
        """
        Initialise et lance le conteneur Docker
        """
        client = docker.from_env(timeout=1000)
        config_docker = machine_configuration.get_node('docker_run_args').config
        config_docker['name'] = self.machine_name
        if not 'hostname' in config_docker:
            config_docker['hostname'] = self.machine_name.replace('testauto_','')

        logger.debut("container_"+machine_name, "Creation d'un conteneur", container_name=machine_name, config_docker=config_docker)
        config_docker['host_config'] = client.api.create_host_config(**machine_configuration.config.get('host_config',{}))

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

        for name, accessor in list(source_manager.get_accessors().items()):          
            self.share_source_accessor(accessor=accessor)


    def share_source_accessor(self, accessor:AbstractSourceAccessor, **kwargs):
        """
        Permet de copier les donnes d'un accessor sur la machine (conteneur)
        :param accessor: accessor a monter 
        """
        self.run_cmd('mkdir -p ' + accessor.machine_path)
        # Verifi si la source exist
        if not os.path.exists(accessor.local_path):
            # Si la sourc n'existe pas un dossier vide sera juste cree
            return

        # Create an archive in temp dir
        local_archive_dirpath = os.path.join("/tmp/devopstestor/", accessor.local_path.replace('/', '_SLASH_') + str(random.randrange(999)))
        local_archive_path = os.path.join(local_archive_dirpath, 'archive.tar')        
        ret = os.makedirs(local_archive_dirpath, exist_ok=True)       

        logger.info('Create temp tar file ' + local_archive_path)
        tar = tarfile.open(local_archive_path, mode='w')
        try:
            tar.add(name=accessor.local_path, arcname=os.path.basename(accessor.machine_path))
        finally:
            tar.close()

        # Envoi vers conteneur        
        data = open(local_archive_path, 'rb').read()
        logger.info('Envoi des donnes du volume vers le conteneur ' + accessor.machine_path)
        
        # create parent path sur le conteneur
        self.container.put_archive(path=os.path.dirname(accessor.machine_path), data=data)

        # Cleanup
        shutil.rmtree(local_archive_dirpath)
        
    def resume_machine(self, global_config, machine_configuration, machine_name, source_manager):
        """
        Se connecte a une machine existante
        A surcharger si necessaire
        """
        super().resume_machine(global_config, machine_configuration, machine_name, source_manager)

        # Share accessor in case of resume machine
        for name, accessor in list(source_manager.get_accessors().items()):          
            self.share_source_accessor(accessor=accessor)