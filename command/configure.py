from command.default import ManagerDefaultController
from cement.core.controller import expose
from util.config import Configuration
import os


class ConfigureController(ManagerDefaultController):
    class Meta:
        label = 'configure'
        description = 'Allows to set directories for SteamCMD and Quake Live'
        arguments = [
            (['--steamcmd'], dict(help='Sets location of steamcmd', dest='steamdir')),
            (['--ql'], dict(help='Sets location of QL Dedicated Server', dest='qldir')),
            (['--servers'], dict(help='Sets location of server list config', dest='servers')),
        ]

    @expose(hide=True)
    def default(self):
        config = Configuration()

        if self.app.pargs.qldir is not None:
            config.set('directories', 'ql', os.path.expanduser(self.app.pargs.qldir))

        if self.app.pargs.steamdir is not None:
            config.set('directories', 'steamcmd', os.path.expanduser(self.app.pargs.steamdir))

        if self.app.pargs.servers is not None:
            config.set('config', 'servers', os.path.expanduser(self.app.pargs.servers))

        config.update()
        print('Configuration updated')