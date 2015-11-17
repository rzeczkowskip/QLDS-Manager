import os

from cement.core.controller import expose

from qldsmanager.command.default import ManagerDefaultController
from qldsmanager.util.config import Configuration


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
            (['--rcon'], dict(help='Sets location of rcon config (optional)', dest='rcon'))
        ]

    @expose(hide=True)
    def default(self):
        config = Configuration()

        if self.app.pargs.qldir is not None:
            config.set('dir', 'ql', os.path.expanduser(self.app.pargs.qldir))

        if self.app.pargs.steamdir is not None:
            config.set('dir', 'steamcmd', os.path.expanduser(self.app.pargs.steamdir))

        if self.app.pargs.servers is not None:
            config.set('config', 'servers', os.path.expanduser(self.app.pargs.servers))

        if self.app.pargs.supervisor is not None:
            config.set('supervisor', 'supervisor', os.path.expanduser(self.app.pargs.supervisor))

        if self.app.pargs.supervisorctl is not None:
            config.set('supervisor', 'supervisorctl', os.path.expanduser(self.app.pargs.supervisorctl))

        if self.app.pargs.rcon is not None:
            config.set('config', 'rcon', os.path.expanduser(self.app.pargs.rcon))

        config.update()

        data = [
            ('QLDS dir', config.get('dir', 'ql')),
            ('SteamCMD dir', config.get('dir', 'steamcmd')),

            ('Supervisor', config.get('supervisor', 'supervisor')),
            ('Supervisorctl', config.get('supervisor', 'supervisorctl')),

            ('Servers config', config.get('config', 'servers')),
            ('Rcon config', config.get('config', 'rcon'))
        ]

        for d in data:
            print('%s:\n    %s' % d)

        print('Configuration updated')
