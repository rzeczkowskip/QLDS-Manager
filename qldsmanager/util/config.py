from configparser import ConfigParser
import os
import re

from qldsmanager import app_dir
from qldsmanager.util.matheval import eval_expr
from qldsmanager.util.filesystem import FSCheck


class AbstractConfig:
    def __init__(self):
        self.__config_dir = os.path.expanduser('~/.qldsmanager/') #has to end with /

        if not hasattr(self, 'filename'):
            self.filename = None

        if not hasattr(self, 'filepath'):
            self.filepath = None

        if not hasattr(self, 'reuired'):
            self.required = None

        self._configure()

        self.parser = self.__get_parser()

        if self.required:
            self.__check_missing()

        self.extra_check()

    def __get_parser(self):
        parser = ConfigParser()

        if self.filepath is None:
            if os.path.isfile(app_dir + self.filename):
                parser.read_file(open(app_dir + self.filename))

            parser.read(os.path.expanduser(self.__config_dir + self.filename))
        else:
            parser.read(os.path.expanduser(self.filepath))

        return parser

    def __check_missing(self):
        options = self.required
        missing = self._has_missing(self.parser.sections(), options.keys())
        if missing:
            print('Missing sections in configuration: %s' % ', '.join(missing))
            exit(10)

        missing_options = dict()
        for section,values in options.items():
            missing = self._has_missing(self.parser.options(section), values)
            if missing:
                missing_options[section] = missing

        if missing_options:
            print('Missing options in sections\n  %s' % '\n  '.join([
                              '%s: %s' % (key, value) for (key, value) in missing_options.items()
                              ]))
            exit(11)

    def _has_missing(self, data, required_keys):
        missing = []
        for k in required_keys:
            if k not in data:
                missing.append(k)

        return missing

    def update(self):
        config_file = self.__config_dir + self.filename

        if not os.path.isdir(self.__config_dir):
            os.mkdir(self.__config_dir)

        if os.path.isfile(config_file) and not os.access(config_file, os.W_OK):
            raise IOError('Cannot write to file %s' % config_file)

        with (open(config_file, 'w+')) as config_fp:
            self.parser.write(config_fp)

    def set(self, section: str, option: str, value):
        return self.parser.set(section, option, value)

    def get(self, section, option):
        try:
            return self.parser.get(section, option)
        except:
            return None

    def get_config_dir(self):
        return self.__config_dir

    def extra_check(self):
        return True

    def pre_parse(self):
        return True

    def _configure(self):
        return True


class Configuration(AbstractConfig):
    def _configure(self):
        self.filename = 'config'
        self.required = dict(
            dir=['ql', 'steamcmd'],
            config=['servers']
        )


class ServerConfig(AbstractConfig):
    def __init__(self):
        self.config = Configuration()
        self.extra_required = ['net_port']

        self.servers = {}
        self.parameters = {}
        self.defaults = {}
        self.extra = {}
        self.loop = {}

        self._configure()

        self.filepath = os.path.expanduser(self.config.get('config', 'servers'))
        self.filename = os.path.basename(self.filepath)

        servers_file_dir = os.path.dirname(self.filepath)
        servers_file_dir_fs = FSCheck(servers_file_dir)

        if not servers_file_dir_fs.exists(error=False):
            os.makedirs(servers_file_dir)

        servers_file_fs = FSCheck(self.filepath)
        if not servers_file_fs.exists(error=False):
            open(self.servers_file, 'a').close()

        if not servers_file_fs.access('r'):
            print('Cannot open server list configuration for reading')
            exit(33)

        super(ServerConfig, self).__init__()

    def extra_check(self):
        self.__compile()

        missing_options = dict()

        for sid,data in self.servers.items():
            missing = self.check_required(data)
            if missing:
                missing_options[sid] = missing

        if missing_options:
            print('Missing options in servers\n  %s' % '\n  '.join([
                              '%s: %s' % (key, value) for (key, value) in missing_options.items()
                              ]))
            exit(11)

    def __compile(self):
        self.parameters = self.__parse_section('parameters')

        self.defaults = self.__parse_section('defaults')
        self.extra = self.__parse_section('extra')

        for section in self.parser.sections():
            name = None

            if section.startswith('defaults:'):
                name = section.split(':', 1)
                if len(name) > 1:
                    self.defaults[name[1]] = self.__parse_section(section)

            if section.startswith('extra:'):
                name = section.split(':', 1)
                if len(name) > 1:
                    self.extra[name[1]] = self.__parse_section(section)

            if section.startswith('server:'):
                sid = section.split(':', 1)
                if len(sid) > 1:
                    self.servers[sid[1]] = self.__parse_section(section)

            if name is not None and len(name) > 1:
                self.loop[name[1]] = 1

        global_loop = 1

        tmp_servers = {}

        for sid in sorted(self.servers):
            extend = None
            name = sid.split(':', 1)
            if len(name) > 1:
                extend = name[1]

            tmp_servers[name[0]] = self.__parse_server(sid, extend, global_loop)

            global_loop += 1
            if extend is not None:
                self.loop[extend] += 1

        self.servers = tmp_servers

    def __parse_section(self, section):
        tmp = {}
        if self.parser.has_section(section):
            for o,v in self.parser.items(section):
                tmp[o] = v

        return tmp

    def __parse_server(self, sid, extend, global_loop):
        parsed = {}
        server = self.servers[sid]

        if extend is not None and extend in self.defaults:
            tmp = self.defaults[extend].copy()
            tmp.update(server)
            server = tmp

        for k,v in server.items():
            if extend is not None and extend in self.extra:
                if k in self.extra[extend]:
                    v = self.extra[extend][k].replace('${self}', v)

            v = self.__replace_parameters(v, server, extend, global_loop)

            parsed[k] = v

        return parsed

    def __replace_parameters(self, str_, server, extend, global_loop):
        #find all parameters
        for param in re.findall('\$\{parameters\.(\w+)\}', str_):
            if param in self.parameters:
                str_ = str_.replace('${parameters.' + param + '}', self.parameters[param])

        for param in re.findall('\$\{server\.(\w+)\}', str_):
            if param in server:
                str_ = str_.replace('${server.' + param + '}', server.get(param))

        str_ = str_.replace('${global.loop}', str(global_loop))

        if extend is not None and extend in self.loop:
            str_ = str_.replace('${loop}', str(self.loop[extend]))

        for math in re.findall('>>(.+)<<', str_):
            str_ = str_.replace(
                '>>' + math + '<<',
                str(eval_expr(
                    self.__replace_parameters(math, server, extend, global_loop))
                    )
            )

        return str_

    def check_required(self, server: list):
        return self._has_missing(server, self.extra_required)


class RconConfig(ServerConfig):
    def _configure(self):
        self.extra_required = ['zmq_rcon_port']
        self.servers_file = os.path.expanduser(self.config.get('config', 'rcon'))
