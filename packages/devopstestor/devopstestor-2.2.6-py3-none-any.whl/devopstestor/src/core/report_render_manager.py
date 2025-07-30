import core_utils
import os

class ReportRenderManager():
    """
    Gestionnaire de rapport des tests
    """
    def __init__(self, config_global):
        """
        Constructeur
        :param config_global: Config - Singleton d'access a la configuration global
        """
        self.config_global = config_global
        self.renders = {}


    def compute_renders(self, compte_rendu_tests):
        """
        Definition des renderers a initialiser
        :param compte_rendu_tests: CampaignReport - donnees du rapport d'execution
        """
        self.compute_render('ReportTextRenderer', compte_rendu_tests)
        self.display_report('ReportTextRenderer')

        if self.config_global.get('report::html_report_path') != False:
            self.compute_render('ReportHtmlRenderer', compte_rendu_tests)
            self.write_report_in_file(
                'ReportHtmlRenderer',
                os.path.join(
                    self.config_global.get('report::html_report_path'),
                    "render.html"
                )
            )
        if self.config_global.get('report::elk_report_path') != False:
            self.compute_render('ReportElkRenderer', compte_rendu_tests)
            self.write_report_in_file(
                'ReportElkRenderer',
                os.path.join(
                    self.config_global.get('report::elk_report_path'),
                    "testautoelk.log"
                )
            )

    def compute_render(self, render_name, compte_rendu_tests):
        """
        Initialisation d'un renderer
        :param render_name: str - nom du generateur de rendu a utiliser
        :param compte_rendu_tests: CampaignReport - donnees du rapport d'execution
        """
        self.renders[render_name] = getattr(__import__(core_utils.get_module_name(render_name)), render_name)(self.config_global, compte_rendu_tests)


    def display_report(self, render_name):
        """
        Affichage d'un rendu en console
        :param render_name: str - nom du generateur de rendu a utiliser
        """
        print(self.renders[render_name].get_str())

    def write_report_in_file(self, render_name, file_path):
        """
        Ecriture d'un rendu dans un fichier
        :param render_name: str - nom du generateur de rendu a utiliser
        :param file_path: str : chemin du fichier a generer
        :return:
        """
        with open(file_path, "w") as f:
            report_str = self.renders[render_name].get_str()
            f.write(report_str)
