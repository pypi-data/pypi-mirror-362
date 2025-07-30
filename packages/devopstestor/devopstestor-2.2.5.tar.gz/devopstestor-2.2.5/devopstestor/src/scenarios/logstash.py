import time
from log_manager import logging
from utils import tail
log = logging.getLogger('scenario.logstash')

import yaml
def mock_logstash_io(machine_provisionner, logstash_provisionner, init_contexte):
    """
    Modifie la configuration de logstash afin de la rendre compatible avec les verifiers io
    """
    res, out = logstash_provisionner.mock_logstash_io()    
    return res, tail(out, 50)

def lancer_test_io(logstash_provisionner, init_contexte):
    """
    Affiche le contexte et ne fait rien (les verifications sont geres par les verifieurs)
    """
    # Initialisation et changement des droits du fichier de sorti
    logstash_provisionner.initialise_mock_output_file()

    return True, yaml.dump(init_contexte['test_messages']['input_message'])

def tester_config(machine_provisionner, logstash_provisionner, init_contexte, **provisionner_params):
    """
    Utilise le binaire logstash dans le but de valider la structure de la configuration
    """
    # Start logstash in test mode
    return logstash_provisionner.test_config(**provisionner_params)
