from abstract_report import AbstractReport
class TestcaseReport(AbstractReport):
    """
    Rapport de la campagne de test
    """
    def __init__(self, name, tags):
        super(TestcaseReport, self).__init__(name)
        self.tags = tags
    def add_scenario(self, scenario):
        """
        Ajoute un rapport de scenario
        """
        self.add_child_to_list('scenarios', scenario)

    def get_scenarios(self):
        """
        Retourne la liste des rapports de scenarios
        """
        return self.get_child_list('scenarios')
