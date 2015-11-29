from cement.core.controller import CementBaseController, expose


class ManagerBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'QLDS Manager'
        usage = 'qldsmanager (sub-commands ...) [options ...] {arguments ...}'

    @expose(hide=True)
    def default(self):
        self.app.args.parse_args(['--help'])


class ManagerDefaultController(CementBaseController):
    class Meta:
        stacked_on = 'base'
        stacked_type = 'nested'
        usage = 'qldsmanager (sub-commands ...) [options ...] {arguments ...}'

    def _setup(self, base_app):
        super(ManagerDefaultController, self)._setup(base_app)

    def _help(self):
        self.app.args.parse_args(['--help'])
