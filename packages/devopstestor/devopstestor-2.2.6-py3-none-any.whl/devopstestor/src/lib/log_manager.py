# -*- coding: utf-8 -*-
'''
Meilleure gestion des logs
'''
import logging
import json
import time
import threading

class LogManager(logging.Logger):

    def __init__(self, name="def", level=logging.NOTSET):
        self.context_thread = {}
        super(LogManager, self).__init__(name, level)

    def get_cur_context(self):
        threadid = threading.current_thread().name
        if not threadid in self.context_thread:
            self.context_thread[threadid] = {
                "context_list": [threadid],
                "contextes_stack": {}
            }

        return self.context_thread[threadid]
    def get_context_list(self):
        return self.get_cur_context()['context_list']
    def get_contextes_stack(self):
        return self.get_cur_context()['contextes_stack']

    def format_msg(self, msg, **complement):
        return "{} : {} - {}".format('.'.join(self.get_context_list()), msg, json.dumps(complement))

    # Modification du rendu du message des methodes classiques
    def debug(self, msg, *args, **complement):
        return super(LogManager, self).debug(msg=self.format_msg(msg, **complement))

    def info(self, msg, *args, **complement):
        return super(LogManager, self).info(msg=self.format_msg(msg, **complement))

    def warning(self, msg, *args, **complement):
        return super(LogManager, self).warning(msg=self.format_msg(msg, **complement))

    def error(self, msg, *args, **complement):
        return super(LogManager, self).error(msg=self.format_msg(msg, **complement))

    # Ajout de methodes contextuelles
    def debut(self, context_name, msg="", *args, **complement):
        if msg == "":
            msg = "Debut de {}".format(context_name)

        # Sauvegarde de la duree
        if not context_name in self.get_contextes_stack():
            self.get_contextes_stack()[context_name] = []
        self.get_contextes_stack()[context_name].append(time.time())
        self.get_context_list().append(context_name)

        self.debug(msg, *args, **complement)

    def fin(self, context_name, msg="", *args, **complement):

        if msg == "":
            msg = "Fin de {}".format(context_name)

        # Calcul de la duree du contexte
        complement['duree'] = -1
        if context_name in self.get_contextes_stack():
            complement['duree'] = round(time.time() - self.get_contextes_stack()[context_name].pop(), 4)

        self.info(msg, *args, **complement)

        if context_name in self.get_contextes_stack():
            self.get_context_list().pop()


logging.setLoggerClass(LogManager)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s ', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
