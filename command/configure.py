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
            (['--supervisor'], dict(help='Sets location of supervisord executable', dest='supervisor')),
            (['--supervisorctl'], dict(help='Sets location of supervisorctl executable', dest='supervisorctl')),
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

        if self.app.pargs.supervisor is not None:
            config.set('supervisor', 'supervisor', os.path.expanduser(self.app.pargs.supervisor))

        if self.app.pargs.supervisorctl is not None:
            config.set('supervisor', 'supervisorctl', os.path.expanduser(self.app.pargs.supervisorctl))

        config.update()
        print('Configuration updated')
