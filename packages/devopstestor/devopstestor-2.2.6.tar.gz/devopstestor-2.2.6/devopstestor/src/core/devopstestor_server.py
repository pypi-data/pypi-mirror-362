class DevopstestorServer:
    def __init__(self, client_path, **kwargs):
        # Initialisation des ressouces serveur
        from devopstestor import Devopstestor
        Devopstestor.init_path()
        import rpyc
        import json
        import sys
        # devopstestor = Devopstestor(client_path=client_path, **kwargs)
        from global_config_factory import GlobalConfigFactory
        from config import Config
        import logging

        # Declaration du service
        @rpyc.service
        class DevopstestorService(rpyc.Service):
            def __init__(self):
                self.lock = False
                self.devopstestor = Devopstestor(client_path=client_path, **kwargs)

            @rpyc.exposed
            def get_global_config(self):
                return json.dumps(self.devopstestor.global_config.config)

            @rpyc.exposed
            def get_logging(self):
                return logging

            @rpyc.exposed
            def on_disconnect(self, coco):
                print('Mr se kasse')

            @rpyc.exposed
            def start(self, stdout=None, stderr=None, global_config_overload='{}', **kwargs):
                try:
                    self.lock = True
                    if stdout is not None:
                        sys.stdout = stdout
                    if stderr is not None:
                        sys.stderr = stderr
                    self.devopstestor.start(
                        global_config_overload=json.loads(global_config_overload), **kwargs
                    )
                except Exception as e:
                    print(f"Exception ! {e}")
                except KeyboardInterrupt as e:
                    print(f'Une exception KeyboardInterrupt a ete levee {e}')
                finally:
                    if stdout is not None:
                        sys.stdout = sys.__stdout__
                    if stderr is not None:
                        sys.stderr = sys.__stderr__
                    self.lock = False

        # Demarrage du serveur en exposant le service "DevopstestorService"
        from rpyc.utils.server import ThreadedServer
        t = ThreadedServer(DevopstestorService, port=18861)
        t.start()
