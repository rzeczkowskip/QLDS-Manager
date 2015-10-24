# QLDS Manager

## Download

Grab the latest stable version from https://github.com/rzeka/QLDS-Manager/releases

## Default locations

* SteamCMD - `$HOME/steamcmd/`
* QL server files - `$HOME/QLserver`

To change those directories, open `qlds.sh` script and edit those lines:

```bash
STEAMCMD_DIR="$HOME/steamcmd"
QL_DIR="$HOME/QLserver"
```

## SteamCMD

If You haven't got SteamCMD yet, run script like:

`./qlds.sh steamcmd`

## Quake Live Server files

To install or update QL server files

`./qlds.sh update`

## Run the server

To run server, use script with `run` argument. It requires 2 additional arguments:

* Server-list file location
* Server ID from server-list

Eg.:
`./qlds.sh run /home/qlserver/qlds_config 0`

## Server config file

You can check example config file in `qlds_config`. It's just a simple array, so You can define as many servers as You want.
Notice that each server is defined in `SERVER` variable with id in `[]` eg.: `SERVER[0]` is server with id `0`

There are 2 servers configures in there. If You need some help with creating another server, check https://github.com/rzeka/QLDS-Manager

## Example supervisord config

```bash
[program:qlds]
command=/home/qlserver/qldsmanager.sh run /home/qlserver/qlds_config %(process_num)s
user=qlserver
process_name=qlds_%(process_num)s
numprocs=2
autorestart=true
environment=HOME="/home/qlserver",USER="qlserver"
```

# TODO

* Detailed supervisord configuration
* More process control system configurations
