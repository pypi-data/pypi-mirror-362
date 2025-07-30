
import os
from abstract_machine_controller import AbstractMachineController
from log_manager import logging
logger = logging.getLogger('machine.DebugController')

class DebugController(AbstractMachineController):
    """
    Permet de mocker un controleur
    Des logs sont generer lorsqu'il est appelle
    """

    @staticmethod
    def pre_initialize(global_config, machine_configuration, source_manager):
        """
        permet de pre initialise la machine
        Construit l'image docker presente dans le dockerfile dockerfile_dir_path/Dockerfile
        """
        logger.debug('pre_initialize')

    def create_machine(self, global_config, machine_configuration, machine_name, source_manager):
        """
        Initialise la machine
        """
        logger.debug('create_machine')

    def run_cmd(self, command):
        """
        Lance une commande sur le container.
        :param command: commabde a lancer
        :return: status, output
        """
        logger.debug('commande', command=command, machine_name=self.machine_name)

        return 0, "output"

    def put_in_file(self, content, file_path, makedir=False):
        """
        Permet de copier du contenu dans un fichier sur la machine
        :param content: Contenu a copier
        :param file_path: nom du fichier
        :return: status, output
        """
        logger.debug('put_in_file', file_path=file_path, content=content,  machine_name=self.machine_name)
        return 0, "{'toto':'titi'}"

    def get_file_content(self, file_path):
        """
        Permet de recuperer le contenu d'un fichier sur la machine
        :param file_path: Chemin vers le fichier
        :return: status, contenu du fichier (string)
        """
        logger.debug('get_filecontent', filepath=file_path, machine_name=self.machine_name)
        return 0, "{}"

    def destroy_machine(self, global_config, machine_configuration, machine_name, source_manager):
        """
        Stop et supprime le container lorsque l'objet est supprime
        """
        logger.debug("destroy_machine", machine_name=machine_name)
