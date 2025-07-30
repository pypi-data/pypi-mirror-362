from scenario_executor import ScenarioExecutor
from testcase_report import TestcaseReport
from log_manager import logging
import re

class TestcaseExecutor():
    def __init__(self, global_config, name, tags, default_target, machines_factory):
        """
        Constructeur : Initialisation
        """
        self.global_config = global_config
        self.machines_factory = machines_factory
        self.name = name
        self.tags = tags
        self.default_target = default_target
        self.scenarios = []
        self.log = logging.getLogger('testcase.testcase_executor')
        self.step_filter_regex = re.compile(self.global_config.get('testcase::filtre_steps'))

    def add_scenario(self, scenario_name, machine_provisionner, scenario_title = None, scenario_description = "",  verifieurs_list = [], expected_result=True, scenario_args={}):
        """
        Ajoute un scenario et sa liste de verifieurs associes
        """

        if scenario_title is None:
            scenario_title = "{} - {}".format(len(self.scenarios) + 1, scenario_name)
        if self.step_filter_regex.match(scenario_title):
            # Build verifiers list and files
            # Verifier can be path or content, if content, a file is generated here
            verifier_basepath = '/srv/verifiers/testcase/tests'
            verifier_basename = f"testcase.{scenario_title.replace(' ','')}"
            # cleanup old builded verifiers
            machine_provisionner.get_machine_controller().run_cmd(f"rm -rf {verifier_basepath}/{verifier_basename.replace('.', '/')}")
            verifieurs_list_builded = []
            for v in verifieurs_list:
                if isinstance(v, str):
                    verifieurs_list_builded.append(v)
                elif isinstance(v, dict) and len(v) == 1:
                    for vname, vconcent in v.items():
                        nvname = f"{verifier_basename}.{vname}"
                        machine_provisionner.get_machine_controller().put_in_file(
                            content=vconcent, 
                            file_path=f"{verifier_basepath}/{nvname.replace('.', '/')}.py", 
                            makedir=True)
                        verifieurs_list_builded.append(nvname)
                else:
                    raise ValueError('Format attendu verifier : str ou vname -> vcontent, data='+str(v))

            self.scenarios.append(ScenarioExecutor(
                global_config=self.global_config,
                machines_factory=self.machines_factory,
                testcase_name=self.name,
                name=scenario_name,
                title=scenario_title,
                description=scenario_description,
                verifieurs_list=verifieurs_list_builded,
                expected_result=expected_result,
                machine_provisionner=machine_provisionner,
                default_target=self.default_target,
                **scenario_args
            ))

    def run(self):
        """
        Lance chaque scenarios et retourne le resultat via un embriquement de rapports
        """
        self.log.debut('test_case_'+self.name)
        test_case_report = TestcaseReport(self.name, self.tags)
        is_skipped = False
        for scenario in self.scenarios:
            scenario_report = scenario.run(
                is_skipped=is_skipped
            )
            if scenario_report.result == False:
                is_skipped = True
            test_case_report.add_scenario(scenario_report)

        # Nettoyage machines
        self.machines_factory.notify_testcase_destroy(testcase_name=self.name)
        
        # Calcul du resultat des noeuds
        test_case_report.compute_result_bychildren()
        self.log.fin('test_case_'+self.name)
        return test_case_report
