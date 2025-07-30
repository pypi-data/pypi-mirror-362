"""
Fixtures saltstack
"""

import pytest
import salt.client
import salt.config
import subprocess, json

@pytest.fixture()
def salt_minion():
    """
    Permet de recuperer un salt-minion ('eq commande salt-call')
    """
    opts = salt.config.minion_config('/etc/salt/minion')
    master_opts = salt.config.client_config('/etc/salt/master')
    # opts['file_client'] = 'local'
    grains = salt.loader.grains(opts)
    opts['grains'] = grains
    utils = salt.loader.utils(opts)
    salt_minion = salt.loader.minion_mods(opts, utils=utils)
    return salt_minion

@pytest.fixture()
def salt_grains(salt_minion):
    """
    Retourne l'ensemble des grains du minion
    """
    return list(salt_minion.grains.items())

@pytest.fixture()
def salt_pillars():
    """
    Coutournement pour acceder aux pillars
    L'acces aux pillars n'est en effet pas possible via le salt_minion python
    """
    # Recuperation du pillar passe en parametre du scenario si existant
    return json.loads(subprocess.check_output(['salt-call', 'pillar.items', '--output=json'])).get('local', {})

@pytest.fixture()
def salt_caller():
    """
    Permet de recuperer un client salt caller permettant d'executer la plupart des modules.
    A utiliser en cas d'erreur avec le salt_minion. Notamment KeyError: 'master_uri'.
    voir https://docs.saltstack.com/en/latest/ref/clients/index.html#salt-s-loader-interface
    """
    return salt.client.Caller()
