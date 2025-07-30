import imp
import os

def get_class_name(module_name):
    """
    Determine le nom de la classe en fonction d'un nom du module
    :param module_name: Nom du module
    :return: Nom de la classe correspondante
    """
    up_next_char = True
    result = ""
    for car in module_name:
        if up_next_char:
            car = car.upper()
            up_next_char = False
        else:
            car = car.lower()

        if car == "_":
            up_next_char = True
        else:
            result += car

    return result

def get_module_name(class_name):
    """
    Determine le nom du module en fonction d'un nom de class
    :param class_name: Nom de la class
    :return: Nom du module correspondant
    """
    result = ""
    for car in class_name:
        if car.isupper():
            result += "_"
        result += car
    return  result[1:].lower() # Suppression du 1er tirer

def import_class(class_name):
    """
    Retourne l'objet class souhaite importe selon les regles de nommages
    :param class_name: nom de la class
    :return: Class correspondante
    """
    return getattr(__import__(get_module_name(class_name)), class_name)

def instance_object(class_name, **args):
    """
    Instancie la classe dont le nom est passe en parametre
    :param class_name: Nom de la classe a instancier
    :param args: arguments a passer au constructeur
    :return: instance de la classe correspondante
    """
    return getattr(__import__(get_module_name(class_name)), class_name)(**args)

def get_global_path(global_config, in_path):
    """
    Recherche un fichier ou dossier
    :param global_config: instance de configuration global
    :param in_path: chemin a convertir
    :return: chemin absolu si existant
    """
    if os.path.isabs(in_path) and os.path.exists(in_path):
        return in_path  # Le chemin existe deja, il est absolu
    rel_base_paths = [
        os.getcwd(),
        global_config.get('client_path'), 
        global_config.get('lib_path')
    ] + global_config.get('core::other_conf_dirs') +  global_config.get('testcase::base_path')
    for base_path in rel_base_paths:
        test_path = os.path.join(base_path, in_path)
        if os.path.exists(test_path):
            return test_path
    raise Exception('file {} not found'.format(in_path))

def import_py_file(global_config, relative_path):
    """
    Importe un fichier python selon son chemin relatif
    Le fichier est d'abords recuperer cote client, puis cote framwork
    :param global_config: instance de configuration global
    :param relative_path: chemin relatif du fichier a importer
    :return: import
    """
    return imp.load_source(relative_path, get_global_path(global_config, os.path.join("src", relative_path)))
