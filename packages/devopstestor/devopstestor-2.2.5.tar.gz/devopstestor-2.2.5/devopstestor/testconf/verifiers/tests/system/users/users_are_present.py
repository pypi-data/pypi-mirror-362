from context_fixtures import scenario_context, argument_getter

def test_users_are_present(host, argument_getter):
    """
    Verification des utilisateurs presents sur la machine
    """
    users_arg = argument_getter.get_arg('users_are_present')
    for user, user_checks in users_arg.items():
        assert host.user(user).exists, "L'utilisateur {} doit exister".format(user)
        ouser = host.user(user)
        if 'uid' in user_checks:
            assert ouser.uid == user_checks['uid'], "L'utilisateur {} doit avoir l'uid {}".format(user, user_checks['uid'])
        if 'groups' in user_checks:
            ouser.groups.sort()
            user_checks['groups'].sort()
            assert ouser.groups == user_checks['groups'], "L'utilisateur {} doit avoir les groupes {}".format(user, user_checks['groups'].sort())
