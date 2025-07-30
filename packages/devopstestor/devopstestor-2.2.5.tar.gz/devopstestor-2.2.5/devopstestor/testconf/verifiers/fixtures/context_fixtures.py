"""
Fixtures saltstack
"""
import pytest
import json
from datetime import datetime
from devopstestor.src.lib.utils import nested_dict_to_flat_dict_with_array

@pytest.fixture()
def scenario_context():
    """
    Permet de recuperer le context du scenario (nom, arguments)
    """
    res = json.load(open('/tmp/verifiers_context.json'))

    # convert timestamp to datetime
    time_context = res['scenario']['time_context']
    format = "%Y-%m-%d %H:%M:%S.%f"
    time_context['start_time'] = datetime.strptime(time_context['start_time'], format)
    time_context['end_time'] = datetime.strptime(time_context['end_time'], format)
    return res

@pytest.fixture()
def time_context(scenario_context):
    return scenario_context['scenario']['time_context']

class AgumentGetter:
    def __init__(self, context_data):
        self.dict_args = context_data.get('scenario', {}).get('args', {})
        self.flat_args = nested_dict_to_flat_dict_with_array(input=self.dict_args)

    def get_arg_leaf(self, arg_name, defaultVal=None):
        if arg_name not in self.flat_args:
            if defaultVal is None:
                pytest.skip('Argument manquant {}'.format(arg_name))
            else:
                return defaultVal
        return self.flat_args[arg_name]

    def get_arg(self, arg_name, defaultVal=None):
        if arg_name not in self.dict_args:
            if defaultVal is None:
                pytest.skip('Argument manquant {}'.format(arg_name))
            else:
                return defaultVal
        return self.dict_args[arg_name]

@pytest.fixture()
def argument_getter(scenario_context):
    argg = AgumentGetter(scenario_context)
    return argg
