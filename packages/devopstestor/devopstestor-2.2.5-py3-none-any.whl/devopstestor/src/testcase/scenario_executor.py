from scenario_report import ScenarioReport
from verifier_report import VerifierReport
from deployment_report import DeploymentReport
import json_utils
from datetime import datetime
from core_utils import import_py_file, get_class_name
from utils import copy_merge_recursive_dict
import json

from log_manager import logging

class ScenarioExecutor():
    code_to_result={
        0: True
    }

    def __init__(self, global_config, machines_factory, testcase_name, name, title, description, machine_provisionner, default_target, verifieurs_list=[], expected_result=True, **scenario_args):
        """
        Constructeur : Initialisation
        """
        self.global_config = global_config
        self.machines_factory = machines_factory
        self.testcase_name = testcase_name
        self.name = name
        self.title = title
        self.description = description
        self.verifieurs_list = verifieurs_list
        self.expected_result = expected_result
        self.machine_provisionner = machine_provisionner
        self.default_target = default_target
        self.scenario_args = scenario_args
        self.log = logging.getLogger('testcase.scenario_executor')

    def run(self, is_skipped):
        """
        Lance les tests : scenarios + verifieurs associes
        """
        scenario_report = ScenarioReport(
            name=self.name,
            title=self.title,
            description=self.description
        )
        self.log.info('Lancement scenario', scenario=self.name)

        # Lancement du Deploiement
        deploy_report = DeploymentReport(self.name)
        if is_skipped == False:
            ret, out = self.play_scenario(
                machine_provisionner=self.machine_provisionner,
                scenario_name=self.name,
                **self.scenario_args
            )
            if ret == None: # skipped by config
                ret = self.expected_result

            # Gestion du cas ou le deploiement doit etre KO
            if self.expected_result == False:
                ret = not ret
        else:
            # Resultat par defaut si une etape est KO
            ret = False
            out = "Skipped"

        deploy_report.set_node_result(
            result=ret,
            stdout=out
        )
        scenario_report.add_deployment(deploy_report)

        # Lancement des verifiers
        verifiers_report = VerifierReport(self.verifieurs_list)
        if len(self.verifieurs_list) > 0:
            self.log.info('Lancement des verifieurs')
            verifier_data = None
            if is_skipped == False:
                ret, verifier_data = self.play_verifiers(self.machine_provisionner, self.verifieurs_list)
                if ret == False:
                    # Si le deploiement est KO, on skip la suite du testcase
                    is_skipped = True
                elif ret == None: #skipped by config
                    ret = True
            else:
                # Resultat par defaut si une etape est KO
                ret = False
                verifier_data = {
                    'stdout': "Skipped"
                }
        else:
            verifier_data = {
                'stdout': "Empty list"
            }
        verifiers_report.set_verifiers_result(
            result=ret,
            verifier_data=verifier_data
        )
        scenario_report.set_verifier_report(verifiers_report)
        scenario_report.compute_result_bychildren()
        return scenario_report


    def play_scenario(self, machine_provisionner, scenario_name, **scenarios_args):
        """
        Lance le scenario sur l'hote
        Le scenario sera joue a travers le provisioner avec les arguments scenarios_args
        """
        self.log.info('Lancement deploiement', scenario=self.name)
        datetimeformat="%Y-%m-%d %H:%M:%S.%f"
        time_context = {
            "start_time": datetime.utcnow().strftime(datetimeformat)
        }

        if not self.global_config.get('testcase::skip_deploy') == True:
            tmp_pathlist = scenario_name.split('.')
            test_function = tmp_pathlist.pop()
            test_relfilepath = 'scenarios/' + '/'.join(tmp_pathlist) + '.py'

            # Lancement du scenario
            scenario_module = import_py_file(self.global_config, test_relfilepath)
            scenario_function = getattr(scenario_module, test_function)
            scenario_args = scenario_function.__code__.co_varnames
            arg_to_pass = dict(scenarios_args)
            for arg_name in scenario_args:
                if "_provisionner" in arg_name: # Recuperation du provisionner selon le nom de l'argument du scenario
                    if arg_name == "machine_provisionner":
                        arg_to_pass["machine_provisionner"] = machine_provisionner # default_machine_provisionner
                    else:
                        arg_to_pass[arg_name] = self.machines_factory.get_builded_machine_provisionner(
                            testcase_name=self.testcase_name,
                            machine_name=machine_provisionner.get_machine_controller().machine_name,
                            provisionner_controller_class_name=get_class_name(arg_name), # Calcul du nom de class du provisionner
                            machine_controller_preset=self.default_target.get('machine_preset')
                        )
                elif arg_name == 'global_config':
                    arg_to_pass['global_config'] = self.global_config

            scenario_result = scenario_function(
                # machine_provisionner=machine_provisionner,
                **arg_to_pass
            )
            try:
                statut, stdout = scenario_result
            except:
                raise Exception('Code retour scenario {} incorrect ! - format attendu : statut, stdout')
            time_context['end_time'] = datetime.utcnow().strftime(datetimeformat)

            # Met a jour le contexte des verifieurs
            machine_provisionner.get_machine_controller().put_in_file(
                content=json.dumps(
                    {
                        "scenario": {
                            'name': scenario_name,
                            'args': scenarios_args,
                            'time_context': time_context
                        }
                    },
                    cls=json_utils.EnhancedJSONEncoder
                ),
                file_path='/tmp/verifiers_context.json'
            )
            return statut, stdout
        else:
            # Cas ou le deploiement n'est pas joue
            machine_provisionner.get_machine_controller().put_in_file(
                content=json.dumps(
                    {
                        "scenario": {
                            'name': "skipped",
                            'args': scenarios_args,
                            'time_context': {
                                'start_time': time_context['start_time'],
                                'end_time': time_context['start_time'] # Start == endtime
                            }
                        }
                    }
                ),
                file_path='/tmp/verifiers_context.json'
            )
            return None, "Skipped by config"

    def play_verifiers(self, machine_provisionner, verifiers):
        """
        Lance les verifieurs sur la machine
        """
        self.log.debut('Lancement des verifiers', scenario=self.name)
        if not self.global_config.get('testcase::skip_verifiers') == True:
            params = {
                "verifiers_paths": ["/srv/verifiers/custom/tests/", "/srv/verifiers/generic/tests/", "/srv/verifiers/testcase/tests/"],
                "fixtures_path": ["/srv/verifiers/custom/fixtures/", "/srv/verifiers/generic/fixtures/"],
                "utils_path": ["/srv/verifiers/custom/utils/", "/srv/verifiers/generic/utils/"],
                "report_path": "/tmp/verifier_report.json",
                "verifiers_targets": verifiers
            }

            machine = machine_provisionner.get_machine_controller()
            ret_code, stdout = machine.run_python("/srv/verifiers/generic/utils/verififier_luncher.py '"+json.dumps(params)+"'")

            ret, report_str =  machine.get_file_content(file_path=params['report_path'])
            print("REPORT")
            print(report_str)
            verifier_data = json.loads(report_str)
            verifier_data['stdout'] = stdout
            for line in stdout.split('\n'):
                self.log.info('Verifier result - {}'.format(line))
            self.log.fin('Lancement des verifiers', scenario=self.name)
            return self.code_to_result.get(ret_code, False), verifier_data
        else:
            return None, None
