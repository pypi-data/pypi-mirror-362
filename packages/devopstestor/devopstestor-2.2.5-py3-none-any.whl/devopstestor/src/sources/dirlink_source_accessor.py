
from abstract_source_accessor import AbstractSourceAccessor
import subprocess
import os
from log_manager import logging
logger = logging.getLogger('source.DirlinkSourceAccessor')

class DirlinkSourceAccessor(AbstractSourceAccessor):
    """
    Permet de transformer les sources en fichiers recuperables
    La source doit pouvoir etre copie sur une machine
    """
    def __init__(self, name, global_config, source_config):
        """
        Recupere la source si besoin pour la rendre accessible en fichier
        """
        super(DirlinkSourceAccessor, self).__init__(
            name=name,
            global_config=global_config,
            source_config=source_config
        )
        # Attributs specifiques a l'implementation FileSystem
        self.dir_name = os.path.dirname(self.local_path)
        self.readonly = source_config.get('readonly', True)
        self.name = name
        self.global_config = global_config
        self.source_config = source_config
        self.rollback_enable = False
        self.tmp_path = os.path.join(
            global_config.get('core::work_directory'),
            name
        )
        self.force_cleanup = self.global_config.get('source_manager::force_source_cleanup', False) is True

        if self.readonly is False and (source_config.get('rollback_oncleanup', False) is True or self.force_cleanup):
            self.rollback_enable = True
            if self.global_config.get('machine::resume_machine') == False or self.force_cleanup:
                # Sauvegarde du contenu
                cmd = [
                    'rsync',
                    '-a','--delete',
                    self.source_config.get('path::local')+'/',
                    self.tmp_path
                ]
                logger.info('Sauvegarde du volume', name=name,  cmd=cmd)
                subprocess.call(cmd)


    def __del__(self):
        if self.rollback_enable is True and (self.global_config.get('machine::preserve_machine') == False or self.force_cleanup):
            # recover content
            cmd = [
                'rsync',
                '-a','--delete',
                self.tmp_path + '/',
                self.source_config.get('path::local')
            ]
            logger.info('restauration du volume', name=self.name,  cmd=cmd)
            subprocess.call(cmd)
