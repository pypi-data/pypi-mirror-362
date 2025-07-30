import subprocess
from source_manager import SourceManager
from config import Config
import vagrant
from fabric.api import env, execute, task, run, settings, sudo
from fabric.contrib.project import rsync_project
import os
import shutil
import random
from core_utils import get_global_path
from abstract_machine_controller import AbstractMachineController
from log_manager import logging
import os

logger = logging.getLogger('machine.VagrantController')
import tarfile
from config import Config
class VagrantController(AbstractMachineController):
    """
    Initialise, creer et controle une VM via Vagrant
    """

    def __init__(self, **kwarg):
        self.directories_to_clean = []
        self.vagrant = None
        super().__init__(**kwarg)

    @staticmethod
    def __get_real_machine_name(vagrant, test_machine_name:str) -> str:
        """
        Calcul le nom de la machine a partir des nom reellement present dans la configuration Virtualbox
        Si inexistant, la machine par default sera utilise (cas Vagrant mono machine)
        TODO gerer le cas ou default n'existe pas non plus
        """        
        return test_machine_name if test_machine_name in [vm.name for vm in vagrant.status()] else "default"

    def create_machine(self, global_config:Config, machine_configuration:Config, machine_name:str, source_manager:SourceManager, resume_machine=False):
        """
        Initialise et lance la VM
        """
        vagrant_orig_path = get_global_path(
            global_config=global_config, 
            in_path=machine_configuration.get('vagrant_dir')
        )
        machine_name = machine_name.replace('testauto_','')

        # Clone de la configuration dans un dossier a part
        # En effet, plusieurs instance de la VM doivent pouvoir etre cree
        self.vagrant_working_path = os.path.join(vagrant_orig_path, ".testauto_vms", machine_name)

        if os.path.isdir(self.vagrant_working_path):
            if resume_machine is False:
                # Cas ou on ne veut pas repartir d'une machine existante
                raise Exception(f'Erreur, la VM {machine_name} existe deja')
        else:    
            # Cas ou la VM est inexistante
            # creation de l'arborescence a partir du modele
            shutil.copytree(vagrant_orig_path, self.vagrant_working_path, ignore=shutil.ignore_patterns('.testauto_vms*')) 
            
        # Variabilisation du Vagrantfile
        env = dict(os.environ)
        env['TESTAUTO_HOSTNAME'] = machine_name
        self.vagrant = vagrant.Vagrant(self.vagrant_working_path, env=env)
        self.vagrant_vm_name = self.__get_real_machine_name(self.vagrant, machine_name)

        # Vagrant up
        self.vagrant.up(vm_name=self.vagrant_vm_name)

        # Synchronisation de chaque source
        for name, accessor in list(source_manager.get_accessors().items()):
            self._create_sync_folder(
                local_path=accessor.local_path, 
                vm_path=accessor.machine_path
            )            

    def is_aldready_exists(self, machine_configuration:Config, machine_name : str) -> bool:
        """
        Retourne True si la machine est deja existante
        """
        # calcul du chemin vers le vagrant file de la VM
        vagrant_dir = os.path.join(
            get_global_path(
                global_config=self.global_config, 
                in_path=machine_configuration.get('vagrant_dir')
            ), 
            ".testauto_vms", 
            machine_name.replace('testauto_','')
        )
        if not os.path.isdir(vagrant_dir):
            # Si pas de conf, on considere que la VM est down
            return False
        
        # Recuperation de l'etat via Vagrant
        vagrant_obj = vagrant.Vagrant(vagrant_dir)
        vagrant_vm_name = self.__get_real_machine_name(vagrant_obj, machine_name)
        vm = None
        for svm in vagrant_obj.status():
            if svm.name == vagrant_vm_name:
                vm = svm
                break
        
        # Si la VM existe c'est VRAI, sinon c'est FAUX
        res = vm is not None and (vm.state == 'running' or vm.state == 'poweroff')
        logger.debug('VM Already exist ?', res=res, state=vm.state)
        return res


    def resume_machine(self, global_config:Config, machine_configuration:Config, machine_name:str, source_manager:SourceManager):
        """
        Se connecte a une machine existante
        """
        logger.debug('debut resume machine', machine_name=machine_name)
        # On repart comme pour la creation d'une nouvelle VM a un parametre pres
        self.create_machine(global_config, machine_configuration, machine_name, source_manager, resume_machine=True)       
        logger.debug('fin resume machine', machine_name=machine_name)
      

    def put_in_file(self, content:str, file_path:str, makedir=False) -> tuple:
        """
        Permet de copier du contenu dans un fichier sur la machine
        :param content: Contenu a copier
        :param file_path: nom du fichier
        :return: code retour
        """
        if makedir:
            self.run_cmd('mkdir -p {}'.format(os.path.dirname(file_path)))
        return self.run_cmd(f"echo '{content}' > {file_path}")        

    def get_file_content(self, file_path:str) -> tuple:
        """
        Permet de recuperer le contenu d'un fichier sur la machine
        :param file_path: Chemin vers le fichier
        :return: contenu du fichier (string)
        """
        return self.run_cmd(f'cat {file_path}')
    

    def _create_sync_folder(self, local_path, vm_path):
        logger.debug("_create_sync_folder",local_path=local_path,vm_path=vm_path)
        self.run_cmd(f'mkdir -p {vm_path}')
        self.run_cmd(f'chmod 777 {vm_path}')
        if local_path[-1] != "/":
            local_path += "/"

        with settings(host_string=self.vagrant.user_hostname_port(vm_name=self.vagrant_vm_name),
            key_filename = self.vagrant.keyfile(vm_name=self.vagrant_vm_name),
            disable_known_hosts = True, warn_only=True):

            rsync_project(remote_dir=vm_path, local_dir=local_path, ssh_opts="-o StrictHostKeyChecking=no",
                         exclude=['.git'], delete=True)
    

    def run_cmd(self, command: str, workdir:str=None) -> tuple:
        """
        Lance une commande sur la VM.
        """
        ret=-1
        stdout=""

        with settings(host_string=self.vagrant.user_hostname_port(vm_name=self.vagrant_vm_name),
            key_filename = self.vagrant.keyfile(vm_name=self.vagrant_vm_name),
            disable_known_hosts = True, warn_only=True, ):
            prefix = ""
            if workdir is not None:
                prefix = f"cd {workdir} && "            
            result = sudo(prefix + command)
            ret = result.return_code
            stdout = result.stdout.strip()
            
        logger.debug('cmd.run', ret=str(ret), stdout=stdout)
        return ret, stdout

    def destroy_machine(self, global_config:Config, machine_configuration:Config, machine_name:str, source_manager:SourceManager):
        """
        Stop et supprime la VM
        """
        if self.vagrant != None:
            self.vagrant.destroy(vm_name=self.vagrant_vm_name)

        for path in self.directories_to_clean + [self.vagrant_working_path]:
            shutil.rmtree(path)
