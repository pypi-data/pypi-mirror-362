from abstract_report import AbstractReport
from utils import recursive_merge_dict

class VerifierReport(AbstractReport):
    """
    Rapport des verifiers
    """
    def __init__(self, elem_name):
        super(VerifierReport, self).__init__(elem_name)

        # Init default value
        self.verifier_data = {
            'stats':{
                'verifiers': 0,
                'verifiers_ok': 0,
                'verifiers_ko': 0,
                'skipped': 0,
                'duree': 0.0,
                'result': True
            },
            'verifiers': {},
            'stdout': ''
        }

    def set_verifiers_result(self, result, verifier_data=None):
        """
        Methode 1 : Definit les resultats du noeud (cas feuille)
        """
        if verifier_data is not None:
            # merge avec les valeurs par defaut
            recursive_merge_dict(
                self.verifier_data,
                verifier_data
            )        

        super(VerifierReport, self).set_node_result(
            result=result,
            stdout=self.verifier_data['stdout']
        )
