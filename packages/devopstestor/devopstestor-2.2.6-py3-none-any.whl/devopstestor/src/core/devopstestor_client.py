class DevopstestorClient:
    def __init__(self, **kwargs):
        # Initialisation des ressouces serveur
        import rpyc
        import json
        import sys
        from devopstestor import Devopstestor
        Devopstestor.init_path()
        from global_config_factory import GlobalConfigFactory
        from config import Config
        c = rpyc.connect('localhost', 18861, config={"allow_public_attrs": True, "sync_request_timeout": None})
        try:

            global_config = Config.create_from_dict(json.loads(c.root.get_global_config()))
            GlobalConfigFactory.compute_args(global_config=global_config, function_args=kwargs)

            # ._config['sync_request_timeout'] = None
            # c.root.start(stdout=sys.stdout, stderr=sys.stderr, global_config_overload=json.dumps(global_config.config), **kwargs)
            res = c.root.start(stdout=sys.stdout, global_config_overload=json.dumps(global_config.config), **kwargs)
            # c.root.start(global_config_overload=json.dumps(global_config.config), **kwargs)
            # async_start = rpyc.async_(c.root.start)
            # async_start(global_config_overload=json.dumps(global_config.config), **kwargs)
        except Exception as e:
            print(f'Une exception a ete levee {e}')
        except KeyboardInterrupt as e:
            print(f'Une exception KeyboardInterrupt a ete levee {e}')
        finally:
            # c.root.on_disconnect(c)
            c.close()
