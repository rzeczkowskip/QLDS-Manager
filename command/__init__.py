from . import default
from . import version
from . import setup

commands = [
    default.ManagerBaseController,
    version.VersionController,
    setup.SetupController
]
