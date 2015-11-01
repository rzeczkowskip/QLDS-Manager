from command.default import ManagerDefaultController
from cement.core.controller import expose
from util.config import Configuration
import os,sys

class SetupController(ManagerDefaultController):
    class Meta:
        label = 'setup'
        description = 'Allows to set directories for SteamCMD and Quake Live'
        arguments = [
            (['--steamcmd'], dict(help='Sets location of steamcmd', dest='STEAMDIR')),
            (['--ql'], dict(help='Sets location of QL Dedicated Server', dest='QLDIR')),
        ]

    @expose(hide=True)
    def default(self):
        if (self.app.pargs.QLDIR == None and self.app.pargs.STEAMDIR == None):
            self._help()
            sys.exit()

        config = Configuration()

        if (self.app.pargs.QLDIR != None):
            config.set('directories', 'ql', os.path.expanduser(self.app.pargs.QLDIR))

        if (self.app.pargs.STEAMDIR != None):
            config.set('directories', 'steamcmd', os.path.expanduser(self.app.pargs.STEAMCMD))

        config.update()