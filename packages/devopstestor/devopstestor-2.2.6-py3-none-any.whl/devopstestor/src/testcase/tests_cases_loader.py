from utils import copy_merge_recursive_dict
from test_case import TestCase
from log_manager import logging
log = logging.getLogger('core.TestCaseLoader')
import re
import yaml
import os

class TestCaseLoader():
    def __init__(self, global_config):
        self.test_case_config = global_config.get_node('testcase')
        self.test_cases_files = self.test_case_config.get_node('test_cases_files')
        self.test_case_base_path = list(self.test_case_config.get('base_path'))
        expected_kind = self.test_case_config.config.get('kinds', ['testcase-undefined'])
        self.common_conf = {}
        self.test_cases = []
        re_filtre = re.compile("^{}$".format(global_config.get('testcase::filtre_regex')))
        # Chargement des configs communes
        if self.test_cases_files.exist('common_config'):
            for cf_path in self.test_cases_files.get_node('common_config').config:
                i = 0
                config_patth_pattern = '{}/{}'
                while i < len(self.test_case_base_path) and not os.path.exists(config_patth_pattern.format(self.test_case_base_path[i], cf_path)):
                    i +=1
                if i >= len(self.test_case_base_path):
                    log.warn('testcase conf dir not found {}'.format(cf_path))
                else:
                    common_config = yaml.load(open('{}/{}'.format(self.test_case_base_path[i], cf_path)), Loader=yaml.Loader)

                    # Les configs sont merges sucessivements dans l'ordre
                    self.common_conf = copy_merge_recursive_dict(
                        defaut=self.common_conf,
                        source=common_config
                    )
        list_test_case = []
        for test_case_base_path in self.test_case_base_path:
            for root, dirs, files in os.walk(test_case_base_path):
                for file in files:
                    if file.endswith(".yaml") and file.startswith('testauto_'):
                         abs_path = os.path.join(root, file)
                         relpath = abs_path.replace(test_case_base_path+'/', '')
                         list_test_case.append({
                            'relpath': relpath,
                            'abs_path': abs_path
                         })

        # Chargement des tests cases
        for tc in list_test_case:
            tc_name = tc['relpath'].replace('/', '.').replace('.yml', '').replace('.yaml', '')
            if re_filtre.match(tc_name):
                # Les configs sont merges sucessivements avec la config global
                try:
                    test_case = yaml.load(open(tc['abs_path']), Loader=yaml.Loader)
                    tc_kind = test_case.get('kind', "testcase-undefined")
                    if tc_kind not in expected_kind:
                        log.info(f'Testcase skiped {tc["relpath"]}, bad kind : {tc_kind} ')
                    else:
                        self.test_cases.append(
                            # TODO check testcase classname dans conf
                            TestCase(
                                global_config=global_config,
                                config_path=tc['abs_path'],
                                name=tc_name,
                                test_case_conf=copy_merge_recursive_dict(
                                    defaut=self.common_conf,
                                    source=test_case
                                )
                            )
                        )
                except Exception as e:
                    log.error(f'Impossible de charger le testcase {tc["relpath"]}')
                    raise e


    def get_test_cases(self):
        return self.test_cases
