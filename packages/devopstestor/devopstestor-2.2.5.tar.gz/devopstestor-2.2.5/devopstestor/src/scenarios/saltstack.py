def initialise_context(machine_provisionner, init_contexte, pillar, **kwarg):
    # Reinitialise les pillars a partir des donnes fournis pas le testcase
    statut, stdout = machine_provisionner.set_pillars(init_contexte, merge=False)
    if statut == False: # Cas d'erreur
        return statut, stdout # inutils de continuer le scenario

    # Ajout des pillars specifiques
    return machine_provisionner.set_pillars(pillar)

# @deprecated
def appliquer_etats(machine_provisionner, init_contexte={}, sls_cible=None, saltenv=None, pillar={}, **kwarg):
    statut, stdout = initialise_context(machine_provisionner, init_contexte, pillar)
    # Ajout du role
    if statut == False: # Cas d'erreur
        return statut, stdout # inutils de continuer le scenario

    # Lancement du deploiement
    statut, stdout = machine_provisionner.runStateApply(
        saltenv=saltenv,
        sls_cible=sls_cible
    )

    return statut, stdout


def call_module(minion_provisionner, module_name, module_args=[], module_kwargs={}, salt_args=[], init_contexte={}, pillar={}, **kwarg):
    statut, stdout = initialise_context(minion_provisionner, init_contexte, pillar)
    # Ajout du role
    if statut == False: # Cas d'erreur
        return statut, stdout # inutils de continuer le scenario
    res, out = minion_provisionner.call_module(module_name=module_name, module_args=module_args, module_kwargs=module_kwargs, salt_args=salt_args)
    return res, f"call_module {module_name}\n module_args:{module_args}\n module_kwargs:{module_kwargs}\n salt_args: {salt_args}\n ---\n {out}"
