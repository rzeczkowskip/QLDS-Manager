from configparser import ConfigParser
import os


class AbstractConfig:
    __config_dir = os.path.expanduser('~/.qldsmanager/') #has to end with /
    filename = None
    required = None

    def __init__(self):
        if self.filename == '':
            self.filename = None

        self.parser = self.__get_parser(self.filename)

        if self.required:
            self.__check_missing(self.required)

        self.extra_check()

    def __get_parser(self, filename):
        parser = ConfigParser()

        if os.path.isfile(filename):
            parser.read_file(open(filename))

        parser.read(os.path.expanduser(self.__config_dir + filename))

        return parser

    def __check_missing(self, options: dict):
        missing = self.__has_missing(self.parser.sections(), options.keys())
        if missing:
            print('Missing sections in configuration: ' + ', '.join(missing))
            exit(10)

        missing_options = dict()
        for section,values in options.items():
            missing = self.__has_missing(self.parser.options(section), values)
            if missing:
                missing_options[section] = missing

        if missing_options:
            print('Missing options in sections\n  ' + '\n  '.join([
                              '%s: %s' % (key, value) for (key, value) in missing_options.items()
                              ]))
            exit(11)

    def __has_missing(self, data, keys):
        missing = []

        for k in keys:
            if k not in data:
                missing.append(k)

        return missing

    def update(self):
        config_file = self.__config_dir + self.filename

        if not os.path.isdir(self.__config_dir):
            os.mkdir(self.__config_dir)

        if os.path.isfile(config_file) and not os.access(config_file, os.W_OK):
            raise IOError('Cannot write to file ' + config_file)

        with (open(config_file, 'w+')) as config_fp:
            self.parser.write(config_fp)

    def set(self, section: str, option: str, value):
        return self.parser.set(section, option, value)

    def get(self, section, option):
        return self.parser.get(section, option)

    def extra_check(self):
        return True

class Configuration(AbstractConfig):
    filename = 'config'
    required = dict(
        dir=['ql', 'steamcmd'],
        config=['servers']
    )
