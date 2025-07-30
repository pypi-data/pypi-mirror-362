
from campaign_report import CampaignReport
from threading import Thread

from log_manager import logging
logger = logging.getLogger('core.ordonnanceur')
import sys
class Ordonnanceur():
    """
    L'ordonnanceur gere la parallelisation du lancement des testcases
    """
    def __init__(self, config_global, source_manager, tests_cases_loader, machines_factory, testcase_executor_factory, report_render_manager):
        """
        Lancement de l'ordonnanceur
        :param config_global: Config - Singleton d'access a la configuration global
        :param source_manager: SourceManager - Gestionnaire de sources
        :param tests_cases_loader: TestCaseLoader - Chargeur de testcase
        :param machines_factory: MachineFactory - Fabrique de machine
        :param testcase_executor_factory: TestcaseExecutorFactory - usine de testcases executors permettant de lancer un testcase
        """
        self.machines_factory = machines_factory
        self.testcase_executor_factory = testcase_executor_factory
        self.campagne_rapport = CampaignReport("Campagne de test")

        testcases = tests_cases_loader.get_test_cases()
        if len(testcases) > 1 and config_global.get('machine::parallelize', False) == True:
            max_process = config_global.get('machine::max_process')
            logger.debut('lancement_campagne', 'Lancement parallele des testscases', max_process=max_process)
            # Lancement des testscases avec parallelisation
            self.play_testcases_async(testcases, max_process)
            logger.fin('lancement_campagne', 'Lancement parallele des testscases', max_process=max_process)
        else:
            logger.debut('lancement_campagne', 'Lancement synchrone des testscases')
            # Lancement synchrone des testscases
            self.play_testcases(testcases)
            logger.fin('lancement_campagne', 'Lancement synchrone des testscases')

        # Calcul des donnes du rapport
        self.campagne_rapport.compute_result_bychildren()

        # Creation des rendus de rapport
        report_render_manager.compute_renders(self.campagne_rapport)
        if self.campagne_rapport.result == True:
            sys.exit(0)
        else:
            sys.exit(-1)

    def play_testcases(self, testcases):
        """
        Lancement synchrone des testscases selectionnes
        :param testcases: list<TestCase> - testscases a lancer
        """
        logger.debut('ordonnanceur')
        for test_case in testcases:
            test_case_report = test_case.run(
                machines_factory=self.machines_factory,
                testcase_executor_factory=self.testcase_executor_factory
            )
            self.campagne_rapport.add_testcase(test_case_report)
        logger.fin('ordonnanceur')

    def play_testcases_async(self, testcases, thread_max):
        """
        Lancement multithread des testscases selectionnes
        :param testcases: list<TestCase> - testscases a lancer
        """
        class LanceurTestCase(Thread):
            # Classe interne
            def __init__(
                self,
                testcases,
                campagne_rapport,
                machines_factory,
                testcase_executor_factory
            ):
                Thread.__init__(self)
                self.testcases = testcases
                self.campagne_rapport = campagne_rapport
                self.machines_factory = machines_factory
                self.testcase_executor_factory = testcase_executor_factory

            def run(self):
                # Depilage et traitement d'un testcase
                while len(self.testcases) > 0:
                    testcase = self.testcases.pop()
                    try:
                        test_case_report = testcase.run(
                            machines_factory=self.machines_factory,
                            testcase_executor_factory=self.testcase_executor_factory
                        )
                        self.campagne_rapport.add_testcase(test_case_report)
                    except Exception as e:
                        logger.error('LanceurTestCase - {} - Erreur : {}'.format(self.getName(), e))

        nb_pool = thread_max if len(testcases) >= thread_max else len(testcases)
        threads = []
        for num in range(0, nb_pool):
            # Creation des threads
            thread = LanceurTestCase(
                testcases=testcases,
                campagne_rapport=self.campagne_rapport,
                machines_factory=self.machines_factory,
                testcase_executor_factory=self.testcase_executor_factory
            )
            # Lancement des threads
            thread.start()
            threads.append(thread)

        for thread in threads:
            # Attente de la fin de tous les threads
            thread.join()
