from abstract_report import AbstractReport
class CampaignReport(AbstractReport):
    """
    Rapport de la campagne de test
    """
    def add_testcase(self, testcase):
        """
        Ajoute un rapport de testcase
        """
        self.add_child_to_list('testcases', testcase)

    def get_testcases(self):
        """
        Retourne la liste des rapports de testcases
        """
        return self.get_child_list('testcases')
