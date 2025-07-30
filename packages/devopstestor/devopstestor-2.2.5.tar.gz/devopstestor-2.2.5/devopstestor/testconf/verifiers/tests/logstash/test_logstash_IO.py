"""
Verifications..
"""
import datetime
import dateutil.parser
from logstash_fixtures import logstash_manipulator
from context_fixtures import scenario_context, argument_getter
from devopstestor.src.lib.utils import nested_dict_to_flat_dict_with_array
import json
import pytest


def test_messages_struct(logstash_manipulator, scenario_context, argument_getter):
    """
    Verification de la structure du message
    La structure est passe en contexte : verifiers_args.test_messages_struct
    """
    # arrange
    logstash_manipulator.setup_from_context(scenario_context)
    custom_headers = {}
    testfunction_param = argument_getter.get_arg("init_contexte").get('test_messages')
    custom_headers = testfunction_param.get('custom_headers', {})


    # Assertion general si aucune verification n'est parametree cote testcase
    if not 'expected_struct' in testfunction_param \
      and not 'expected_result' in testfunction_param \
      and not 'expected_fields' in testfunction_param \
      and not 'expected_tags' in testfunction_param:
        pytest.skip("Aucune validation (expected_struct, expected_result, expected_fields, expected_tags) n'est demande")

    # message_input = argument_getter.get_arg_leaf("init_contexte.test_messages.input_message")
    message_input = argument_getter.get_arg("init_contexte").get('test_messages').get("input_message")
    print('----- message_input -----')
    print(message_input)
    print('--------------------------')

    # Process
    message_list_out = logstash_manipulator.get_computed_message(
        message=message_input,
        custom_headers=custom_headers
    )
    print('----- message_output -----')
    print(json.dumps(message_list_out, indent=2))
    print('--------------------------')
    assert isinstance(message_list_out, (list, tuple)), "Le retour de logstash doit etre un lot de donnes"

    if len(message_list_out) != 1:
        pytest.skip(f"Le retour de Logstash ne doit comporter qu'un seul message : {len(message_list_out)}")
    message_output = message_list_out[0]

    # Verification du resultat
    flat_result = nested_dict_to_flat_dict_with_array(message_output, preserve_datetime=True)

    ################### Verification du des champs requis ###################
    if 'required_fields' in testfunction_param:
        expected_struct = testfunction_param['required_fields']
        for nom_champ in expected_struct:
            assert nom_champ in flat_result, f"Le champ {nom_champ} doit etre present en sortie de logstash"

    ################### Verification du typage des champs present ###################
    if 'expected_struct' in testfunction_param:
        expected_struct = nested_dict_to_flat_dict_with_array(testfunction_param['expected_struct'], preserve_datetime=True)
        for nom_champ, expected_type in expected_struct.items():
            if nom_champ in flat_result:
                if expected_type == "datetime":
                    ## Cas particulier du type datetime, on tente de charger la date
                    try:
                        d = dateutil.parser.isoparse(flat_result[nom_champ])
                    except ValueError:
                        assert False, f"Le champ {nom_champ} du message sortant doit etre de type datetime, le format(%Y-%m-%dT%H:%M:%S.%fZ) ne correspond pas la valeur {flat_result[nom_champ]}"
                else:
                    assert isinstance(flat_result[nom_champ], eval(expected_type)), f"Le champ {nom_champ} du message sortant doit etre de type {expected_type}, actuel {type(flat_result[nom_champ])}"

    ################### Verification de la valeur des champs present ###################
    if 'expected_result' in testfunction_param:
        expected_result = nested_dict_to_flat_dict_with_array(testfunction_param['expected_result'], preserve_datetime=True)
        for nom_champ, expected_value in expected_result.items():
            if isinstance(expected_value, dict) and expected_value.get('__type__') == "datetime.datetime":
                expected_value_parse = datetime.datetime(*expected_result.get('args', []))
                result_node = dateutil.parser.isoparse(flat_result[nom_champ])
                assert expected_value_parse == result_node, f"Verification du contenu du champ {nom_champ} de type datetime : recu={flat_result[nom_champ]}<->attendu={expected_value}"
            else:
                assert nom_champ in flat_result, f"Le champ {nom_champ} doit etre present avec la valeur {expected_value} en sortie de logstash"
                assert flat_result[nom_champ] ==  expected_value,f"Verification du contenu du champ {nom_champ} : recu={flat_result[nom_champ]}<->attendu={expected_value}"


    ################### Verification du contenu des listes ###################
    if 'list_must_contain' in testfunction_param:
        for fieldname, expected_elements in testfunction_param['list_must_contain'].items():
            for elem in expected_elements:
                assert elem in message_output[fieldname], f"\"{elem}\" doit etre present dans la liste {fieldname}"

    if 'list_must_not_contain' in testfunction_param:
        for fieldname, expected_elements in testfunction_param['list_must_not_contain'].items():
            for elem in expected_elements:
                assert elem not in message_output[fieldname], f"\"{elem}\" ne doit pas etre present dans la liste {fieldname}"
