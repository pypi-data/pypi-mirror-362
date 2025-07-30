import time
from datetime import datetime
from log_manager import logging
log = logging.getLogger('scenario.devopstestor')

def do_nothing(machine_provisionner, init_contexte, **kwarg):
    """
    Ne fait rien
    """
    return True, "Nothing is done"


def log_in_file(machine_provisionner, init_contexte, log, **kwarg):
    mc = machine_provisionner.get_machine_controller()
    ret, out = mc.append_in_file('{} - {} - {}'.format(datetime.now().isoformat(), mc.machine_name, log), '/tmp/log.txt')
    return True, out
