from command.default import ManagerDefaultController
from cement.core.controller import expose
from util.config import Configuration, ServerConfig
from util.supervisor import Supervisor
from util.filesystem import FSCheck

class SupervisorController(ManagerDefaultController):
    class Meta:
        label = 'supervisor'
        description = 'Supervisor management'

    @expose(hide=True)
    def default(self):
        self.app.args.parse_args(['--help'])

    @expose(help='Powers off supervisord and all its processes')
    def stop(self):
        supervisor = Supervisor()

        supervisor.ctl(['shutdown'])

    @expose(help='Start supervisord service')
    def start(self):
        supervisor = Supervisor()

        supervisor.start()

    @expose(help='Regenerates and reloads supervisord config file. This will restart modified servers!')
    def reload(self):
        supervisor = Supervisor()
        servers_config = ServerConfig()

        supervisor.generate_config(servers_config.servers)

        supervisor.ctl(['reload'])
        supervisor.ctl(['update'])

    @expose(help='Check if server\'s configuration is valid')
    def check(self):
        ServerConfig()
        print('Configs are OK')
