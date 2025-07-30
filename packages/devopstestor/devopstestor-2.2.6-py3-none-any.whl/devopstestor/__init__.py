import coloredlogs
coloredlogs.install()
from .src.core.devopstestor import Devopstestor
from .src.core.devopstestor_server import DevopstestorServer
from .src.core.devopstestor_client import DevopstestorClient
from .src.core import *
from .src.lib import *
from .src.machine import *
from .src.provisionner import *
from .src.reporting import *
from .src.sources import *
from .src.testcase import *
from .src.scenarios import *
