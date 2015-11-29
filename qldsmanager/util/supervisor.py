from configparser import ConfigParser
import platform
import os
from subprocess import call

from qldsmanager.util.config import Configuration
from qldsmanager.util.filesystem import FSCheck


class Supervisor:
    def __init__(self):
        self.__config = Configuration()
        self.process_prefix = 'qlds_'

        self.__config_file = self.__config.get_config_dir() + '/supervisor.conf'

    def generate_config(self, servers):
        parser = ConfigParser()

        config_dir = self.__config.get_config_dir()

        parser.add_section('unix_http_server')
        parser.set('unix_http_server', 'file', config_dir + '/supervisor.sock')
        parser.set('unix_http_server', 'chmod', '0700')

        parser.add_section('supervisord')
        parser.set('supervisord', 'logfile', config_dir + '/supervisor_error.log')
        parser.set('supervisord', 'pidfile', config_dir + '/supervisor.pid')

        parser.add_section('rpcinterface:supervisor')
        parser.set('rpcinterface:supervisor', 'supervisor.rpcinterface_factory', 'supervisor.rpcinterface:make_main_rpcinterface')

        parser.add_section('supervisorctl')
        parser.set('supervisorctl', 'serverurl', 'unix://' + config_dir + '/supervisor.sock')

        ql_executable = self.get_ql_executable()

        for sid,data in servers.items():
            name = self.process_prefix + sid
            section = 'program:' + name
            parser.add_section(section)
            parser.set(section, 'command', self.build_command_line(sid, data, ql_executable))
            parser.set(section, 'process_name', name)
            parser.set(section, 'autorestart', 'true')

        if os.path.isfile(self.__config_file) and not os.access(self.__config_file, os.W_OK):
            raise IOError('Cannot write to file ' + self.__config_file)

        with (open(self.__config_file, 'w+')) as config_fp:
            parser.write(config_fp)

    def build_command_line(self, sid, server, executable):
        command_line = [
            executable,
            '+set fs_homepath %s/%s' % (os.path.expanduser('~/.quakelive/'), sid)
        ]

        for k,v in sorted(server.items()):
            command_line.append('+set %s %s' % (k, v))

        return ' '.join(command_line)

    def get_ql_executable(self):
        if platform.architecture()[0] == '64bit':
            executable = 'run_server_x64.sh'
        else:
            executable = 'run_server_x86.sh'

        return os.path.expanduser(self.__config.get('dir', 'ql')) + '/' + executable

    def get_config_location(self):
        return self.__config_file

    def start(self):
        supervisor_executable = self.__config.get('supervisor', 'supervisor')
        supervisor_executable_fs = FSCheck(supervisor_executable)

        supervisor_executable_fs.exists()
        supervisor_executable_fs.access('x')

        return call([supervisor_executable, '-c', self.__config_file])

    def ctl(self, args: list):
        args = list(args)

        ctl_executable = self.__config.get('supervisor', 'supervisorctl')
        ctl_executable_fs = FSCheck(ctl_executable)

        ctl_executable_fs.exists()
        ctl_executable_fs.access('x')

        call_args = [ctl_executable, '-c', self.__config_file] + args

        return call(call_args)
