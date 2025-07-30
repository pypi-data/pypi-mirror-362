from abstract_report import AbstractReport
class ScenarioReport(AbstractReport):

    def __init__(self, name, title="No title", description=""):
        super(ScenarioReport, self).__init__(name)
        self.title = title
        self.description = description

    def set_verifier_report(self, verifier):
        """
        Ajoute un rapport de verifier
        """
        self.add_child_to_list('verifiers', verifier)

    def get_verifier(self):
        """
        Retourne la liste des rapports des verifiers
        """
        return self.get_child_list('verifiers')[0]

    def add_deployment(self, deployment):
        """
        Ajoute un rapport de deploiement
        """
        self.add_child_to_list('deployments', deployment)

    def get_deployments(self):
        """
        Retourne la liste des rapports de deploiement
        """
        return self.get_child_list('deployments')
