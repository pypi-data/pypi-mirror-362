from source_manager import SourceManager
import os
from config import Config
class AbstractMachineController(object):
    """
        Classe abstraite d'un controlleur de machine
        Chaque implementation doit heriter de cette class
    """

    @staticmethod
    def pre_initialize(global_config:Config, machine_configuration:Config, source_manager:SourceManager):
        """
        Lorsque c'est necessaire
        permet d'initialise les pre-requis a la construction d'une machine
        """
        pass

    def is_aldready_exists(self, machine_configuration:Config, machine_name:str) -> bool:
        """
        Retoure True si la machine est deja existante
        """
        return False

    def create_machine(self, global_config:Config, machine_configuration:Config, machine_name:str, source_manager:SourceManager):
        """
        Initialise la machine
        A surcharger si necessaire
        """
        pass

    def resume_machine(self, global_config:Config, machine_configuration:Config, machine_name:str, source_manager:SourceManager):
        """
        Se connecte a une machine existante
        A surcharger si necessaire
        """
        pass


    def run_cmd(self, command:str) -> int:
        """
        Permet de lancer une commande sur la machine
        A surcharger
        """
        pass

    def run_python(self, script:str) -> int:
        """
        Permet de lancer une commande python sur la machine
        en fonction de l'environement
        """
        return self.run_cmd(
            command="{} {}".format(
                self.global_config.get('machine::env::pythonpath'),
                script
            )
        )

    def append_in_file(self, content:str, file_path:str) -> int:
        """
        Permet d'ajouter du contenu dans un fichier sur la machine
        :param content: Contenu a copier
        :param file_path: nom du fichier
        :return: code retour
        A surcharger
        """

        res, oldcontent = self.get_file_content(file_path=file_path)
        if res == 0:
            newcontent = "{}\n{}".format(oldcontent, content) if res is not False else content
        else:
            newcontent = content
        return self.put_in_file(newcontent, file_path)

    def put_in_file(self, content:str, file_path:str, makedir=False) -> int:
        """
        Permet de copier du contenu dans un fichier sur la machine
        :param content: Contenu a copier
        :param file_path: nom du fichier
        :return: code retour
        A surcharger
        """
        if makedir:
            self.run_cmd('mkdir -p {}'.format(os.path.dirname(file_path)))
        pass

    def get_file_content(self, file_path:str) -> str:
        """
        Permet de recuperer le contenu d'un fichier sur la machine
        :param file_path: Chemin vers le fichier
        :return: contenu du fichier (string)
        A surcharger
        """
        pass

    def destroy_machine(self, global_config:Config, machine_configuration:Config, machine_name:str, source_manager:SourceManager):
        """
        Liberation de la machine
        A surcharger
        """
        pass


    def __init__(self, global_config:Config, machine_configuration:Config, machine_name:str, source_manager:SourceManager, machine_preset_name:str):
        """
        A ne pas surcharger
        Ordonnance la construction de la machine
        """
        self.global_config = global_config
        self.machine_name = machine_name
        self.source_manager = source_manager
        self.machine_configuration = machine_configuration
        self.machine_preset_name = machine_preset_name

        if global_config.get('machine::resume_machine') == True \
        and self.is_aldready_exists(machine_name=machine_name, machine_configuration=machine_configuration) == True:
            # La machine existe deja et l'option resume est active
            self.resume_machine(
                global_config=self.global_config,
                machine_configuration=self.machine_configuration,
                machine_name=self.machine_name,
                source_manager=self.source_manager
            )
        else:
            # Creation d'une nouvelle machine
            self.create_machine(
                global_config=self.global_config,
                machine_configuration=self.machine_configuration,
                machine_name=self.machine_name,
                source_manager=self.source_manager
            )

        # Recuperation des variables d'environnement si existantes
        # Ces variables permettent de configurer les testauto en fonction de la machine
        ret, env_values = self.run_cmd("env")
        if ret == 0 and env_values != "":
            env_config = global_config.get_node('machine').get_node('env').config
            for v in env_values.split('\n'):
                if 'devopstestor_' in v:
                    tmp = v.split('=')
                    global_config.set('machine::env::{}'.format(tmp[0].replace('devopstestor_', '')), tmp[1])

    def __del__(self):
        """
        A ne pas surcharger
        Ordonnance selon le parametrage la suppression de la machine
        """
        if self.global_config.get('machine::preserve_machine') == False:
            self.destroy_machine(
                global_config=self.global_config,
                machine_name=self.machine_name,
                machine_configuration=self.machine_configuration,
                source_manager=self.source_manager
            )
