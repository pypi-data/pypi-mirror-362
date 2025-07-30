
import subprocess
import os
from core_utils import import_class, get_global_path
from config import Config
import logging

log = logging.getLogger("sources.sourcemanager")

class SourceManager():
    """
    Gestion des differentes sources de donnes (Accessor)
    """
    def __init__(self, global_config):
        """
        Initialisation charge les accessors definis dans la configuration
        """
        log.info('Init sourcemanager')
        self.global_config = global_config
        sources = global_config.get_node('source_manager').get_node('sources').config
        self.accessors = {}
        disabled_sources = global_config.get('source_manager::disabled_sources')
        for name, source_config in list(sources.items()):
            if name not in disabled_sources:
                # Transforme relative path to real path
                lpath = get_global_path(global_config, source_config.get('path',{}).get('local'))
                self.add_source_accessor(
                    name=name,
                    source_config=source_config
                )

    def get_accessors(self):
        return self.accessors

    def add_source_accessor(self, name, source_config):
        log.info('Recuperation de la source', name=name)
        self.accessors[name] = import_class(source_config.get('accessor_type'))(
            name=name,
            global_config=self.global_config,
            source_config=Config.create_from_dict(source_config)
        )
