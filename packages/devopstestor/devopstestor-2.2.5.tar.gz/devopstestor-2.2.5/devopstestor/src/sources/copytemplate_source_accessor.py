
from abstract_source_accessor import AbstractSourceAccessor
import subprocess
import os
from log_manager import logging
logger = logging.getLogger('source.DirlinkSourceAccessor')

class CopytemplateSourceAccessor(AbstractSourceAccessor):
    """
    Permet de transformer les sources en fichiers recuperables
    La source doit pouvoir etre copie sur une machine
    La source peut contenir des variables dont la valeur est passe dans la source config
    """
    def __init__(self, name, global_config, source_config):
        """
        Recupere la source si besoin pour la rendre accessible en fichier
        """
        super(CopytemplateSourceAccessor, self).__init__(
            name=name,
            global_config=global_config,
            source_config=source_config
        )

        # Le localpath devient un repertoire intermediaire dans lequel les fichiers seront copies
        self.origin = str(self.local_path)
        self.local_path = global_config.get('core::work_directory') + "/" + name

        self.name = name
        self.readonly = source_config.get('readonly', True)

        dir_name = os.path.basename(self.origin)
        # creation du repertoire temporaire
        cmd = [
            'mkdir',
            '-p',
            self.local_path
        ]
        logger.info('Creation du dossier temporaire', cmd=cmd)
        subprocess.call(cmd)
        # Copie des fichiers sources vers le dossier de travail
        cmd = [
            'rsync',
            '-a',
            '--delete-after',
            '--exclude=".git"',
            self.origin+"/",
            self.local_path
        ]
        logger.info('Copie des fichiers', cmd=cmd)
        subprocess.call(cmd)

        # remplacement des variables par les valeurs
        if source_config.exist('variables'):
            for file_name, vars in list(source_config.get_node('variables').items()):
                filepath = "{}/{}".format(self.local_path, file_name)
                file_str = "filenotfound"
                with open (filepath, "rt") as f:
                    file_str = f.read()
                for var_name, value in list(vars.items()):
                    file_str = file_str.replace(var_name, value)
                with open (filepath, "wt") as f:
                    f.write(file_str)

    def __del__(self):
        cmd = [
            'rm',
            '-rf',
            "{}/{}".format(self.local_path, self.name)
        ]
        logger.info('Nettoyage de la source',cmd=cmd)
        if os.path.exists("{}/{}".format(self.local_path, self.name)):
            subprocess.call(cmd)
