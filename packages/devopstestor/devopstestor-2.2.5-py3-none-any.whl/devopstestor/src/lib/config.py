
from utils import flat_dict_to_nested_dict_with_array, nested_dict_to_flat_dict_with_array
import copy

class Config():

    @staticmethod
    def create_from_dict(dict):
        """
        Cree une instance de config a partir d'un dict

        :param dict: dictionnaire a transformer en Config
        :return: instance de Config avec les donnes du dictionnaire
        """
        conf = Config()
        conf.config = copy.deepcopy(dict)
        conf.flat_config = nested_dict_to_flat_dict_with_array(separator='::', input=dict)
        return conf

    @staticmethod
    def create_from_flat_dict(flat_dict):
        """
        Cree une instance de config a partir d'un dict plat
        :param flat_dict: dictionnaire plat a transformer en Config
        :return: instance de Config avec les donnes du dictionnaire
        """
        conf = Config()
        conf.flat_config = flat_dict
        conf.config = flat_dict_to_nested_dict_with_array(separator='::', flat_dict=flat_dict)
        return conf


    def __init__(self):
        """
        Constructeur
        """
        self.config = {}
        self.flat_config = {}

    def exist(self, name):
        """
        retourne True si le parametre exist, False sinon
        """
        # Recherche si feuille
        if name in self.flat_config:
            return True
        # Recherche si noeud intermediaire
        for key, val in list(self.config.items()):
            if name in key:
                return True

        return False

    def get(self, name, default="valeur_par_defaut"):
        """
        Retourne la valeur de la cle
        Si inexistante la valeur par defaut si existante sinon exception
        """
        if default == "valeur_par_defaut" and not self.exist(name):
            raise Exception(f"config error : required param {name} not exist !",)
        return self.flat_config.get(name, default)

    def get_node(self, node_name):
        """
        Retourne une config a un nouveau noeud
        Si inexistante la valeur par defaut si existante sinon exception
        """
        node = self.config.get(node_name, None)
        if node == None:
            raise Exception(f"config error : node {node_name} not exist !")
        return Config.create_from_dict(node)

    def clone(self):
        return Config.create_from_dict(self.config)

    def items(self):
        """
        Permet d'iterer sur le noeud
        """
        return list(self.config.items())

    def set(self, name, value, force=False):
        """
        Set value to config
        """
        if not force and not self.exist(name):
            raise Exception(f"Config error, cannot change config {name} : not exist")
        self.flat_config[name] = value
        self.config = flat_dict_to_nested_dict_with_array(self.flat_config, separator="::")
