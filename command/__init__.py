from . import default
from . import version
from . import setup
from . import download

commands = [
    default.ManagerBaseController,
    version.VersionController,
    setup.SetupController,
    download.DownloadController
]
