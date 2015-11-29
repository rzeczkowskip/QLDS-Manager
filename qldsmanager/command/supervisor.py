from cement.core.controller import expose

from qldsmanager.command.default import ManagerDefaultController
from qldsmanager.util.config import ServerConfig
from qldsmanager.util.supervisor import Supervisor


class SupervisorController(ManagerDefaultController):
    supervisor = Supervisor()
    servers = ServerConfig()

    class Meta:
        label = 'supervisor'
        description = 'Supervisor management'

    @expose(hide=True)
    def default(self):
        self.app.args.parse_args(['--help'])

    @expose(help='Powers off supervisord and all its processes')
    def stop(self):
        self.supervisor.ctl(['shutdown'])

    @expose(help='Start supervisord service')
    def start(self):
        self.supervisor.generate_config(self.servers.servers)

        self.supervisor.start()

    @expose(help='Regenerates and reloads supervisord config file. This will restart modified servers!')
    def reload(self):
        self.supervisor.generate_config(self.servers.servers)
        self.supervisor.ctl(['update'])
