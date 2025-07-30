from core_utils import get_module_name, instance_object
import time
from log_manager import logging
from config import Config
from utils import copy_merge_recursive_list_of_dict
logger = logging.getLogger('core.MachineFactory')

class MachinesFactory(object):
    """
    Permet de creer des machines sur lesquels des tests pourront etre lancess
    """
    def __init__(self, global_config, source_manager):
        """
        Initialisation du gestionnaire de machines
        :param global_config: Config - accesseur a la configuration global
        :param source_manager: SourceManager - gestionnaire de sources
        """
        # Liste des machines deja charges
        self.presets_preinitialized = [] # Liste des preset preinitialise (pas forcement instancie)
        self.allocations_per_testcase = {} # testcase_name -> list of (preset_name, machine_name,  provisionner_id): utilise pour la suppression
        self.created_machines_controller_presets = {} # machine_name -> MachineController (unique par "machine_name")
        self.machine_controll_modules = {} # machine_controller_className -> module (resultat du import nom_module)
        self.created_machines_provisionner = {} # preset_name, machine_name_provisionner_name -> MachineProvisionner (multiple par "machine_name")

        self.source_manager = source_manager
        self.global_config = global_config
        self.mutex_actif = False # Mutex pour ne pas // les appels a get_builded_machine_provisionner


    def get_builded_machine_provisionner(self, testcase_name, machine_name, machine_controller_preset = None, provisionner_controller_class_name = None, **machine_controller_args):
        """
        Construit ou retourne une machine identifiee par son nom ainsi qu'un provisionneur
        Si une machine de meme nom et le preset qu'une machine existante est demande, celle ci-est retournee
        Si une machine de meme nom mais pas de meme preset qu'une machine existante est demandee, une erreur est levee
        Un provisionner est instanciee pour chaque trio de demande machine/preset/provisionner
        :param testcase_name: str - nom du testcase a la source de la demande
        :param machine_name: str - nom de la machine a generer
        :param machine_controller_args: kwarg - parametre a passer au controleur de machine
        :return: MachineController - nouvelle instance d'un controleur de machine
        """
        # Attente liberation du mutex
        while self.mutex_actif is True:
            logger.debug('get_builded_machine_provisionner() : Waiting for mutex free')
            time.sleep(10)

        self.mutex_actif = True

        # Recuperation des metadonnees permettant de generer des machines avec le controleur choisit
        preset_name = machine_controller_preset if machine_controller_preset is not None else self.global_config.get('machine::preset_name')

        ########## Presets de machines ############
        # Calcul du preset_config en prenant en commpte le mecanisme d'heritage entre presets
        presets_node = self.global_config.get_node('machine').get_node('presets')
        base_preset_config = presets_node.get_node(preset_name)
        presets_dicts_to_merge = [ presets_node.get_node(pname).config for pname in base_preset_config.get('extends', []) ]
        preset_config_dict = copy_merge_recursive_list_of_dict(*presets_dicts_to_merge, base_preset_config.config)
        preset_config_dict["extends_presets"] = presets_dicts_to_merge
        preset_config = Config.create_from_dict(preset_config_dict)

        machine_controller_className = preset_config.get('controller_class_name')
        provisionner_controller_className = provisionner_controller_class_name if provisionner_controller_class_name is not None else self.global_config.get('provisionner::controller_class_name')

        ########## Cas ERREUR ############
        # Detection du cas d'erreur machine demande existe deja mais pas sur le preset demandee (confit de config)
        if machine_name in self.created_machines_controller_presets and self.created_machines_controller_presets[machine_name].machine_preset_name != preset_name:
            raise Exception('La machine demandee ({}) existe deja avec un autre type de machine preset({} != {})'.format(
                machine_name,
                preset_name,
                self.created_machines_controller_presets[machine_name].machine_preset_name
                )
            )

        ########## Import ############
        # Import de la classe si elle n'a pas deja ete chargee
        if machine_controller_className not in self.machine_controll_modules:
            self.machine_controll_modules[machine_controller_className] = __import__(get_module_name(machine_controller_className))

        ########## pre_initialize ############
        # Appel la methode statique pre_initialize du controller de machine si la class n'a pas encore ete chargee
        # Lorsque c'est nessaire, ceci permet de pre initialise la machine avant la premiere instanciation (si le preset n'est pas charge)
        if preset_name not in self.presets_preinitialized:
            self.presets_preinitialized.append(preset_name)
            getattr(getattr(self.machine_controll_modules[machine_controller_className], machine_controller_className), "pre_initialize")(
                global_config=self.global_config,
                machine_configuration=preset_config,
                source_manager=self.source_manager
            )


        ########## Instanciation ############
        # Cette machine as t-elle deja ete cree ?
        if machine_name not in self.created_machines_controller_presets:
            # Instanciation du controller de machine
            self.created_machines_controller_presets[machine_name] = getattr(self.machine_controll_modules[machine_controller_className], machine_controller_className)(
                global_config=self.global_config,
                machine_configuration=preset_config,
                machine_name=machine_name,
                source_manager=self.source_manager,
                machine_preset_name=preset_name
            )

        ########## Provisioner ############
        provisionner_id = f"{preset_name}_{provisionner_controller_className}_{machine_name}"
        # Ce provisionner pour cette machine exist-t il deja ?
        if provisionner_id not in self.created_machines_provisionner:
            # Instanciation du provisioner qui sera l'interface des testcases
            self.created_machines_provisionner[provisionner_id] = instance_object(
                class_name=provisionner_controller_className,
                global_config=self.global_config,
                machine_controller=self.created_machines_controller_presets[machine_name],
                machine_name=machine_name
            )

        self.mutex_actif = False

        ######## Enregistrement de l'allocation ########
        if not testcase_name in self.allocations_per_testcase:
            self.allocations_per_testcase[testcase_name] = []
        self.allocations_per_testcase[testcase_name].append({
            "machine_name": machine_name,
            "provisionner_id": provisionner_id
        })

        return self.created_machines_provisionner[provisionner_id]

    def notify_testcase_destroy(self, testcase_name):
        """
        Cette methode est lance lorsqu'un testcase est termine dans le but de nettoyer les machines qui lui sont lies
        :param testcase_name: str - nom du testcase a la source de la demande
        """
        for allocation in self.allocations_per_testcase[testcase_name]:
            # Si ressource encore chargee alors on la supprime
            # La ressouce peut avoir ete supprimme via une autre allocation ou un doublon dans la list
            if allocation['machine_name'] in self.created_machines_controller_presets:
                del self.created_machines_controller_presets[allocation['machine_name']]
            if allocation['provisionner_id'] in self.created_machines_provisionner:
                del self.created_machines_provisionner[allocation['provisionner_id']]
        del self.allocations_per_testcase[testcase_name]
