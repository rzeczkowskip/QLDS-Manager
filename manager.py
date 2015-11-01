from cement.core.foundation import CementApp
import command
import util.config

class Manager(CementApp):
    class Meta:
        label = 'QLDS-Manager'
        handlers = command.commands


with Manager() as app:
    app.run()
