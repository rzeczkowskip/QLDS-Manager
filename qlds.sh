#!/bin/bash
# Created by: Piotr "rzeka" Rzeczkowski <piotr@rzeka.net>
# Usage: https://github.com/rzeka/QLDS-Manager
# Last update: 2015-10-21

if [[ $HOME == '' ]]; then
    echo "No home dir available"
    exit 1
fi

STEAMCMD_DIR="$HOME/steamcmd"
QL_DIR="$HOME/QLserver"

#Don't change anything after this line :)
QL_APPID="349090"
STEAMCMD_URL="https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
STEAMCMD_ARCHIVE="steamcmd_linux.tar.gz"

if [[ $1 == "steamcmd" ]]; then
    if [[ -d $STEAMCMD_DIR ]]; then
        echo "SteamCMD directory already exists - remove it before installing SteamCMD again"
        exit 1
    fi

    mkdir $STEAMCMD_DIR
    cd $STEAMCMD_DIR

    if [[ $2 == "wget" ]]; then
        wget $STEAMCMD_URL
    else
        curl -O $STEAMCMD_URL
    fi

    tar zxf $STEAMCMD_ARCHIVE
    chmod +x steamcmd.sh

    echo "SteamCMD installed in $STEAMCMD_DIR"
elif [[ $1 == "update" ]]; then
    if [[ ! -f $STEAMCMD_DIR/steamcmd.sh || ! -x $STEAMCMD_DIR/steamcmd.sh ]]; then
        echo "Cannot find SteamCMD"
        exit 1
    fi

    exec $STEAMCMD_DIR/steamcmd.sh +login anonymous +force_install_dir $QL_DIR +app_update $QL_APPID +quit
elif [[ $1 == "run" ]]; then
    if [[ $2 == '' || ! -f $2 ]]; then
        echo "You have to pass config location as parameter eg.:"
        echo "$0 run ~/myconfig server_id"
        exit 1
    fi

    if [[ $3 == '' || $3 -lt 0 ]]; then
        echo "You have to pass server ID you want to start"
        exit 1
    fi

    . $2

    if [ `uname -m` == 'x86_64' ]; then
        QL_EXEC="run_server_x64.sh"
    else
        QL_EXEC="run_server_x86.sh"
    fi

    SERVER_CONFIG=${SERVER[$3]}
    if [[ $SERVER_CONFIG == '' ]]; then
        echo "Server config $3 doesn't exists!"
    else
        exec $QL_DIR/$QL_EXEC $SERVER_CONFIG
    fi
else
    echo "Available commands: steamcmd, update, run"
    echo "    $0 steamcmd - installs steamcmd"
    echo "    $0 update - updates QL server files"
    echo "    $0 run [server config file] [server id] - run server using specified config and id"
fi
