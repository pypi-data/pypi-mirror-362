import datetime
import json

class ReportElkRenderer():
    def __init__(self, config_global, campaign_report):
        """
        Creation du rapport d'execution sous forme de metriques ELK
        :param global_config: Config - accesseur aux donnes de configuration
        :param campaign_report: CampaignReport - donnes du rapport
        """
        self.metrics = []
        self.context = {
            "campaign_id": datetime.datetime.now().isoformat()
        }
        context = config_global.get_node('report').get_node('report_context').config
        if context is not None:
            self.context.update(context)

        self.add_metric(
            typeid='campaign',
            datetime=campaign_report.datetime,
            campaigne_name=campaign_report.elem_name,
            campaigne_result=self.__convertResultStr(campaign_report.result),
            campaigne_duree=campaign_report.duree
        )

        testcases = campaign_report.get_child_list('testcases')
        for testcase in testcases:
            self.add_metric(
                typeid='testcase',
                datetime=testcase.datetime,
                testcase_name=testcase.elem_name,
                testcase_result=self.__convertResultStr(testcase.result),
                testcase_stdout=testcase.stdout,
                testcase_duree=testcase.duree
            )
            for tag in testcase.tags:
                self.add_metric(
                    typeid='tag',
                    datetime=testcase.datetime,
                    testcase_name=testcase.elem_name,
                    testcase_result=self.__convertResultStr(testcase.result),
                    testcase_tag=tag
                )
            for scenario in testcase.get_child_list('scenarios'):
                self.add_metric(
                    typeid='scenario',
                    datetime=scenario.datetime,
                    testcase_name=testcase.elem_name,
                    testcase_result=self.__convertResultStr(testcase.result),
                    scenario_name=scenario.elem_name,
                    scenario_result=self.__convertResultStr(scenario.result),
                    scenario_stdout=scenario.stdout,
                    scenario_duree=scenario.duree
                )
                for deployment in scenario.get_child_list('deployments'):
                    self.add_metric(
                        typeid='deployment',
                        datetime=deployment.datetime,
                        testcase_name=testcase.elem_name,
                        testcase_result=self.__convertResultStr(testcase.result),
                        scenario_name=scenario.elem_name,
                        scenario_result=self.__convertResultStr(scenario.result),
                        deployment_name=deployment.elem_name,
                        deployment_result=self.__convertResultStr(deployment.result),
                        deployment_stdout=deployment.stdout,
                        deployment_duree=deployment.duree
                    )
                verifier = scenario.get_verifier()
                if verifier is not None:
                    for verifier_name, verifier_data in list(verifier.verifier_data['verifiers'].items()):
                        self.add_metric(
                            typeid='verifiers',
                            datetime=verifier.datetime,
                            testcase_name=testcase.elem_name,
                            testcase_result=self.__convertResultStr(testcase.result),
                            scenario_name=scenario.elem_name,
                            scenario_result=self.__convertResultStr(scenario.result),
                            verifier_name=verifier_name,
                            verifier_result=self.__convertResultStr(verifier.result),
                            verifier_duree=verifier.duree
                        )
                        for verifier_test_name, testcase_content in list(verifier_data['testcases'].items()):
                            self.add_metric(
                                typeid='verifier_testcase',
                                datetime=verifier.datetime,
                                testcase_name=testcase.elem_name,
                                testcase_result=self.__convertResultStr(testcase.result),
                                scenario_name=scenario.elem_name,
                                scenario_result=self.__convertResultStr(scenario.result),
                                verifier_name=verifier_name,
                                verifier_result=self.__convertResultStr(verifier.result),
                                verifier_test_duree=testcase_content['duree'],
                                verifier_test_result=self.__convertResultStr(testcase_content['result']),
                                verifier_test_name=verifier_test_name,
                                failure_messages=[ failure['message'] for failure in testcase_content['failures'] ] if 'failures' in testcase_content is False else []
                            )

    def add_metric(self, typeid, datetime, **complement):
        metric = {
            '@timestamp': datetime.isoformat(),
            'context': self.context,
            'typeid': typeid
        }
        metric.update(complement)
        self.metrics.append(metric)

    def __convertResultStr(self, resutbool):
        if resutbool == True:
            return "OK"
        else:
            return "KO"

    def get_str(self):
        res = ""
        for metric in self.metrics:
            res += json.dumps(metric) + "\n"
        return res
