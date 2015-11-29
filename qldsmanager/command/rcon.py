from cement.core.controller import expose

from qldsmanager.command.default import ManagerDefaultController
from qldsmanager.util.config import ServerConfig, RconConfig
from qldsmanager.util.rcon import Rcon


class RconController(ManagerDefaultController):
    class Meta:
        label = 'rcon'
        description = 'Rcon console'
        arguments = [
            (['server_id'], dict(
                help='Server id available in servers config file (servers:<id>:group)',
                action='store'
            ))
        ]

    @expose(hide=True)
    def default(self):
        sid = self.app.pargs.server_id

        servers = ServerConfig().servers
        rcon = RconConfig().servers

        is_rcon = False

        if sid in rcon:
            server = rcon[sid]
            is_rcon = True
        elif sid in servers:
            server = servers[sid]
        else:
            print('Server %s doesn\'t exists' % sid)
            exit(50)

        if not is_rcon and 'zmq_rcon_enable' not in server:
            print('Rcon not enabled in server configuration %s' % sid)
            exit(51)

        if 'zmq_rcon_port' not in server:
            print('Rcon port missing in server configuration %s' % sid)
            exit(52)

        if 'zmq_rcon_password' not in server:
            print('Rcon password missing in server configuration %s' % sid)

        if 'zmq_rcon_ip' in server:
            host = server['zmq_rcon_ip']
        elif 'net_ip' in server:
            host = server['net_ip']
        else:
            host = '127.0.0.1' #defaults to localhost

        port = server['zmq_rcon_port']
        password = server['zmq_rcon_password']

        rcon = Rcon(host, port, password)
        rcon.connect()

        loop = True
        while loop:
            loop = rcon.loop()
