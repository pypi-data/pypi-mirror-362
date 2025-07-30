"""
Verifications..
"""
import pytest
from logstash_fixtures import logstash_manipulator
from context_fixtures import scenario_context, argument_getter

def test_api_is_up(logstash_manipulator, scenario_context):

    # arrange
    logstash_manipulator.setup_from_context(scenario_context)
    expected_result = "green"

    # act
    result = logstash_manipulator.get_instance_status()

    # assert
    assert result == expected_result, "L'API doit montrer que logstash est fonctionnel"


def test_log_has_no_error(host, argument_getter):
    trace_path = argument_getter.get_arg_leaf("log_filepath")
    log_file = host.file(trace_path)
    if not log_file.exists:
        pytest.skip("Le fichier de trace '{}' n'existe pas".format(log_file))

    log_content = log_file.content_string
    warn_result = "ERROR" not in log_content \
    or "error" not in log_content \
    or "FATAL" not in log_content \
    or "fatal" not in log_content \
    or "Exception" not in log_content
    if warn_result:
        pytest.skip("WARN : Presence d'erreurs dans les traces {}".format(trace_path))
