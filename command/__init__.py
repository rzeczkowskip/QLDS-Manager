from command import default
from command import version
from command import configure
from command import download
from util.config import Configuration
from util.filesystem import FSCheck


def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

commands = [
    default.ManagerBaseController,
    version.VersionController,
    configure.ConfigureController,
    download.DownloadController,
    #server.ServerController,
    #supervisor.SupervisorController,
    #rcon.RconController
]

config = Configuration()
supervisor_fs = FSCheck(config.get('supervisor', 'supervisor'))
supervisorctl_fs = FSCheck(config.get('supervisor', 'supervisorctl'))

if supervisor_fs.exists(error=False) and supervisor_fs.access('x', error=False) and supervisorctl_fs.exists(error=False) and supervisorctl_fs.access('x', error=False):
    from command import server
    from command import supervisor

    commands.append(server.ServerController)
    commands.append(supervisor.SupervisorController)

if module_exists('zmq'):
    from command import rcon
    commands.append(rcon.RconController)

