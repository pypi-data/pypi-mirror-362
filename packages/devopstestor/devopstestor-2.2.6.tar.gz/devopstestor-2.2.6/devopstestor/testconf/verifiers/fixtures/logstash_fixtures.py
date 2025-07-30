"""
Fixtures utils pour les verifiers de test
"""
import pytest
from logstash.logstash_manipulator import LogstashManipulator

@pytest.fixture()
def logstash_manipulator():
    """
    Retourne le path du dossier contenant le lmConf.js
    """

    # TODO preconfigure with contexte
    lm = LogstashManipulator()    
    return lm
