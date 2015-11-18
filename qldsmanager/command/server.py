from cement.core.controller import expose

from qldsmanager.command.default import ManagerDefaultController
from qldsmanager.util.config import ServerConfig
from qldsmanager.util.supervisor import Supervisor


class ServerController(ManagerDefaultController):
    class Meta:
        label = 'server'
        description = 'Server management'
        arguments = [
            (['--check'], dict(help='Checks configuration and exits app', action='store_true')),
            (['server_ids'], dict(
                help='Server id available in servers config file (servers:<id>:group)',
                action='store',
                nargs='*'
            ))
        ]

    @expose(hide=True)
    def default(self):
        if self.app.pargs.check:
            ServerConfig()

        self.app.args.parse_args(['--help'])

    @expose(help='Start server <server_id>')
    def start(self):
        supervisor = Supervisor()
        server_config = ServerConfig()

        for sid in self.app.pargs.server_ids:
            if sid in server_config.servers:
                supervisor.ctl(['start', supervisor.process_prefix + sid])
            else:
                print('Server %s doesn\'t exists' % str(sid))
                exit(50)

    @expose(help='Stop server <server_id>')
    def stop(self):
        supervisor = Supervisor()
        server_config = ServerConfig()

        for sid in self.app.pargs.server_ids:
            if sid in server_config.servers:
                supervisor.ctl(['stop', supervisor.process_prefix + sid])
            else:
                print('Server %s doesn\'t exists' % str(sid))
                exit(50)

    @expose(help='Restart server <server_id>')
    def restart(self):
        supervisor = Supervisor()
        server_config = ServerConfig()

        for sid in self.app.pargs.server_ids:
            if sid in server_config.servers:
                supervisor.ctl(['restart', supervisor.process_prefix + sid])
            else:
                print('Server %s doesn\'t exists' % str(sid))
                exit(50)

    @expose(help='Attch server <server_id>')
    def attach(self):
        supervisor = Supervisor()
        server_config = ServerConfig()

        for sid in self.app.pargs.server_ids:
            if sid in server_config.servers:
                supervisor.ctl(['fg', supervisor.process_prefix + sid])
            else:
                print('Server %s doesn\'t exists' % str(sid))
                exit(50)

