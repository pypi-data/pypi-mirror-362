from abstract_provisionner import AbstractProvisionner
from utils import grep, tail
from log_manager import logging
from os import path
import time

log = logging.getLogger('provisionner.SystemDProvisionner')


class SystemdProvisionner(AbstractProvisionner):

    def create_service(self, service_name, User, Group, ExecStart, composant_name=None):
        """
        Cree un service
        """
        if composant_name is None:
            composant_name = service_name

        if len(ExecStart) > 400: # Si la commande est trop longue on passe par un fichier de lancement
            launcher_path =  "/usr/local/bin/{}".format(service_name)
            ret, out = self.machine_controller.put_in_file(
                content="#!/bin/bash\n" \
                        "echo 'Lancement du service'\n" \
                        "{}\n" \
                        "echo 'Arret du service'\n".format(ExecStart),
                file_path="{}".format(launcher_path)
            )
            ret, out = self.machine_controller.run_cmd(
                "chmod +x {}".format(launcher_path)
            )
            ExecStart = launcher_path

        ret, out = self.machine_controller.put_in_file(
            content="[Unit] \n" \
                    "Description={}\n" \
                    "[Service]\n" \
                    "Type=simple\n" \
                    "User={}\n" \
                    "Group={}\n" \
                    "ExecStart={}\n" \
                    "Restart=always\n" \
                    "WorkingDirectory=/tmp\n" \
                    "Nice=19\n" \
                    "LimitNOFILE=16384\n" \
                    "TimeoutStopSec=infinity\n" \
                    "[Install]\n" \
                    "WantedBy=multi-user.target\n".format(composant_name, User, Group, ExecStart, User),
            file_path="/etc/systemd/system/{}.service".format(service_name)
        )
        if ret != 0:
            return False, out
        ret, out = self.machine_controller.run_cmd("chmod 644 /etc/systemd/system/{}.service".format(service_name))
        if ret != 0:
            return False, out
        ret, out = self.machine_controller.run_cmd("systemctl daemon-reload")
        if ret != 0:
            return False, out
        ret, out = self.machine_controller.run_cmd("systemctl enable {}".format(service_name))
        return True if ret == 0 else False, out

    def create_service_from_install(self, composant_name, service_name):
        package_name = self.get_last_package_name(composant_name)
        for systemdext in ['service', 'timer']:
            systemd_service_file_path = "/liv/{}/systemd/{}_template.{}".format(package_name, composant_name, systemdext)

            is_file_exist, service_content = self.machine_controller.run_cmd("cat {}".format(systemd_service_file_path))
            if str(is_file_exist) != "0":
                return False, "Aucun fichier service n'est a copier"

            ret, out = self.machine_controller.run_cmd(
                "cp {} /etc/systemd/system/{}.{}".format(systemd_service_file_path, service_name, systemdext))
            if ret != 0:
                return False, out
            ret, out = self.machine_controller.run_cmd("chmod 644 /etc/systemd/system/{}.{}".format(service_name, systemdext))
            if ret != 0:
                return False, out
        ret, out = self.machine_controller.run_cmd("systemctl daemon-reload")
        if ret != 0:
            return False, out
        ret, out = self.machine_controller.run_cmd("systemctl enable {}".format(service_name))

        return True if ret == 0 else False, "------------ /etc/systemd/system/{}.{} ------------\n{}".format(
            service_name, systemdext, service_content)

    def service_control(self, service_name, action):
        """
        Action sur le service vua la commande systemctl
        """
        ret, out = self.machine_controller.run_cmd(
            "systemctl {} {}".format(action, service_name)
        )
        # Interpretation resultats
        result = True if ret == 0 else False
        journalctl_out = ""
        if result is False:
            ret, journalctl_out = self.machine_controller.run_cmd("journalctl -xe")
        return result, "{}\n--\n{}".format(out, grep(
            input=journalctl_out,
            motif="Unit {}".format(service_name),
            size_before=0,
            size_after=50))
