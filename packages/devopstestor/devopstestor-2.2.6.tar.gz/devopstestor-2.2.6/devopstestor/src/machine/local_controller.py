from config import Config
from source_manager import SourceManager
import sys
import os
import subprocess
from abstract_machine_controller import AbstractMachineController
from log_manager import logging
logger = logging.getLogger('machine.LocalController')

class LocalController(AbstractMachineController):
    @staticmethod
    def pre_initialize(global_config:Config, machine_configuration:Config, source_manager:SourceManager):
        global_config.set('machine::parallelize', False) # parallelize forbiden in Local mode

    def create_machine(self, global_config:Config, machine_configuration:Config, machine_name:str, source_manager:SourceManager):
        """
        Initialisation des proprietes d'instance
        """
        self.file_to_clean = []

        # Creation des liens symbomliques pour acceder aux sources
        for name, accessor in list(source_manager.get_accessors().items()):
            if not os.path.exists(accessor.machine_path):
                self.run_cmd('mkdir -p {}'.format(os.path.abspath(accessor.machine_path+"/..")))
                self.run_cmd('ln -s {} {}'.format(accessor.local_path, accessor.machine_path))

    def destroy_machine(self, global_config:Config, machine_configuration:Config, machine_name:str, source_manager:SourceManager):
        """
        Nettoyage
        Chaque modifications identifiees apporte sur la machine en local doit etre nettoyee
        """
        for path in self.file_to_clean:
            logger.info('Nettoyage du chemin temporaire', path=path)
            os.remove(path)

    def put_in_file(self, content:str, file_path:str, makedir=False) -> tuple:
        """
        Permet de copier du contenu dans un fichier sur la machine
        :param content: Contenu a copier
        :param file_path: nom du fichier
        :return: code retour
        """
        logger.info('put_in_file', filepath=file_path, content=content,  machine_name=self.machine_name)
        # Sauvegarde de l'etat precedent
        if not os.path.exists(file_path):
            self.file_to_clean.append(file_path)
        if makedir:
            self.run_cmd('mkdir -p {}'.format(os.path.dirname(file_path)))
            
        with open(file_path, "w+") as f:
            f.write(content)

        return 0, ""

    def get_file_content(self, file_path:str) -> tuple:
        """
        Permet de recuperer le contenu d'un fichier sur la machine
        :param file_path: Chemin vers le fichier
        :return: contenu du fichier (string)
        """
        logger.debug('get_filecontent', file_path=file_path, machine_name=self.machine_name)

        return self.run_cmd('cat ' + file_path)

    def run_python(self, script:str) -> tuple:
        """
        Permet de lancer une commande python sur la machine
        en fonction de l'environement
        Surcharge AbstractMachineController car specificites
        """
        return self.run_cmd(
            command="{} {}".format(
                sys.executable, # on reprend le meme binaire python que celui du moteur
                script
            )
        )

    def run_cmd(self, command:str) -> tuple:
        '''
        Lance une commande sur le conteneur.
        '''
        logger.debut('commande', "Lancement d'une commande sur le conteneur", machine_name=self.machine_name, command=command)
        ret = 0
        output = ""
        try:
            output = subprocess.check_output(
                [command],
                shell = True
            )
        except subprocess.CalledProcessError as e:
            logger.error('Erreur lors du lancement de la commande', command=command)
            ret = e.returncode
            output = e.output
        finally:
            logger.fin('commande', command=command, machine_name=self.machine_name, ret_code=ret)
        return ret, str(output, 'utf-8') #convert bytes to str
