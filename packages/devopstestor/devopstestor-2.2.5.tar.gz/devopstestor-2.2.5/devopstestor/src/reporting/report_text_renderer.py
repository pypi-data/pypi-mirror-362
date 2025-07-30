from utils import prefix_lines, nested_dict_to_flat_dict_with_array
import json
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

result_color={
    True: bcolors.OKGREEN,
    False: bcolors.FAIL
}

def result2label(result):
    if result == True:
        return "OK"
    elif result == False:
        return "KO"
    else:
        return "UNKNOW"

class ReportTextRenderer():
    def __init__(self, config_global, campaign_report):
        # Regles d'affichage detaille des resultats du rapport
        # Affichage detaille si mode debug pas plus de 2 tests a afficher
        detail_testcase_ok = config_global.get('report::report_level') == 'debug' \
        or campaign_report.nb_children < 4
        res = "---------------------------------------------\n"
        res += "----------- Resultats des tests -------------\n"
        context = config_global.get_node('report').get_node('report_context').config
        if context is not None:
            for k,v in list(nested_dict_to_flat_dict_with_array(context).items()):
                res += "  - {} : {}\n".format(k, v)
        res += "---------------------------------------------\n"
        res += result_color.get(campaign_report.result) + "Campagne de test {} : {}\n".format(campaign_report.elem_name, result2label(campaign_report.result)) + bcolors.ENDC
        testcases = campaign_report.get_child_list('testcases')
        res += "  Nombre de tests case : {}\n".format(campaign_report.nb_children)
        if campaign_report.nb_children_ok > 0:
          res += bcolors.OKGREEN + "  {} test(s) sont OK soit {}% des tests{}\n".format(
            campaign_report.nb_children_ok,
            (campaign_report.nb_children_ok / campaign_report.nb_children) * 100,
            bcolors.ENDC
          )
        if campaign_report.nb_children_ko > 0:
          res += bcolors.FAIL + "  {} test(s) sont KO soit {}% des tests{}\n".format(
            campaign_report.nb_children_ko,
            (campaign_report.nb_children_ko / campaign_report.nb_children) * 100,
            bcolors.ENDC
          )
        res += "---------------------------------------------\n"
        for testcase in testcases:
            res += result_color.get(testcase.result) + "    Test cases {} : {}\n".format(testcase.elem_name, result2label(testcase.result)) + bcolors.ENDC
            if detail_testcase_ok or not testcase.result:
                if len(testcase.tags) > 0:
                    res += "      tags : \n"
                    for tag in testcase.tags:
                        res += "        - {}\n".format(tag)
                scenarios = testcase.get_child_list('scenarios')
                res += "      Nombre de scenarios : {}\n".format(len(scenarios))
                for scenario in scenarios:
                    res += "        ---\n"
                    res += result_color.get(scenario.result)
                    res += "        Scenario {} : {} \n".format(scenario.title, result2label(scenario.result))
                    if scenario.title != scenario.elem_name:
                        res += "          name : {} \n".format(scenario.elem_name)
                    res += bcolors.ENDC
                    if scenario.description is not None and scenario.description != "":
                        res += prefix_lines(scenario.description, "            ") + "\n"
                    if detail_testcase_ok or not scenario.result:
                        for deployment in scenario.get_child_list('deployments'):
                            res += "          ---\n"
                            res += result_color.get(deployment.result) + "          Deploiement : {}\n".format(result2label(deployment.result))
                            if detail_testcase_ok or not deployment.result:
                                res += "                {}\n".format(deployment.elem_name)
                                res += "                stdout: \n"
                                res += prefix_lines(deployment.stdout, "                  ") + "\n"
                                res += bcolors.ENDC

                        if scenario.get_verifier() is not None:
                            res += result_color.get(scenario.get_verifier().result) + "          Verifiers : " + result2label(scenario.get_verifier().result) + bcolors.ENDC +"\n"
                            if detail_testcase_ok or not scenario.get_verifier().result:
                                verifier_data = scenario.get_verifier().verifier_data
                                for verifier_name, verifier in list(verifier_data['verifiers'].items()):
                                    res += "            " + result_color.get(verifier['result']) + "    " + verifier_name + " : " + result2label(verifier['result']) + bcolors.ENDC + '\n'
                                    for verifier_test, testcase_content in list(verifier['testcases'].items()):
                                        res += "            " + result_color.get(testcase_content['result']) + "      - " + verifier_test + " : " + result2label(testcase_content['result']) + " \n"
                                        for failure in testcase_content['failures']:
                                            res += "                  ----- Failure : " + failure['message'] + ' ----- \n'
                                            res += prefix_lines(failure['stdout'], "                    ")
                                            res += '\n                  ------------ \n'
                                            res += bcolors.ENDC
                                        for skipped in testcase_content['skipped']:
                                            res += "                    - skipped : " + skipped + '\n'
                                        if testcase_content['stdout'] != "":
                                            res += "                    --- stdout ---\n"
                                            res += prefix_lines(testcase_content['stdout'], "                    ")
                                            res += "\n"
                                res += result_color.get(verifier_data['stats']['result'])
                                res += "              Duree: " + str(verifier_data['stats']['duree']) + "\n"
                                res += "              verifiers: " + str(verifier_data['stats']['verifiers']) + "\n"
                                res += "              verifiers_ok: " + str(verifier_data['stats']['verifiers_ok']) + "\n"
                                res += "              verifiers_ko: " + str(verifier_data['stats']['verifiers_ko']) + "\n"
                                res += "              skipped: " + str(verifier_data['stats']['skipped']) + "\n"
                                res += "              result: " + result2label(verifier_data['stats']['result']) + "\n"
                                res += bcolors.ENDC

                res += "\n"
        res += "---------------------------------------------\n"
        self.report_str = res


    def get_str(self):
        return self.report_str
