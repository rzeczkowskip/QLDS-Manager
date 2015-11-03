from command.default import ManagerDefaultController
from cement.core.controller import expose
from util.config import Configuration
from urllib.request import urlretrieve
from subprocess import call
import os
import stat
import tarfile


class DownloadController(ManagerDefaultController):
    steamcmd_url = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz'
    steamcmd_archive = '/steamcmd.tar.gz'
    ql_appid = 349090

    class Meta:
        label = 'download'
        description = 'Allows to download/update SteamCMD and QL Dedicated Server files'

    @expose(hide=True)
    def default(self):
        self.app.args.parse_args(['--help'])

    @expose(help='Downloads and installs SteamCMD')
    def steamcmd(self):
        config = Configuration()

        steamcmd_dir = os.path.expanduser(config.get('dir', 'steamcmd'))

        #check if steamcmd dir exists
        if os.path.isdir(steamcmd_dir):
            print(steamcmd_dir + ' exists. Remove it or change SteamCMD location with "setup" command')
            exit(30)

        os.makedirs(steamcmd_dir)

        if not os.access(steamcmd_dir, os.W_OK):
            print('Cannot get write access to ' + steamcmd_dir)
            exit(31)

        print('Downloading SteamCMD archive')
        urlretrieve(self.steamcmd_url, steamcmd_dir + self.steamcmd_archive)

        print('Extracting SteamCMD atchive to ' + steamcmd_dir)
        archive = tarfile.open(steamcmd_dir + self.steamcmd_archive)
        archive.extractall(steamcmd_dir)

        steamcmd_stat = os.stat(steamcmd_dir + '/steamcmd.sh')
        os.chmod(steamcmd_dir + '/steamcmd.sh', steamcmd_stat.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        print('SteamCMD installed in ' + steamcmd_dir)
        print('Remember that you need "lib32stdc++6" installed in your system')

    @expose(help='Downloads and updates QL Dedicated Server files')
    def ql(self):
        config = Configuration()

        steamcmd = os.path.expanduser(config.get('dir', 'steamcmd') + '/steamcmd.sh')

        if not os.path.exists(steamcmd):
            print('SteamCMD executable doesn\'t exist. Install SteamCMD first')
            exit(32)

        if not os.access(steamcmd, os.X_OK):
            print('SteamCMD script (' + steamcmd + ') is not executable')
            exit(31)

        print('Downloading QL Dedicated Server files using SteamCMD...')

        call([
            steamcmd,
            '+login anonymous +force_install_dir %s +app_update %d +quit' % (config.get('dir', 'ql'), self.ql_appid)
        ])