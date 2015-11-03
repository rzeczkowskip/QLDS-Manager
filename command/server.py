from command.default import ManagerDefaultController
from cement.core.controller import expose
from util.config import ServerConfig


class ServerController(ManagerDefaultController):
    class Meta:
        label = 'server'
        description = 'Server management'
        arguments = [
            (['--check'], dict(help='Checks configuration and exits app', action='store_true')),
        ]

    @expose(hide=True)
    def default(self):
        if self.app.pargs.check:
            self.check()

        self.app.args.parse_args(['--help'])

    def check(self):
        ServerConfig()
        exit()
