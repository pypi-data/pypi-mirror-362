from context_fixtures import scenario_context, argument_getter, time_context
from datetime import datetime, timedelta
import time

def test_services_are_valid(host, argument_getter):
    """
    Le service doit etre valide
    """
    services_are_up = argument_getter.get_arg('services_are_up')
    for service_name, service_checks in services_are_up.items():
        if not 'skip_check_validity' in service_checks or service_checks['skip_check_validity'] is False:
            assert host.service(service_name).is_valid, "Le service {} doit etre valide".format(service_name)

def test_services_are_running(host, argument_getter, time_context):
    """
    Verification de l'etat RUNNING du service
    Attente pour verifier que le service ne crash avant la fin de `delay`
    """
    # Recuperation des parametres
    services_are_up = argument_getter.get_arg('services_are_up')

    for service_name, service_checks in services_are_up.items():
        # Premiere verification
        is_service_running = host.service(service_name).is_running, "Le service {} doit etre demarre".format(service_name)
        if is_service_running is False:
            assert is_service_running, "Le service {} doit etre demarre".format(service_name)

        # Analyse dans le temps
        delay = service_checks.get('wait_before_checkstart', 50) # Delais a attentdre pour valider le bon lancement du service

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
        if 'started_since' in service_checks:
            if service_checks['started_since'] == 'before':
                assert max_test_date < time_context['start_time'], f"le service {service_name} doit etre demarre avant l'execution du scenario"
            elif service_checks['started_since'] == 'onstep':
                assert max_test_date >= time_context['start_time'], f"le service {service_name} doit avoir ete demarre par le scenario"
            else:
                assert False, 'started_since arg value invalid, valeurs attendues : before, onstep'

def test_services_are_enabled(host, argument_getter):
    """
    Le service doit etre en automatique
    """
    services_are_up = argument_getter.get_arg('services_are_up')
    for service_name, service_checks in services_are_up.items():
        if 'enable' in service_checks:
            assert host.service(service_name).is_enabled == service_checks['enable'], "Le service {} doit etre configure avec enable={}".format(service_name, service_checks['enable'])
