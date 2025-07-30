"""
Scenario permettant la mise en place de differents mock sur la machine cible
"""
from utils import grep, copy_merge_recursive_dict, flat_dict_to_nested_dict_with_array, nested_dict_to_flat_dict_with_array
import yaml
import json

def delete_conf_line(machine_provisionner, init_contexte, file_path, motifs):
    mc = machine_provisionner.get_machine_controller()
    ret, file_content = mc.get_file_content(file_path=file_path)
    if str(ret) != '0':
        return False, "Le fichier {} n'a pu etre ouvert".format(file_path)

    # Remplacement du contenu
    new_file_content = str(file_content)
    deleted_line = ""
    for motif in motifs:
        deleted_line += "delete line -> " + grep(new_file_content, motif=motif, size_before=0, size_after=0, reverse=False) + "\n"
        new_file_content = grep(new_file_content, motif=motif, size_before=0, size_after=0, reverse=True)

    # Sauvegarde du fichier original
    ret, out = mc.run_cmd(command="cp {} {}.original".format(file_path,file_path))
    if str(ret) != '0':
        return False, "Impossible de sauvegarder le fichier original"

    # Depot du nouveau fichier
    ret, file_content = mc.put_in_file(content=new_file_content, file_path=file_path)
    if str(ret) != '0':
        return False, "Impossible de deposer le nouveau fichier"
    return True, deleted_line

def set_file_content(machine_provisionner, init_contexte, file_path, content, user=None, group=None, chmod=None):
    mc = machine_provisionner.get_machine_controller()
    ret, res = mc.put_in_file(content=str(content), file_path=file_path)
    if str(ret) != '0':
        return False, "Impossible remplir le fichier"

    if user is not None:
        mc.run_cmd('chown {} {}'.format(user, file_path))
    if group is not None:
        mc.run_cmd('chgrp {} {}'.format(group, file_path))
    if chmod is not None:
        mc.run_cmd('chmod {} {}'.format(chmod, file_path))

    return True, res

def replace_in_file(machine_provisionner, init_contexte, file_path, search, replace, file_out_path=None):
    mc = machine_provisionner.get_machine_controller()
    ret, file_content = mc.get_file_content(file_path=file_path)
    if str(ret) != '0':
        return False, "Impossible d'ouvrir le fichier"

    content = str(file_content).replace(search, replace)
    if file_out_path is None:
        file_out_path = file_path
    ret, res = mc.put_in_file(content=str(content), file_path=file_out_path)
    if str(ret) != '0':
        return False, "Impossible remplir le fichier"

    return True, res

def append_in_file(machine_provisionner, init_contexte, file_path, content, user=None, group=None, chmod=None):
    mc = machine_provisionner.get_machine_controller()
    ret, res = mc.append_in_file(content=str(content), file_path=file_path)
    if str(ret) != '0':
        return False, "Impossible remplir le fichier"

    if user is not None:
        mc.run_cmd('chown {} {}'.format(user, file_path))
    if group is not None:
        mc.run_cmd('chgrp {} {}'.format(group, file_path))
    if chmod is not None:
        mc.run_cmd('chmod {} {}'.format(chmod, file_path))

    return True, res

def delete_path(machine_provisionner, init_contexte, path):
    mc = machine_provisionner.get_machine_controller()
    ret, res = mc.run_cmd('rm -rf {}'.format(path.replace(' ', '\ ')))
    return str(ret) == '0', res

def delete_paths(machine_provisionner, init_contexte, paths):
    rescat = ""
    for path in paths:
        ret, res = delete_path(machine_provisionner, init_contexte, path)
        rescat += "\n " + res
        if ret is False:
            return False, rescat
    return True,rescat

def override_yaml_file(machine_provisionner, init_contexte, file_path, override_content, user=None, group=None, chmod=None):
    """
    Remplace le contenu d'un fichier au format yaml par surcharge
    """
    mc = machine_provisionner.get_machine_controller()
    ret, file_content = mc.get_file_content(file_path=file_path)
    if str(ret) != '0':
        return False, "Le fichier {} n'a pu etre ouvert".format(file_path)

    content = yaml.load(file_content, Loader=yaml.FullLoader)
    newcontent = copy_merge_recursive_dict(defaut=content, source=override_content)
    return set_file_content(machine_provisionner, init_contexte, file_path, yaml.dump(newcontent), user, group, chmod)

def delete_node_in_yaml_file(machine_provisionner, init_contexte, file_path, node_paths =[], user=None, group=None, chmod=None):
    """
    Supprime des noeuds dans un fichier au format yaml
    """
    mc = machine_provisionner.get_machine_controller()
    ret, file_content = mc.get_file_content(file_path=file_path)
    if str(ret) != '0':
        return False, "Le fichier {} n'a pu etre ouvert".format(file_path)

    flat_content = nested_dict_to_flat_dict_with_array(
        yaml.load(file_content, Loader=yaml.FullLoader)
    )
    flat_copy = dict(flat_content)
    for kdel in node_paths:
        for k,v in flat_content.items():
            if k[0:len(kdel)] == kdel:
                del flat_copy[k]

    return set_file_content(machine_provisionner, init_contexte, file_path, yaml.dump(flat_dict_to_nested_dict_with_array(flat_copy)), user, group, chmod)

def create_http_logger(systemd_provisionner, listen_port, init_contexte, endpoints=None, logout_path="/var/log/http_logger.log", username="root"):
    """
    Creation d'un service qui trace toutes les requetes HTTP ainsi que leurs contenu dans un fichier de traces
    Le verifier http_logger propose des outils de verification des requetes recues
    """
    endpoint_arg = "-e '{}'".format(json.dumps(endpoints)) if endpoints is not None else ""

    service_name="testauto_http_logger"
    # Creation du service si inexistant
    res, out = systemd_provisionner.create_service(
        composant_name=service_name,
        service_name=service_name,
        User=username,
        Group=username,
        ExecStart="/usr/bin/python3 /srv/verifiers/generic/service/http_logger.py -p {} -o {} {}".format(
                listen_port,
                logout_path,
                endpoint_arg
            )
    )
    if res is False:
        return res, out
    # Nettoyage des resultats precedents
    systemd_provisionner.get_machine_controller().run_cmd("rm -f {}".format(logout_path))

    # Demarrage du service http logger si pas deja demarre
    return systemd_provisionner.service_control(
        service_name=service_name,
        action="start"
    )
