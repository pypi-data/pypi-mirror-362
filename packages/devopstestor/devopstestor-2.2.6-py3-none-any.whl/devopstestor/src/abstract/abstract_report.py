import datetime
class AbstractReport(object): # Premiere definition pour initialiser le type
    pass
class AbstractReport(object):
    """
    Rapport de la campagne de test
    """
    # 1 - Initialisation du rapport

    def __init__(self, elem_name:str):
        """
        Initialise le rapport

        :param elem_name: Nom de l'element
        """
        self.elem_name = elem_name
        self.is_running = True
        self.children_list = {} # dict de list de noeud enfants
        self.nb_children = -1
        self.nb_children_ok = -1
        self.nb_children_ko = -1
        self.result = None
        self.result = None
        self.datetime = datetime.datetime.now()
        self.stdout = ""

    def add_child_to_list(self, name:str, child:AbstractReport):
        """
        Ajoute un sous element

        :param name: Nom de la list d'elements
        :param child: Rapport fils a ajouter
        """
        self.__check_is_running()
        if not name in self.children_list:
            self.children_list[name] = []
        self.children_list[name].append(child)

    def get_child_list(self, name:str) -> dict:
        """
        Recupere un sous element
        :param name: Nom de la list d'elements
        :return: La list d'element
        """
        return self.children_list.get(name, [])

    # 2 - Calcul du resultat

    def set_node_result(self, result:bool, stdout:str):
        """
        Methode 1 : Definit les resultats du noeud (cas feuille)
        """
        self.__compute_duree()
        self.__check_is_running()
        self.is_running = False
        self.result = result
        self.stdout = stdout

    def compute_result_bychildren(self):
        """
        Methode 2 : calcul le resultat en fonction de celui des noeuds fils
        """
        self.__check_is_running()
        self.__compute_duree()
        result = True
        self.nb_children = 0
        self.nb_children_ok = 0
        self.nb_children_ko = 0
        for child_name, child_list, in list(self.children_list.items()):
            for child_node in child_list:
                child_res = child_node.get_result()
                if child_res == True:
                    self.nb_children_ok += 1
                else:
                    self.nb_children_ko += 1
                self.nb_children += 1
                result = child_res and result
        self.result = result
        self.is_running = False

    # 3 - Recuperation du resultat

    def get_result(self) -> bool:
        """
        Recupere le resultat du noeud
        """
        self.__check_is_teminated()
        return self.result

    def get_node_stdout(self) -> str:
        """
        Retourne le resultat de la sortie standard
        """
        self.__check_is_teminated()
        return self.stdout

    ##### Private methodes #####

    def __compute_duree(self):
        self.duree = (datetime.datetime.now() - self.datetime).seconds

    def __check_is_teminated(self):
        """
        Si les tests tournent encore, une exception est levee
        """
        if self.is_running == True:
            raise Exception("Can't get result of the report {} during test running".format(self.__class__.__name__))

    def __check_is_running(self):
        """
        Si les tests ne tournent plus, une exception est levee
        """
        if self.is_running == False:
            raise Exception("Can't initialise report {} when test is finished".format(self.__class__.__name__))
