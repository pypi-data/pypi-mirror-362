"""
Verification de la bonne extraction des traces par le composant ADAA
"""
import json
from nested_diff import diff
from nested_diff.fmt import TextFormatter

from context_fixtures import scenario_context, argument_getter
def test_result_file(host, argument_getter):
    http_logger_node = argument_getter.get_arg("http_logger")
    filename = http_logger_node.get("extract_file_path")
    expected_node = http_logger_node.get("expected_content")

    res = host.file(filename)
    assert res.exists, "Fichier de resultat present"

    requests_result = [ not_empy for not_empy in res.content_string.split('\n') if not_empy != '' ]
    nb_request = len(expected_node)
    assert len(requests_result) == nb_request, "le Nombre de requete dans le fichier doit etre {}".format(nb_request)

    id = 0 # Id de correlation expected -> resultat trouve (l'ordre des resultats est primordiale)
    for requeststr in requests_result:
        req = json.loads(requeststr)
        expect_req = expected_node[id]
        if 'data' in expect_req:
            assert len(req['data']) == len(expect_req['data'])
            # Print diff 4 debug
            print(TextFormatter().format(diff(req['data'], expect_req['data'], U=False, multiline_diff_context=3)))
            assert req['data'] == expect_req['data']
        id += 1
