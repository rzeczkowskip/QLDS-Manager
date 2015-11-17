from cement.core.foundation import CementApp
import command
import signal
from cement.core.exc import CaughtSignal


class Manager(CementApp):
    class Meta:
        label = 'QLDS-Manager'
        handlers = command.commands


with Manager() as app:
    try:
        app.run()
    except CaughtSignal as e:
        # do something with e.signum or e.frame (passed from signal)
        if e.signum in [signal.SIGTERM, signal.SIGINT]:
            print('Exiting...')
