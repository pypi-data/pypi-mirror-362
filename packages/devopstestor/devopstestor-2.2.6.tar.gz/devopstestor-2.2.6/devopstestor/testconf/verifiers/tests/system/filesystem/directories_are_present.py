from context_fixtures import scenario_context, argument_getter

def test_directories_are_present(host, argument_getter):
    """
    Verification de la presence des dossiers
    """
    directories_arg = argument_getter.get_arg('directories_are_present')
    for directory_path, directory_check in directories_arg.items():
        assert host.file(directory_path).exists, "Le dossier {} doit exister".format(directory_path)
        odirectory = host.file(directory_path)
        assert odirectory.is_directory, "{} n'est pas un dossier".format(directory_path)
        if 'mode' in directory_check:
            assert oct(odirectory.mode) == '0o{}'.format(directory_check['mode']), "Le dossier {} doit avoir les droits {}".format(directory_path, directory_check['mode'])
        if 'user' in directory_check:
            assert odirectory.user == directory_check['user'], "Le dossier {} avoir comme proprietaire {}".format(directory_path, directory_check['user'])
        if 'group' in directory_check:
            assert odirectory.group == directory_check['group'], "Le dossier {} avoir comme groupe {}".format(directory_path, directory_check['group'])
        if 'nb_childs' in directory_check:
            assert len(odirectory.listdir()) == directory_check['nb_childs'], "Le dossier {} doit contenir {} elements".format(directory_path, directory_check['nb_childs'])
        if 'listdir' in directory_check:
            assert odirectory.listdir() == directory_check['nb_childs'], "Le dossier {} doit contenir les elements {}".format(directory_path, directory_check['listdir'])
