from cement.core.foundation import CementApp
import command
import util.config

util.config.Configuration()

class Manager(CementApp):
    class Meta:
        label = 'QLDS-Manager'
        handlers = [
            command.default.ManagerBaseController,
            command.setup.SetupController
        ]


with Manager() as app:
    app.run()