from abstract_provisionner import AbstractProvisionner
from log_manager import logging
log = logging.getLogger('provisionner.LogstashProvisionner')
import os
import yaml
import time
from glob import glob


############# Params #############
config_input_dir='/etc/logstash_in'
config_mock_dir='/usr/share/logstash/config'

verifiers_logstash_out_filepath='/tmp/logstash_test.out'
config_mock_io = """
input{
  http{
    codec => "json"
    port => 5044
    ecs_compatibility => disabled
  }
}
output{
  file{
    codec => "json_lines"
    enable_metric => false
    ecs_compatibility => disabled
    path => "/tmp/logstash_test.out"
    file_mode => 0777
  }
}
"""
################## Recursive internal functions #########
def find_block_start(strtab: list, indice = 0) -> str:
  if indice >= len(strtab):
    return "\n"

  sline = strtab[indice].replace(' ', '') 
  res = ''
  if 'input{' in sline or 'output{' in sline:
      print('Find block in or out')
      indice = find_end_of_block(strtab, indice+1) + 1
  else:
    res = strtab[indice]    

  return  res + f'\n{find_block_start(strtab, indice+1)}' 



def find_end_of_block(strtab: list, indice: int, nb_block = 0):

  # Si on trouve la fin ou si on arrive a la fin on retourne l'indice
  if indice >= len(strtab) and '}' in strtab[indice]:
    return indice

  nb_block += strtab[indice].count('{')
  nb_block -= strtab[indice].count('}') 
  
  if indice >= len(strtab) or nb_block == 0:
    return indice

  # TODO voir si < 0  
  
  return find_end_of_block(strtab, indice+1, nb_block )
  


def delete_output_from_file(file_content):  
  res = find_block_start(strtab=file_content.split('\n'))
  return res

################## Class Provisionner ###################
class LogstashProvisionner(AbstractProvisionner):

    ########### Initialisation du provisionner ###########
    def initialise(self, machine_controller, machine_name):
        self.machine_controller = machine_controller
        self.env = self.global_config.get_node('machine').get_node('env')

    ########### Lancement de logstash ###############
    def test_config(self, **others):
        """
        Lancement oneshot afin de tester la configuration fournie
        """
        arguments= [
            "--node.name logstashtestconf",
            "--log.level info",
            "--config.debug",
            "--config.test_and_exit",
            "--path.data /tmp",
            "--path.logs /tmp",
            "--path.settings " + config_input_dir 
        ]
        username = others.get('run_as', 'root')

        # Lancement Logstash
        ret, out = self.machine_controller.run_cmd(
            "su -l {} -c '{} {}'".format(
                username,
                self.env.get('logstash::bin_path'),
                " ".join(arguments)
            )
        )

        # Interpretation resultats
        result = True if ret == 0  else False
        return result, out

    def mock_logstash_io(self):
        """
        Cette fonction cree un mock de la configuration montee sur la VM dans /etc/logstash_in vers le repertoire de travail de logstash
        Le mock supprime toute les "input" et "output" de la configuration logstash pour la remplacer par les input/output permettant de communiquer avec les testsauto
        """

        # cleanup old execution
        ret, out = self.machine_controller.run_cmd(f'rm -rf {config_mock_dir}')
        ret, out = self.machine_controller.run_cmd(f'cp -r {config_input_dir} {config_mock_dir}')

        # Find config files
        list_config_files=[] # file to inspect for mock

        pipeline_path = os.path.join(config_input_dir, 'pipelines.yml')
        ret, pipeline_yaml_content = self.machine_controller.get_file_content(pipeline_path)

        if str(ret) == '0':
            for conf in yaml.safe_load(pipeline_yaml_content):
                ret, list_glob = self.machine_controller.run_cmd('sh -c "ls {}"'.format(conf['path.config'].replace(config_mock_dir, config_input_dir))) # resolv glob path

                if str(ret) == '0':
                   log.warn(f"logstash pipeline.yml path resolution error : {conf['path.config']}")
                else:
                  list_config_files += list_glob.split('\n')
        
        
        logstashyaml_path = os.path.join(config_input_dir, 'logstash.yml')
        ret, logstashyaml_path_content = self.machine_controller.get_file_content(logstashyaml_path)

        if str(ret) == '0':
            pc = yaml.safe_load(logstashyaml_path_content)['path.config']
            ret, list_glob = self.machine_controller.run_cmd('sh -c "ls {}"'.format(pc.replace(config_mock_dir, config_input_dir))) # resolv glob path

            if str(ret) != '0':
              log.warn(f"logstash logstash.yml path resolution error : {pc}")
            else:
              list_config_files += list_glob.split('\n')

        list_config_files = set(list_config_files) # Dedoublonnage
        log.info('Mock file ' + str(list_config_files))
        # Compute file
        first = True
        for fpath in list_config_files:
            if fpath != "":
              input_path = fpath
              ret, config_file_content = self.machine_controller.get_file_content(input_path)
              if str(ret) != "0":
                return False, "Le fichier f{input_path} mentionne dans le pipeline.yml n'existe pas !"
              new_content = delete_output_from_file(config_file_content)             
              out_path = fpath.replace(config_input_dir, config_mock_dir)
              # Add mock on first config file
              if first:
                  first = False
                  new_content += '\n' + config_mock_io
              ret, config_file_content = self.machine_controller.put_in_file(new_content, out_path, makedir=True)
              if str(ret) != '0':
                return False, "Erreur lors de l'ecriture dans le fichier f{out_path}"
        
        # Wait for logstash refresh conf
        time.sleep(10)


        return True, "Mock OK" 
           

    def initialise_mock_output_file(self):
        # RAZ logstash output and wait for logstash to prevent connection refused before starting verifier (send log + verify result)
        ret, out = self.machine_controller.run_cmd(f"touch {verifiers_logstash_out_filepath}")
        ret, out = self.machine_controller.run_cmd(f"chmod 777 {verifiers_logstash_out_filepath}")
        time.sleep(10)
        return str(ret) != '0', out
