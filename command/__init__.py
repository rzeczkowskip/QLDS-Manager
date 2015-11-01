from . import default
from . import version
from . import configure
from . import download

commands = [
    default.ManagerBaseController,
    version.VersionController,
    configure.ConfigureController,
    download.DownloadController
]
