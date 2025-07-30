from context_fixtures import scenario_context, argument_getter

def test_service_is_valid(host, argument_getter):
    service_name = argument_getter.get_arg('service_name')
    assert host.service(service_name).is_valid, "Le service {} doit etre valide".format(service_name)

def test_service_is_enabled(host, argument_getter):
    service_name = argument_getter.get_arg('service_name')
    assert host.service(service_name).is_enabled, "Le service {} doit etre actif".format(service_name)

def test_service_is_down(host, argument_getter):
    service_name = argument_getter.get_arg('service_name')
    assert not host.service(service_name).is_running, "Le service {} doit etre arrete".format(service_name)
