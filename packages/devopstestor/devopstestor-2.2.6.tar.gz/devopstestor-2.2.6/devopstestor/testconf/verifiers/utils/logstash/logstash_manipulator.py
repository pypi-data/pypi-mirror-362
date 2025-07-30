import logging
import http.server
import http.client, urllib.parse
import json
import time
import os

import socketserver
last_logstash_result = None
class LogstashManipulator:
    def __init__(self):
        self.setup()

    def setup(self, logstash_host="127.0.0.1", logstash_in_port=1234, logstash_out_filepath=2345, logstash_api_port=9600, request_content_type="text/plain"):
        """
        Initialisation
        """
        self.logstash_host = logstash_host
        self.logstash_in_port = logstash_in_port
        self.logstash_out_filepath = logstash_out_filepath
        self.logstash_api_port = logstash_api_port
        self.request_content_type = request_content_type
        self.reponse_timeout = 30 # 30 sec
        self.mutex = False

    def setup_from_context(self, scenario_context):
        print('-------------------------------------')
        print(scenario_context)
        print('-------------------------------------')
        scenario_args = scenario_context.get('scenario').get('args').get('init_contexte')
        self.setup(
            logstash_host=scenario_args.get('logstash_input_http_host', '127.0.0.1'),
            logstash_in_port=int(scenario_args.get('logstash_input_http_port')),
            logstash_out_filepath=str(scenario_args.get('verifiers_logstash_out_filepath', scenario_args.get('logstash_out_filepath'))),
            logstash_api_port=int(scenario_args.get('logstash_api_port', 9600)),
            request_content_type=scenario_args.get('request_content_type', "text/plain")
        )

    def get_computed_message(self, message, custom_headers = None):
        """
        Retourne le message traite par logstash
        """
        self._purge_last_result()
        self._push_message_to_logstash(message=message, custom_headers=custom_headers)
        result = self._logstash_message_shift()

        return result

    def get_instance_status(self):
        return self.get_api_result()['status']

    def get_api_result(self, retry=15):
        try:
            conn = http.client.HTTPConnection("{}:{}".format(self.logstash_host, self.logstash_api_port))

            conn.request("GET", "")
            response = conn.getresponse()
            logging.info(response.status, response.reason)
            data = response.read()
            if response.status != 200:
                raise Exception("Erreur de communication avec Logstash")
            return json.loads(data)
        except Exception as e:
            print(e)
            if retry > 0:
                print('----- Retry : {}:{}'.format(self.logstash_host, self.logstash_api_port))
                time.sleep(10)
                return self.get_api_result(retry - 1)
            else:
                raise Exception("Erreur de communication avec Logstash")

    def _push_message_to_logstash(self, message, custom_headers=None):
        """
        Envoi un message a logstash via input HTTP
        """
        self._wait_for_mutex()
        headers = {
            "Content-type": self.request_content_type,
            "Accept": "text/plain"
        }
        if isinstance(message, (dict,list,tuple)):
            # Conversion des message structure en json
            message = json.dumps(message)
            headers['Content-type'] = "application/json"

        if custom_headers is not None:
            for k, v in custom_headers.items():
                headers[k] = v
        nb_tentative = 15
        status = None
        while nb_tentative > 0 and status != 200:
            try:
                print('Tentative de connexion')
                conn = http.client.HTTPConnection("{}:{}".format(self.logstash_host, self.logstash_in_port))
                conn.request("POST", "", message, headers)
                response = conn.getresponse()
                # logging.info(str(response.status), str(response.reason))
                data = response.read()
                conn.close()
                status = response.status
                if status != 200:
                    raise ConnectionResetError("Statut ko")
            except (http.client.RemoteDisconnected, ConnectionResetError):
                # Il arrive que le logstash ne reponde pas du premier coups
                # cas du mock de la config qui n'est pas encore pris en compte par logstash
                print('Erreur de connexion')
                nb_tentative -= 1
                time.sleep(5)

        if status != 200:
            raise Exception(f"Erreur de communication avec Logstash, statut={status}")
        self._release_mutex()

    def _logstash_message_shift(self):
        """
        Extrait le premier message du fichier de resultat
        """
        self._wait_for_mutex()
        print("_logstash_message_shift")

        last_logstash_result = ""
        temps_restant = int(self.reponse_timeout)
        wait_time = 5

        while last_logstash_result == "" and temps_restant > 0:
            print("Attente")
            time.sleep(wait_time)
            temps_restant -=  wait_time

            with open(self.logstash_out_filepath, 'r') as file_result:
                fc =  file_result.read()
                print(f'---------Ouverture du fichier {self.logstash_out_filepath} -----------')
                print(fc)
                print('--------------------')
                last_logstash_result = []
                for line in fc.split('\n'):
                    try:
                        last_logstash_result.append(json.loads(line) )
                    except json.decoder.JSONDecodeError:
                        pass # On ignore l'exception (pb d'espace)


        # Manipulation pour recuperer le document de logstash
        self._release_mutex()
        if last_logstash_result == "":
            raise Exception('Erreur, le resultat retourne par logstash est ""')

        return last_logstash_result
    def _purge_last_result(self):
        with open(self.logstash_out_filepath, 'w') as file_result:
            file_result.truncate(0)
    def _release_mutex(self):
        self.mutex = False

    def _wait_for_mutex(self):
        if self.mutex is True:
            raise Exception("Le mutex n'est pas relache")
        self.mutex = True
