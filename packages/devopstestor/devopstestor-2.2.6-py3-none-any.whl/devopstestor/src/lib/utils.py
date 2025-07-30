import copy
import datetime
import json
import yaml
import re
import os

### Utils to parse env var in yaml file #### 
path_matcher = re.compile(r'.*\$\{([^}^{]+)\}.*')
def path_constructor(loader, node):
    return os.path.expandvars(node.value)

class EnvVarLoader(yaml.SafeLoader):
    pass

EnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
EnvVarLoader.add_constructor('!path', path_constructor)



def nested_dict_to_flat_dict_with_array(input, separator=".", path="", preserve_array=True, preserve_datetime=False):

    """
        Converti les dictionnaires d'une arborscence en dictionnaire plat.
        Cette fonction preserve ou pas les list

        :param input: L'elemenent a traiter.
        :type input: dict/list/string/int/..

        :param separator: Le delimiter entre les clefs du dictionnaire.
        :type separator: string

        :param path: La clef du dictionaire plat du niveau (variable interne).
        :type path: string

        :param preserve_array: Indique si les tableau doivent subir le traitement
        :type preserve_array: boolean

        :Example:
        >>> nested_dict_to_flat_dict(input = {'keyA' : {'keyB' : 'value'}}, nested_dict_child={})
        {'keyA.keyB' : 'value'}

    """
    if isinstance(input, dict): # Cas dictionnaire : chaque sous element est extrait
        res = {}
        for name, val in list(input.items()):
            basepath = "{}{}".format(path, name)
            if preserve_datetime is True and isinstance(val, dict) and val.get('__type__', '') == 'datetime.datetime':
                # Cas particulier des dict correspondant a des type (ex )
                child = datetime.datetime(*val['args']).isoformat()
                # child = {name: val}
            else:
                child = nested_dict_to_flat_dict_with_array(input=val, separator=separator, path="{}{}".format(basepath, separator), preserve_array=preserve_array)
            if isinstance(child, dict):
                res.update(child) # Si l'element est un dict on merge
            else:
                res[basepath] = child # Sinon on l'ajoute
        return res
    elif isinstance(input, (list, tuple)): # Traitement particulier des tableaux
        if preserve_array:
            res = list(input)
        else:
            res = {}
        for i, valtab in enumerate(input):
            if preserve_array:
                res[i] = nested_dict_to_flat_dict_with_array(input=valtab, separator=separator, path='', preserve_array=preserve_array) # le path repart de 0
            else:
                basepath = "{}{}".format(path, i)
                child = nested_dict_to_flat_dict_with_array(input=valtab, separator=separator, path="{}{}".format(basepath, separator), preserve_array=preserve_array) # Le path continu
                if isinstance(child, dict):
                    res.update(child) # Si l'element est un dict on merge
                else:
                    res[basepath] = child # Sinon on l'ajoute
        return res
    else: # Cas feuille (string, int, ...)
        return input # on retourne l'element

    return None

def flat_dict_to_nested_dict_with_array(flat_dict, separator='.'):
    '''
        Converti un dictionnaire plat en dictionnaire imbrique.
                Cette fonction gere les list preserves
        :param flat_dict: Le dictionnaire a traiter.
        :type flat_dict: dict

        :param separator: La clef du dictionaire plat.
        :type separator: string

        :return: Le dictionnaire imbrique.
        :rtype: dict

        :Example:
        >>> dict_to_nested_dict(flat_dict = {'keyA.keyB' : 'value'}, separator='.')
        {'keyA' : {'keyB' : 'value'}},

    '''

    nested_dict = {}
    for key, value in flat_dict.items():
        keys = key.split(separator)
        previous_key = nested_dict
        key_split_length = len(keys)
        for i in range(0, key_split_length):
            key = keys[i]
            if i == key_split_length - 1:
                if isinstance(value, dict):
                    previous_key[key] = flat_dict_to_nested_dict_with_array(value, separator)
                elif isinstance(value, (list, tuple)): # Traitement des list
                    previous_key[key] = list(value)
                    for i, array_val in enumerate(value):
                        if isinstance(array_val, dict):
                           previous_key[key][i] = flat_dict_to_nested_dict_with_array(array_val, separator)
                        else:
                           previous_key[key][i] = array_val
                else: # feuille
                    if isinstance(previous_key, (list, tuple)):
                        # Cas ou la feuille est un tableau
                        previous_key.append(value)
                        key = int(key)
                        previous_key = list(set(previous_key)) # Deduplicate
                    else:
                        previous_key[key] = value
            elif key not in previous_key:
                previous_key[key] = {}
            previous_key = previous_key[key]

    return nested_dict

def recursive_merge_dict(a, b, path=None):
    """
    merges b into a with overriding
    """
    if path is None:
        path = []
    if b:
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    recursive_merge_dict(a[key], b[key], path + [str(key)])
                else:
                    a[key] = b[key]
            else:
                a[key] = b[key]
