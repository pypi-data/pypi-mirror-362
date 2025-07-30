from utils import copy_merge_recursive_dict
import os
import yaml
import json

from log_manager import logging
log = logging.getLogger('core.ordonnanceur')
from utils import grep, tail
class TestCase():
    """
    Gestion d'un test case
    """
    def __init__(self, config_path, global_config, name, test_case_conf):
        """
        Initialiastion d'un test case

        :param config_path: str - chemin vers le fichier testcase
        :param global_config: Config - accesseur aux donnes de configuration
        :param name: str - nom du testcase
        :param test_case_conf: dict - contenu du fichier testcase

        """
        self.contexte = {}
        self.tags = test_case_conf.get('tags', [])
        self.name = name
        self.global_config = global_config
        self.test_case_conf = test_case_conf

        if 'contexte_list' in test_case_conf:
            self.contexte = self.__overload_list_of_contextes(test_case_conf['contexte_list'])

    def get_contexte(self):
        """
        :return dict - contextes merges
        """
        return self.contexte


    def run(self, machines_factory, testcase_executor_factory):
        """
        Lance un testcase

        :machines_factory: MachinesFactory - Usine de machine
        :testcase_executor_factory: TestcaseExecutorFactory - Usine de TestcaseExecutor
        :return: TestcaseReport - Rapport d'execution du testcase
        """
        log.debut('test_case_'+self.name)

        # Recuperation d'une machine
        default_machine_provisionner = machines_factory.get_builded_machine_provisionner(
            testcase_name=self.name,
            machine_name=self.test_case_conf.get('target', {}).get("machine_name", self.name),
            machine_controller_preset=self.test_case_conf.get('target', {}).get("machine_preset"),
            provisionner_controller_class_name=self.test_case_conf.get('target', {}).get("provisioner_className")
        )
        skip = False

        testcase_exec = testcase_executor_factory.create_testcase_executor(
            name=self.name,
            tags=self.test_case_conf.get('tags', []),
            default_target=self.test_case_conf.get('target', {})
        )

        # Iteration par etapes
        scenario_id = 0
        for scenario in self.test_case_conf['steps']:
            if not 'args' in scenario:
                scenario['args'] = {}
            scenario['args']['init_contexte'] = self.__overload_list_of_contextes([self.contexte, scenario.get('contexte', {})])
            if 'target' in scenario: # Gestion du multimachine
                curr_provisionner = machines_factory.get_builded_machine_provisionner(
                    testcase_name=self.name,
                    machine_name=scenario.get('target').get("machine_name", "{}.scenario{}".format(self.name, scenario_id)),
                    machine_controller_preset=scenario.get('target').get("machine_preset"),
                    provisionner_controller_class_name=scenario.get('target').get("provisioner_className")
                )
            else:
                curr_provisionner = default_machine_provisionner

            testcase_exec.add_scenario(
                scenario_name=scenario['name'],
                verifieurs_list=scenario.get('verifiers', []),
                scenario_title=scenario.get('title'),
                scenario_description=scenario.get('description', 'Aucune description'),
                expected_result=scenario.get('expected_result', True),
                machine_provisionner=curr_provisionner,
                scenario_args=scenario['args']
            )
            scenario_id += 1

        test_case_report = testcase_exec.run()
        log.fin('test_case_'+self.name)
        return test_case_report

    ################################### Methodes utils ############################################
    def __overload_list_of_contextes(self, dict_list):
        """
        Genere un dictionnaire par merge de chaque element d'une liste

        :dict_list: list<dict> - List des contextes a merger
        :return: dict - contextes merges
        """
        res = {}
        for contexte in dict_list:
            res = copy_merge_recursive_dict(
                defaut=res,
                source=self.__resolve_include(contexte)
            )
        return res

    def __resolve_include(self, contexte_node):
        """
        Remplacement des "include" contenu dans les contexte par le contenu des fichiers a inclures

        :contexte_node: dict - noeud d'un contexte
        :return: dict - contextes merges
        """
        if "include" in contexte_node:
            # Chargement des fichiers
            include_childs = []
            for lpath in contexte_node['include']:
                include_childs.append(
                    self.__resolve_include( # Le fichier inclus peut avoir un include
                        yaml.load(
                            open(self.__get_real_path(lpath)),
                            Loader=yaml.Loader
                        )
                    )
                )
            return self.__overload_list_of_contextes(include_childs)
        else:
            return contexte_node

    def __get_real_path(self, lpath):
        """
        Resoud le chemin parametre dans le contexte

        :lpath: str - chemin relatif a testcase::base_path
        :return: str - chemin absolu
        """
        lpath = lpath.replace('.yaml', '')

        for curr_base_path in self.global_config.get('testcase::base_path'):
            real_path = '{}/{}'.format(
                curr_base_path,
                '/'.join(lpath.split('.'))
            )
            if not os.path.exists(real_path):
                real_path = real_path + '.yaml'

            if os.path.exists(real_path):
                if os.path.isdir(real_path):
                    # Meme comportement que les contexte saltstack
                    real_path = real_path + "/init.yaml"

                if os.path.isfile(real_path):
                    # Retourne le chemin si valide
                    return real_path

        # Si le chemin ne conduit pas a un fichier, une exception est levee
        raise Exception("Testcase {} config error : path {} not exist".format(self.name, lpath))
        return None
