from context_fixtures import scenario_context, argument_getter

def test_files_are_present(host, argument_getter):
    """
    Verification de la presence des fichiers
    """
    files_arg = argument_getter.get_arg('files_are_present')
    for file_path, file_check in files_arg.items():
        assert host.file(file_path).exists, "Le fichier {} doit exister".format(file_path)
        ofile = host.file(file_path)
        assert ofile.is_file, "{} n'est pas un fichier".format(file_path)
        if 'mode' in file_check:
            assert oct(ofile.mode) == '0o{}'.format(file_check['mode']), "Le fichier {} doit avoir les droits {}".format(file_path, file_check['mode'])
        if 'user' in file_check:
            assert ofile.user == file_check['user'], "Le fichier {} avoir comme proprietaire {}".format(file_path, file_check['user'])
        if 'uid' in file_check:
            assert ofile.uid == file_check['uid'], "Le fichier {} avoir comme uid proprietaire {}".format(file_path, file_check['uid'])
        if 'group' in file_check:
            assert ofile.group == file_check['group'], "Le fichier {} avoir comme groupe {}".format(file_path, file_check['group'])
        if 'gid' in file_check:
            assert ofile.gid == file_check['gid'], "Le fichier {} avoir comme gid {}".format(file_path, file_check['gid'])
        if 'contains_pattern' in file_check:
            assert ofile.contains(file_check['contains_pattern']), "Le fichier {} doit contenir le pattern {}".format(file_path, file_check['contains_pattern'])