def copy_merge_recursive_list_of_dict(*sources):
    # Retourne un dictionnaire correspondant au merge de tous les dictionnaires passés en parametre
    result = {}
    for source in sources:
        if not isinstance(source, (dict, list, tuple)):
            raise TypeError('copy_merge_recursive_list_of_dict : cette fonction ne prend en parametre que des dicts')
        result = copy_merge_recursive_dict(defaut=result, source=source)
    return result

def copy_merge_recursive_dict(defaut={}, source={}, calls_number=0, replace_list=False):
    # Copie des dictionnaires pour travailler en local.
    # A fin d'eviter des problemes avec les dictionnaires source.
    if(calls_number == 0):
        defaut = copy.deepcopy(defaut)
        source = copy.deepcopy(source)
    calls_number+=1
    if not isinstance(source, dict):
        return source
    result = defaut
    for key, values in source.items():
        if key in result and isinstance(result[key], dict):
            result[key] = copy_merge_recursive_dict(defaut=result[key], source=values, calls_number=calls_number)
        elif key in result and isinstance(result[key], (list, tuple)):
            if replace_list is True:
                result[key] = values
            else:
                # recherche des doublons
                append_result = []
                for el2 in values:
                    trouve = False
                    for el1 in result[key]:
                        if is_value_egal(el2, el1):
                            trouve = True
                    if trouve is False:
                        append_result.append(el2)
                        
                result[key] = list(result[key] + append_result)
        else:
            result[key] = copy_merge_recursive_dict(defaut=values, calls_number=calls_number)

    return result

def is_value_egal(v1, v2):
    '''
    Permet de comparer recursivement les différences entre 2 variables (dict, list ou type simple)
    '''
    return json.dumps(v1) == json.dumps(v2)


def valuate_dict_with_context(dict_input, context = {}, enable_this = True):
    '''
            Peremet de remplacer dans une arborescence de dictionnaire
            les variable $(nom_variable) par leurs valeurs

            :param dict_input: arborescence de dictionnaire source
            :type dict

            :param context: arborescence de dictionnaire precisant la valeur de chaque variable
            :type dict

            :param enable_this: Ajoute une variable "this" permettant de recuperer la valeur d'autre champ du document
            :type boolean

            :return: L'arborescence du dictionnaire value
            :rtype: list

            :Example:
            dict = {
                "root": {
                    "variable1": "valeur1",
                    "variable2": "$(app.home)"
                },
                "root2": "$(this.root.variable1)"
            }
            context={
                "app": {
                    "home": "valeur home"
                }
            }
            result >>
             {
                "root": {
                    "variable1": "valeur1",
                    "variable2": "valeur home"
                },
                "root2": "valeur1"
            }
    '''
    if not isinstance(dict_input, dict):
        return dict_input

    flat_context = nested_dict_to_flat_dict_with_array(input=context, separator="::")
    dict_input = __valuate_dict_with_context_rec(dict_input, flat_context)

    if enable_this:
        # Ajout du this pour manipuler le dict courrant une fois celui-ci charge
        flat_copy = nested_dict_to_flat_dict_with_array(input=dict_input, path="this::", preserve_array=False, separator="::")
        dict_input = __valuate_dict_with_context_rec(dict_input, flat_copy)

    return dict_input

def __valuate_dict_with_context_rec(input, flat_context):
    """
        Fonction interne recursive
        retourne un dictionnaire value par les valeurs du contexte fournit en parametre
    """
    if isinstance(input, dict):
        # Traitement des dictionnaires
        res={}
        for i_dict, val_dict in list(input.items()):
            # Chaque fils est parcourus
            res[i_dict] = __valuate_dict_with_context_rec(val_dict, flat_context)
        return res
    elif isinstance(input, (list, tuple)):
        # Traitement particulier des tableaux
        res = list(input) # Initialisation du tableau de resultat
        for i, val in enumerate(input):
            res[i] = __valuate_dict_with_context_rec(val, flat_context)
        return res
    elif isinstance(input, str):
        # Arrive sur une feuille : Fin du parcours, si la valeur est une chaine les remplacements sont faits
        for i_context, val_context in list(flat_context.items()):
            if isinstance(val_context, str):
                input = str.replace(input, '$({})'.format(i_context), val_context)
        return input

    return input # Arrive ici signifit : arrive sur une feuille qui n'est pas une chaine : aucun traitement



def grep(input, motif, size_before=0, size_after=0, reverse=False):
    lines = input.split('\n')
    nb = len(lines)
    i = 0
    res=[]
    for l in lines:
        if (reverse == False and motif in l) or (reverse == True and motif not in l ):
            for j in range(i-size_before, i-1):
                if j>=0 and j<nb:
                    res.append(lines[j])

            res.append(lines[i])

            for j in range(i+1, i+size_after):
                if j<nb:
                    res.append(lines[j])
        i += 1
    return "\n".join(res)

def tail(string, size):
    lines = string.split('\n')
    nb = len(lines)
    res = []

    deb = nb - size
    if deb < 0:
        deb = 0
    for i in range(deb, nb-1):
        res.append(lines[i])
    return "\n".join(res)

def prefix_lines(string, prefix):
    lines = string.split('\n')
    return "\n".join([prefix + l for l in lines])
