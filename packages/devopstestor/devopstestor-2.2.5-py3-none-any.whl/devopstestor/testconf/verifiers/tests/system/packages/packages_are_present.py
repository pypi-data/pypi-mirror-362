from context_fixtures import scenario_context, argument_getter

def test_packages_are_present(host, argument_getter):
    """
    Verification de la presence des packages
    """
    pkg_arg = argument_getter.get_arg('packages_are_present')
    for pkg_name, pkg_check in pkg_arg.items():
        assert host.package(pkg_name).is_installed, "Le package {} doit etre installe".format(pkg_name)
        opkg = host.package(pkg_name)
        if 'release' in pkg_check:
            assert opkg.release == pkg_check['release'], "Le package {} doit avoir la realease {}".format(pkg_name, pkg_check['release'])
        if 'version' in pkg_check:
            assert opkg.version == pkg_check['version'], "Le package {} doit avoir la version {}".format(pkg_name, pkg_check['version'])
