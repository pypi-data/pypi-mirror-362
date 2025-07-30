# Deprecated : utiliez services_are_up
from context_fixtures import scenario_context, argument_getter
from datetime import datetime, timedelta
import time

def test_service_is_valid(host, argument_getter):
    """
    Le service doit etre valide
    """
    service_name = argument_getter.get_arg('service_name')
    assert host.service(service_name).is_valid, "Le service {} doit etre valide".format(service_name)

def test_service_is_running(host, argument_getter):
    """
    Verification de l'etat RUNNING du service
    Attente pour verifier que le service ne crash avant la fin de `delay`
    """
    # Recuperation des parametres
    service_name = argument_getter.get_arg('service_name')

    # Premiere verification
    is_service_running = host.service(service_name).is_running, "Le service {} doit etre demarre".format(service_name)
    if is_service_running is False:
        assert is_service_running, "Le service {} doit etre demarre".format(service_name)

    # Analyse dans le temps
    delay = argument_getter.get_arg('wait_before_checkstart', 120) # Delais a attentdre pour valider le bon lancement du service

    # Recuperation de du datetime de lancement du service
    retActiveEntrerTimestamp = host.run('systemctl show {} | grep "ActiveEnterTimestamp=" | sed -e "s/ActiveEnterTimestamp=//"'.format(service_name)).stdout.replace('\n','')
    assert retActiveEntrerTimestamp != "", "Le service {} doit avoir un ActiveEnterTimestamp".format(service_name)
    activeEnterTimestamp = datetime.strptime(
        retActiveEntrerTimestamp,
        "%a %Y-%m-%d %H:%M:%S %Z"
    )
    max_test_date = activeEnterTimestamp + timedelta(seconds=delay)
    num_verif = 1
    while datetime.now() < max_test_date:
        assert host.service(service_name).is_running, "Le service {} doit etre demarre, num_verif={}".format(service_name, num_verif)
        num_verif +=1
        time.sleep(delay/5) # 5 tentatives max

def test_service_is_enabled(host, argument_getter):
    """
    Le service doit etre en automatique
    """
    service_name = argument_getter.get_arg('service_name')
    assert host.service(service_name).is_enabled, "Le service {} doit etre en automatique".format(service_name)
