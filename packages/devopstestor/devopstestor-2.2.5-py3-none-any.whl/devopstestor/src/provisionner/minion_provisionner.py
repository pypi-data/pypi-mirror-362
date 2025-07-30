from abstract_provisionner import AbstractProvisionner
from utils import copy_merge_recursive_dict
import json
import yaml
import time
from utils import grep, tail
from log_manager import logging
log = logging.getLogger('provisionner.MinionProvisionner')
class MinionProvisionner(AbstractProvisionner):
    pillar_root = '/srv/pillar-auto/testauto/testauto/'
    pillar_filepath = '/srv/pillar-auto/testauto/testauto/init.sls'
    testtop_filepath = '/srv/pillar-auto/testauto/top.sls'
    verifier_results_filepath = '/tmp/state_apply_result_salt_state.json'
    verifier_report_filepath = '/tmp/state_apply_report_salt_state.json'
    # Rapport de la campagne de test
    code_to_result = {
        0: True
    }

    def initialise(self, machine_controller, machine_name):
        self.machine_controller = machine_controller
        log.debut('MinionProvisionner-prepare', 'Initialisation du minion', machine_name=machine_name)
        ret, output = machine_controller.run_cmd('/usr/bin/systemctl restart salt-master.service')
        ret, output = machine_controller.run_cmd('/usr/bin/systemctl restart salt-minion.service')
        ret, output = machine_controller.run_cmd('/usr/bin/salt-run saltutil.sync_all')
        ret, output = machine_controller.run_cmd('/usr/bin/salt-call saltutil.sync_all')
        ret, output = machine_controller.run_cmd('/usr/bin/salt-run saltutil.sync_all')

        # Creation du fichier pillar temporaire
        self.machine_controller.run_cmd('mkdir -p {}'.format(self.pillar_root))
        if not self.global_config.get('machine::resume_machine'):
            self.set_pillars(pillar={}, merge=False) # Reinit pillar
        self.machine_controller.put_in_file('{"testauto":{"*":["testauto"]}}', self.testtop_filepath) # Reinit top.slssalt
        log.fin('MinionProvisionner-prepare', 'Initialisation du minion', machine_name=machine_name)

    def set_pillars(self, pillar, merge=True):
        '''
        Parametre les pillar du minion

        :param pillar: Pillar a setter
        :param merge: si actif, le pillar passe en parametre est merge avec celui deja present sur la machine
        :return: code retour
        '''
        if merge:
            ret, output = self.machine_controller.get_file_content(file_path=self.pillar_filepath)
            if ret == 0 and output != '':
                pillar_existant = json.loads(output)
                pillar = copy_merge_recursive_dict(defaut=pillar_existant, source=pillar)

        ret, output = self.machine_controller.put_in_file(
            content=json.dumps(pillar),
            file_path=self.pillar_filepath
        )
        result_bool = self.code_to_result.get(ret, False)
        if result_bool == False:
            output = "Impossible de definir le pillar"
        return result_bool, output
    
    ####################################################################################   
    def call_module(self, module_name:str, module_args=[], module_kwargs={}, salt_args=[]):
        '''
        Allow to call salt module
        '''        
        args_str = " ".join(module_args)
        kwargs_str = " ".join([ f"n=\"{v}\"" for n,v in module_kwargs.items() ])
        salt_args_str = " ".join([f'--{arg}' for arg in salt_args ])
        return self.run_salt_cmd(f'salt-call {module_name} {args_str} {kwargs_str} {salt_args_str}')
    
    ####################################################################################

    def run_salt_cmd(self, command):
        '''
        Lance une commande sur le minion.
        '''
        result, output = self.machine_controller.run_cmd(command)
        self.clean_log(output)

        return self.code_to_result.get(result, False), grep(output, "DEBUG", reverse=True)

    def filtre_non_json_elem(self, json_el, non_json=''):     
        # Find first '{' (ignore output non json elements)
        if json_el[0] == '{':
            return json_el, non_json
        
        # move  line if non json
        json_el_lines = json_el.split('\n')
        return self.filtre_non_json_elem('\n'.join(json_el_lines[1:]), '\n' + json_el[0])

    def runStateApply(self, sls_cible=None, saltenv=None, pillar={}):
        '''
        Lance un state apply

        :param saltenv: environment salten
        :type saltenv: string

        :param pillar: pillar a passer au state apply
        :type pillar: dict
        '''
        sls_cible = sls_cible if sls_cible else ''
        env = 'saltenv='+saltenv if saltenv else ''
        pillar = "pillar='"+json.dumps(pillar)+"'" if pillar else ''
        log_level = self.global_config.get('provisionner::log_level')
        # Nettoyage logs
        ret, output = self.machine_controller.run_cmd('rm -f /var/log/salt/minion')

        result_bool = False
        ret, salt_stdout = self.run_salt_cmd(
            'salt-call state.apply {} {} {} -l quiet --log-file-level {} --retcode-passthrough  queue=True --out=json'.format(sls_cible, env, pillar, log_level)
        )
        output = ""
        # Recuperation des logs
        _, output_log = self.machine_controller.get_file_content(file_path='/var/log/salt/minion')
        self.clean_log(output_log)

        # Nouveau rapport yaml
        try:
            salt_stdout, salt_stdout_nonjson = self.filtre_non_json_elem(salt_stdout)
            log.debug('parse stdout ' + salt_stdout)
            saltresult = json.loads(salt_stdout)
            rapport = {
                "total": 0,
                "succeeded": 0,
                "changed": 0,
                "failed": 0,
                "skipped": 0,
                "duration": 0
            }
            states_in_report = {}
            for id, state in saltresult['local'].items():
                rapport['total'] += 1
                rapport['duration'] += state['duration']
                if state['result'] is True:
                    rapport['succeeded'] += 1
                    if state['changes'] != {}:
                        rapport['changed'] += 1
                elif state['result'] is False:
                    rapport['failed'] += 1
                else:
                    rapport['skipped'] += 1

                if log_level == "debug" or state['result'] is False or state['changes'] != {}:
                    # Ajout du state en entier dans le rapport
                    states_in_report[id] = state

            output = "Resultats :\n"
            output += salt_stdout_nonjson
            result_bool = rapport['total'] == rapport['succeeded'] + rapport['skipped']
            for id, sr in states_in_report.items():
                etat = "ERROR" if sr['result'] is False else "Changed" if sr['changes'] != {} else ""
                if sr['result'] is False or ( etat == "Changed" and rapport['failed'] == 0):
                    output += "\n"
                    output += id + '   ' + etat + '\n--\n'
                    output += yaml.dump(sr)
                    output += "\n----------\n"
            output += yaml.dump(rapport)
            # Enregistrement du rapport pour donner acces aux verifiers
            self.machine_controller.put_in_file(json.dumps(saltresult), self.verifier_results_filepath)
            self.machine_controller.put_in_file(json.dumps(rapport), self.verifier_report_filepath)
        except Exception as e:
            output += f"Rapport ilisible: {e}\n"
            if result_bool == True:
                output += tail(salt_stdout, 7)
                output += traceback.format_exc()
            elif len(salt_stdout) > 10000:
                output += grep(salt_stdout, 'Result: False', 6, 15)
            elif len(output) == 0:
                output += grep(salt_stdout, 'failed', 4, 15)
            else:                    
                output += salt_stdout

        return result_bool, output

    def setGrains(self, grains):
        '''
        Permet de definir des grains sur un minion
        :param grains: valeur des grains a set
        :type: dict
        :example:{
            'roles': None,
            'network':{
                'production': 23.23.23.23,
                'localhost': 0.0.0.0
            }
        }
        '''
        return self.run_salt_cmd('salt-call --local grains.setvals "'+json.dumps(grains)+'"')

    def getGrains(self, key=None):
        '''
        Permet d'obtenir les grains presentes sur le minion
        '''
        command = (
            'python -c "'
            'import salt.config;'
            'import salt.loader;'
            '__opts__ = salt.config.minion_config(\'/etc/salt/minion\');'
            '__grains__ = salt.loader.grains(__opts__);'
            'print(__grains__)"'
        )
        _, grains_str = self.run_salt_cmd(command)
        try:
            grains = ast.literal_eval(grains_str)
        except SyntaxError as error:
            log.warning('Erreur lors du parsing des grains: ' + str(error))
            grains = None
        output = grains.get(key) if key else grains
        log.debug('Grains found: ' + str(ret))
        return result, output

    def grains_append(self, key, val):
        return self.run_salt_cmd('salt-call --local grains.append {} "{}"'.format(key, val))

    def grains_remove(self, key, val):
        return self.run_salt_cmd('salt-call --local grains.remove {} "{}"'.format(key, val))

    def clean_log(self, output, level=logging.INFO):
        '''
        Permet de logger le stdout/stderr du conteneur proprement
        TODO ameliorer qualite de log
        '''
        log_lines = output.split('\n')
        for log_to_print in log_lines:
            if 'ERROR' in log_to_print:
                log.error(log_to_print.rstrip().replace("[ERROR   ]", ''))
            elif 'DEBUG' in log_to_print:
                log.debug(log_to_print.rstrip().replace("[DEBUG   ]", ''))
            elif 'INFO' in log_to_print:
                log.info(log_to_print.rstrip().replace("[INFO    ]", ''))
            else:
                log.log(level, log_to_print)
