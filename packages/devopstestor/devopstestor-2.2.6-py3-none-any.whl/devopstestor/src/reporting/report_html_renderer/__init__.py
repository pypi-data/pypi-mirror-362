import yaml
import os
from jinja2 import Environment, FileSystemLoader
import sys

class ReportHtmlRenderer():
    """
    Class permettant de generer un rapport HTML
    """
    def __init__(self, config_global, campaign_report):
        """
        Genere le rapport

        :param global_config: accesseur aux donnes de configuration
        :param campaign_report: donnes du rapport
        """
        self.report_str = ""

        THIS_DIR = os.path.dirname(os.path.abspath(__file__))

        mon_env = Environment(
            loader=FileSystemLoader(THIS_DIR),
            trim_blocks=True
        )

        ## Filtres jinja utiles ##
        def format_date(datetime):
            return datetime.strftime("%d/%m/%y %H:%M")
        def result_to_text(result):
            if result == True:
                return "<span style='color:green;'>Sucess</span>"
            elif result == False:
                return "<span style='color:red;'>Failed</span>"
            return "<span style='color:grey;'>Unknow</span>"

        mon_env.filters['result_to_text'] = result_to_text
        mon_env.filters['format_date'] = format_date

        # Interpretation via template jinja
        self.report_str = mon_env.get_template("./html_template.html.jinja").render(
            config_global=config_global,
            campaign_report=campaign_report
        )

    def get_str(self):
        """
        :return rendu du rapport (string)
        """
        return self.report_str
