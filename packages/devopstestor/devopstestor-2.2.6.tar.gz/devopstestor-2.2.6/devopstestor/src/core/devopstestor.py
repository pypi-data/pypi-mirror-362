# Desactivation de l'import relatif
import sys, os, yaml

class Devopstestor():
   """
   Initialisateur de la solution de test automatise
   """
   def __init__(self, client_path, global_config_overload={}, **main_args):
       """
       Initialise l'outils
       :param client_path: chemin vers le dossier permettant de surcharger les fichiers generiques
       :param global_config_overload: dict de surcharge de la configuration global
       :param main_args: dict d'arguments comme defini dans la configuration "arguments::parameters"
       """
       self.client_path = client_path
       self.lib_path = os.path.abspath(os.path.realpath(__file__) + "/../../..")
       Devopstestor.init_path(clients_paths=[self.client_path]) # Les imports ne deviennent dispo qu'a partir d'ici
       self.init_config = None
       self.__update_config(global_config_overload=global_config_overload, main_args=main_args)

   def start(self, global_config_overload={}, **main_args):
       self.__update_config(global_config_overload=global_config_overload, main_args=main_args)
       if self.global_config.get('core::show_config', False):
           print('--------------- show_config  ---------------')
           print('- Configuration chargee -')
           print('---')
           print(yaml.dump(self.global_config.config))
           print('--------------- ------------ ---------------')
       else:
           self.__load_source_manager()
           self.__load_test_cases()
           self.__load_machines_factory()
           self.__load_testcase_executor_factory()
           self.__load_report_render_manager()
           self.__load_ordonannceur()


   @staticmethod
   def init_path(clients_paths=[]):
       """
       Definition des path d'import
       Avant le chargement de cette fonction, les imports sont pas possible
       """
       lib_path = os.path.abspath(os.path.realpath(__file__) + "/../../..")
       root_paths = [lib_path] + clients_paths
       # Nettoyage du path pour ne garder que les lib
       filter = os.path.abspath(os.path.realpath(__file__) + "/../../../")
       for path in sys.path:
           if path.startswith(filter):
               sys.path.remove(path)

       # Creation du path pour la surcharge du framwork par le client
       for module_name in ['lib', 'machine', 'verifiers', 'scenarios', 'provisionner', 'sources', 'testcase', 'reporting']:
           for root_path in root_paths:
               sys.path.append(root_path + "/src/" + module_name)
       sys.path.append(lib_path + "/src/core")
       sys.path.append(lib_path + "/src/abstract")

   def __update_config(self, global_config_overload={}, main_args={}):
       """
       Charge en memoire la configuration de l'outils
       """
       from global_config_factory import GlobalConfigFactory
       args = {}
       if self.init_config is not None:
           args['base_config'] = self.init_config

       self.global_config = GlobalConfigFactory.load_global_config(
        lib_path=self.lib_path,
        client_path=self.client_path,
        global_config_overload=global_config_overload,
        main_args=main_args,
        **args
       )

   def __load_source_manager(self):
       """
       Recuperation des differentes sources de donnes
       """
       from source_manager import SourceManager
       self.source_manager = SourceManager(
           global_config=self.global_config
       )

       # Add lib to machine
       self.source_manager.add_source_accessor(
           name="devopstestor",
           source_config={
               "accessor_type": "DirlinkSourceAccessor",
               "path":{
                 "local": self.lib_path + "/src/",
                 "machine": '/usr/lib/python3.6/site-packages/devopstestor/'
               }
           }
       )

   def __load_test_cases(self):
       """
       Recherche et met en memoire les configurations relatives aux testcase
       """
       from tests_cases_loader import TestCaseLoader
       self.tests_cases_loader = TestCaseLoader(
           global_config=self.global_config
       )
       if self.global_config.get('testcase::list_only') == True:
           for testcase in self.tests_cases_loader.get_test_cases():
               print(" - " + testcase.name)
           sys.exit(0)

   def __load_machines_factory(self):
       """
       Initialisation de generateur de machine
       """
       from machines_factory import MachinesFactory
       self.machines_factory = MachinesFactory(
           global_config=self.global_config,
           source_manager=self.source_manager
       )

   def __load_testcase_executor_factory(self):
       """
       Initialisation du lanceur de scenarios
       """
       from testcase_executor_factory import TestcaseExecutorFactory
       self.testcase_executor_factory = TestcaseExecutorFactory(
           global_config=self.global_config,
           machines_factory=self.machines_factory
       )

   def __load_report_render_manager(self):
       """
       Initialisation du gestionnaire de generation de rapport
       """
       from report_render_manager import ReportRenderManager
       self.report_render_manager = ReportRenderManager(
           config_global=self.global_config
       )

   def __load_ordonannceur(self):
       """
       Initialisation de l'ordonnanceur des testcase
       """
       from ordonnanceur import Ordonnanceur
       self.ordonnanceur = Ordonnanceur(
           config_global=self.global_config,
           source_manager=self.source_manager,
           tests_cases_loader=self.tests_cases_loader,
           machines_factory=self.machines_factory,
           testcase_executor_factory=self.testcase_executor_factory,
           report_render_manager=self.report_render_manager
       )
