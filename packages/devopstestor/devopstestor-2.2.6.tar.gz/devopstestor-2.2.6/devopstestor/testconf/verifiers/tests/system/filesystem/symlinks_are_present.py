from context_fixtures import scenario_context, argument_getter

def test_symlinks_are_present(host, argument_getter):
    """
    Verification de la presence des liens symboliques
    """
    symlink_args = argument_getter.get_arg('symlinks_are_present')
    for symlink_path, symlink_checks in symlink_args.items():
        assert host.file(symlink_path).exists, "Le lien symbolique {} doit exister".format(symlink_path)
        ofile = host.file(symlink_path)
        assert ofile.is_symlink, "{} doit etre un lien symbolique".format(symlink_path)
        if 'user' in symlink_checks:
            assert ofile.user == symlink_checks['user'], "Le lien symbolique {} avoir comme proprietaire {}".format(symlink_path, symlink_checks['user'])
        if 'group' in symlink_checks:
            assert ofile.group == symlink_checks['group'], "Le lien symbolique {} avoir comme groupe {}".format(symlink_path, symlink_checks['group'])
        if 'linked_to' in symlink_checks:
            assert ofile.linked_to == symlink_checks['linked_to'], "Le lien symbolique {} doit pointer sur {}".format(symlink_path, symlink_checks['linked_to'])
