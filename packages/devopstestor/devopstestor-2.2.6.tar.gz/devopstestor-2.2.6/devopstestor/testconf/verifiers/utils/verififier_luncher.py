import sys, os, json, pytest
import xml.etree.ElementTree as ET

def find_verifier_name(verifiers_names, end_of_key):
    for cle, _ in list(verifiers_names.items()):
        if cle.endswith(end_of_key):
            return cle
    return "cle_testcase_introuvable" # cle par defaut

def parse_junit_verifiers_report(verifiers_targets, file_path, verifieur_not_found):
    """
    Transforme un rapport junit xml un dictionnaire exploitable dans le rapport et dans le contexte
    """
    # Initialisation du rapport avec les verifierus non trouves
    report = {
        'stats':{
            'verifiers': len(verifiers_targets),
            'verifiers_ok': 0,
            'verifiers_ko': len(verifieur_not_found),
            'skipped': 0,
            'duree': 0.0,
            'result': True
        },
        'verifiers': { verifieur_name: { 'result': True, 'testcases': {} } for verifieur_name in verifiers_targets + ["cle_testcase_introuvable"]}
    }

    # Extraction du resultat du rapport junit.xml
    for testsuite in ET.parse(file_path).getroot():
        nb_ko = int(testsuite.attrib['failures']) + int(testsuite.attrib['errors'])
        report['stats']['verifiers_ko'] += nb_ko
        report['stats']['verifiers_ok'] += int(testsuite.attrib['tests']) - nb_ko
        report['stats']['skipped'] += int(testsuite.attrib['skipped'])
        report['stats']['duree'] += float(testsuite.attrib['time'])
        report['stats']['result'] = nb_ko == 0

        for testcase in testsuite:
            test_function_res = {
                "result": True,
                "duree": float(testcase.attrib['time']),
                "failures": [],
                "stdout": "",
                "skipped": []
            }

            # Parcours des failure et sys-out du testcase
            for child in testcase:
                if child.tag == "failure" or child.tag == "error":
                    test_function_res['result'] = False # Si une faillure, la testfunction est KO et le verifieur est KO
                    test_function_res['failures'].append({
                        "message" : child.attrib['message'],
                        "stdout": child.text
                    })
                elif child.tag == "system-out":
                    test_function_res['stdout'] += child.text + "\n\n"
                elif child.tag == "skipped":
                    test_function_res['skipped'].append(child.attrib['message'])

            # Recherche de la cle correspondante au verifieur du rapport junit pour faire la jointure (filename -> verifier.name)
            cle_name = find_verifier_name(report['verifiers'], testcase.attrib['classname'])

            if test_function_res['result'] is False:
                # Si une testfunction est KO, le verifieur est KO
                report['verifiers'][cle_name]['result'] = False
            report['verifiers'][cle_name]['testcases'][testcase.attrib['name'].replace("[local]","")] = test_function_res

    # Clean cle_testcase_introuvable si vide
    if len(report.get('verifiers',{}).get('cle_testcase_introuvable',{}).get('testcases')) == 0:
        del report['verifiers']['cle_testcase_introuvable']
    return report

if __name__ == "__main__":
    # from deveopsteor.log_manager import logging
    # log = logging.getLogger('verifiers')
    params = json.loads(sys.argv[1])

    verifiers_basepaths = params['verifiers_paths']
    verifiers_targets = params['verifiers_targets']
    fixtures_path = params['fixtures_path']
    utils_path = params['utils_path']
    junit_tmp_report_path = '/tmp/junit_verifier_report.xml'
    context_report_path = params['report_path']

    # log.debut('verifier_luncher', verifiers_basepaths=verifiers_basepaths, verifiers_targets=verifiers_targets)

    # Recherche des verifiers
    verifieur_not_found = {}
    verifiers_paths = []
    for tgt in verifiers_targets:
        test_relpath = tgt.replace('.', '/') + '.py'
        for vpath in verifiers_basepaths:
            test_path = os.path.join(vpath, test_relpath)
            if os.path.exists(test_path):
                verifiers_paths.append(test_path)
                break
            else:
                verifieur_not_found[tgt] = {
                    'path_error': test_path,
                    'failures': ['verifier not found'],
                    "result": False
                }

    # Add fixtures and utils path
    sys.path += fixtures_path + utils_path

    # Lancement des verifiers
    ret = pytest.main(verifiers_paths + ['--junitxml', junit_tmp_report_path])

    # Recuperation du rapport d'execution des verifieurs
    resut_report = parse_junit_verifiers_report(verifiers_targets, junit_tmp_report_path, verifieur_not_found)

    # Enregistrement du rapport en yaml
    with open(context_report_path, "w+") as f:
        f.write(json.dumps(resut_report))

    # log.fin('verifier_luncher','fin des verifiers', verifiers_targets=verifiers_targets)

    sys.exit(ret)
