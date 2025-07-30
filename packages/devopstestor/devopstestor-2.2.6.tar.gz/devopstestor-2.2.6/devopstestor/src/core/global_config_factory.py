
from core_utils import get_global_path
from glob import glob
import os
from log_manager import logging
log = logging.getLogger('core.GlobalConfigLoader')
from pathlib import Path
import yaml
import argparse
from utils import flat_dict_to_nested_dict_with_array, nested_dict_to_flat_dict_with_array, copy_merge_recursive_dict, valuate_dict_with_context, EnvVarLoader
from config import Config
import json

class GlobalConfigFactory():
    """
        Parse les arguments selon la configuration recuperee
    """
    @staticmethod
    def compute_args(global_config, function_args={}):
        """
        Charge et merge les fichiers de configurations
        :param global_config: Configuration global
        :param main_args: dict d'arguments comme defini dans la configuration "arguments::parameters"
        :return: la configuration merge (meme objet que argument global_config)
        """

        def bool(value):
            return value == 'True' or value == 'true'

        def str_list(value):
            return value.replace('  ', '').replace(' ,', ',').replace(', ', ',').split(',')

        def str_json(value):
            return json.loads(value)

        arg_type = {
            'str': str,
            'int': int,
            'bool': bool,
            'str_list': str_list,
            'str_json': str_json
        }

        parser = argparse.ArgumentParser(description=global_config.config.get('arguments').get('title'))
        arguments = list(global_config.config.get('arguments').get('parameters').items())
        for name, arg in arguments:
            argument_key = '-{}'.format(name)
            if len(name) > 1:
                argument_key = '--{}'.format(name)
            if arg.get('type') == 'store_true' or arg.get('type') == 'store_false':
                parser.add_argument(argument_key, action=arg.get('type'), help=arg.get('help', ''))
            else:
                parser.add_argument(argument_key, type=arg_type.get(arg.get('type'), str), help=arg.get('help', ''))
        args = parser.parse_args()
        # Valuation de la config par les arguments
        # La valeur des arguments surcharge la config
        for name, arg in arguments:
            # Recuperations des valeurs dans ArgumentParser et dans les arguments function_args
            for val in [getattr(args, name), function_args.get(name)]:
                if not val is None:
                    log.debug(name + ' detecte en argument', val=val)
                    if isinstance(val, dict):
                        # Gestion des valeurs de type dict
                        # On considere le dict comme un ensemble de sous valeurs
                        # Ceci permet de merger le dict passe en arg avec le dict present dans la config
                        nval = nested_dict_to_flat_dict_with_array(separator='::', input=val)
                        for k,v in list(nval.items()):
                            cle_config = "{}::{}".format(arg['config_name'], k)
                            global_config.flat_config[cle_config] = v
                    else:
                        # Gestion des valeurs de type simple
                        global_config.flat_config[arg['config_name']] = val
        """
            Recalcul du neested dict de la config global
        """
        global_config.config = flat_dict_to_nested_dict_with_array(separator='::', flat_dict=global_config.flat_config)
        return global_config


    """
    Recherche et charge les differents elements contribuant a la configuration global
    """
    @staticmethod
    def load_global_config(lib_path, client_path, base_config=Config(), global_config_overload={}, main_args={}):
        """
        Charge et merge les fichiers de configurations
        :param lib_path: chemin global vers les sources du framwork
        :param client_path: chemin global vers le dossier de surcharge spcifique
        :param global_config_overload: dict de surcharge de la configuration global
        :param main_args: dict d'arguments comme defini dans la configuration "arguments::parameters"
        :return: un objet Config avec tous les elements
        """
        base_config = base_config.clone()
        base_config.set('lib_path', lib_path, force=True)
        base_config.set('client_path', client_path, force=True)

        log.debut('Chargement des configurations')
        env_conf_dir_params = [get_global_path(global_config=base_config, in_path=lpath) for lpath in os.environ['DEVOPSTESTOR_OTHER_CONF_DIRS'].split(':')] if os.getenv('DEVOPSTESTOR_OTHER_CONF_DIRS', '') != '' else []
        for path in [os.path.join(lib_path, 'config'), os.path.join(client_path, 'config')] + env_conf_dir_params:
            for file in os.listdir(path):
                file_path = path + "/" + file
                node_name = Path(file).stem
                if node_name in base_config.config:
                    # La config cote lib sert de valeur par defaut
                    base_config.config[node_name] = copy_merge_recursive_dict(defaut=base_config.config[node_name], source=yaml.load(open(file_path), Loader=EnvVarLoader))
                else:
                    base_config.config[node_name] = yaml.load(open(file_path), Loader=EnvVarLoader)

        """
           Ajout parametres calcules
        """
        base_config.config['lib_path'] = lib_path
        base_config.config['client_path'] = client_path
        base_config.config['client_name'] = os.path.basename(client_path)

        base_config.flat_config = nested_dict_to_flat_dict_with_array(separator='::', input=base_config.config)
        """
           Surcharge par ligne de commande
        """
        GlobalConfigFactory.compute_args(global_config=base_config, function_args=main_args)

        """
            Recalcul du neested dict de la config global
        """
        base_config.config = flat_dict_to_nested_dict_with_array(separator='::', flat_dict=base_config.flat_config)

        """
            Surcharge de la config par les emplacements annexe
        """
        for path in base_config.get('core::other_conf_dirs', []):
            for file in os.listdir(path):
                file_path = path + "/" + file
                node_name = Path(file).stem
                if node_name in base_config.config:
                    # La config cote lib sert de valeur par defaut
                    base_config.config[node_name] = copy_merge_recursive_dict(defaut=base_config.config[node_name], source=yaml.load(open(file_path), Loader=EnvVarLoader))
                else:
                    base_config.config[node_name] = yaml.load(open(file_path), Loader=EnvVarLoader)

        """
            Surcharge par le dictionnaire de config (passe au main())
        """
        base_config.config = copy_merge_recursive_dict(defaut=base_config.config, source=global_config_overload)

        """
            Valuation des variables presents dans la configuration
        """
        base_config.config = valuate_dict_with_context(
            dict_input=base_config.config,
            context=base_config.config
        )

        """
            Calcul de chemins absolu
        """
        list_paths = []
        for lpath in list(set(base_config.get_node('testcase').get_node('base_path').config)):
            list_paths += glob(lpath)
        netlist = []
        for lpath in list_paths:
            lgpath = str(lpath)
            if not os.path.isabs(lgpath):
                lgpath = os.path.join(os.getcwd(), lpath)
                if not os.path.exists(lgpath):
                    lgpath = os.path.join(base_config.config['client_path'], lpath)
                    if not os.path.exists(lgpath):
                        lgpath = os.path.join(base_config.config['lib_path'], lpath)
                        if not os.path.exists(lgpath):
                            log.warn("Chemin testcase {} introuvable".format(lpath))
            netlist.append(os.path.abspath(lgpath))

        if len(netlist) == 0:
            raise Exception("Aucun chemin testcase n'existe dans {}".format(','.join(list_paths)))
        base_config.config['testcase']['base_path'] = netlist

        """
            Calcul du flat dict correspondant a la config dict
        """
        base_config.flat_config = nested_dict_to_flat_dict_with_array(separator='::', input=base_config.config)

        log.fin('Chargement des configurations')

        return base_config
