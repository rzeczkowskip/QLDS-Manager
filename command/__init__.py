from . import default
from . import version
from . import configure
from . import download
from . import server
from . import supervisor

commands = [
    default.ManagerBaseController,
    version.VersionController,
    configure.ConfigureController,
    download.DownloadController,
    server.ServerController,
    supervisor.SupervisorController
]
