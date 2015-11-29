import signal

from cement.core.foundation import CementApp
from cement.core.exc import CaughtSignal

from qldsmanager.command import default, version, configure, download
from qldsmanager.util.config import Configuration
from qldsmanager.util.filesystem import FSCheck


def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

commands = [
    default.ManagerBaseController,
    version.VersionController,
    configure.ConfigureController,
    download.DownloadController,
    #download.DownloadWorkshopController,
]

config = Configuration()

supervisor_fs = FSCheck(config.get('supervisor', 'supervisor'))
supervisorctl_fs = FSCheck(config.get('supervisor', 'supervisorctl'))

if (
        supervisor_fs.exists(error=False) and supervisor_fs.access('x', error=False) and
        supervisorctl_fs.exists(error=False) and supervisorctl_fs.access('x', error=False)
   ):
    from qldsmanager.command import server
    from qldsmanager.command import supervisor

    commands.append(server.ServerController)
    commands.append(supervisor.SupervisorController)


if module_exists('zmq'):
    from qldsmanager.command import rcon
    commands.append(rcon.RconController)


class Manager(CementApp):
    class Meta:
        label = 'QLDS-Manager'
        handlers = commands


def main():
    with Manager() as app:
        try:
            app.run()
        except CaughtSignal as e:
            # do something with e.signum or e.frame (passed from signal)
            if e.signum in [signal.SIGTERM, signal.SIGINT]:
                print('Exiting...')

if __name__ == '__main__':
    main()
