#!/bin/bash
# Created by: Piotr "rzeka" Rzeczkowski <piotr@rzeka.net>
# Usage: https://github.com/rzeka/QLDS-Manager
# Last update: 2015-10-23

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

STEAMAPI_VERSION_CHECK="https://api.steampowered.com/ISteamApps/UpToDateCheck/v1/?&format=json&appid=282440&version="

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

    if [ `uname -m` == 'x86_64' ]; then
        SUDO=''
        if [ `id -u` -ne 0 ]; then
            SUDO='sudo'
        fi

        $SUDO dpkg --add-architecture i386
        $SUDO apt-get update
        $SUDO apt-get install lib32stdc++6
    fi

    echo "SteamCMD installed in $STEAMCMD_DIR"
elif [[ $1 == "update" ]]; then
    if [[ ! -f $STEAMCMD_DIR/steamcmd.sh || ! -x $STEAMCMD_DIR/steamcmd.sh ]]; then
        echo "Cannot find SteamCMD"
        exit 1
    fi

    echo "Updating QLDS files"
    exec $STEAMCMD_DIR/steamcmd.sh +login anonymous +force_install_dir $QL_DIR +app_update $QL_APPID +quit
    echo "QLDS updated"
elif [[ $1 == "supervisor-update" ]]; then
    if [ ! -x "$(command -v supervisorctl)" ]; then
        echo "Supervisor (supervisorctl) not found"
        exit 1
    fi

    if [[ check_outdated -eq 1 ]]; then
        SERVER_LIST=$(supervisorctl avail | grep qlds | awk '{print $1}' ORS=' ')

        echo "Updating servers"
        $0 update

        echo "Stopping all supervisord QLDS tagged instances"
        supervisorctl stop $SERVER_LIST

        echo "Servers back online"
        supervisorctl start $SERVER_LIST
    else
        echo "No update required"
        exit
    fi
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

    update_if_required

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
    echo "    $0 supervisor-update - disables all server managed by supervisord and performs an update"
fi

check_outdated() {
    QL_VERSION=$(strings $QL_DIR/qzeroded.x86 | grep "linux-i386" | awk '{print $1}' ORS='')
    QL_UP_TO_DATE="false"

    if [ ! -x "$(command -v wget)" ]; then
        QL_UP_TO_DATE=$(wget -qO- $STEAMAPI_VERSION_CHECK$QL_VERSION | grep "up_to_date" | awk '{print $2}' RS=',' ORS='')
    else
        QL_UP_TO_DATE=$(curl -s $STEAMAPI_VERSION_CHECK$QL_VERSION | grep "up_to_date" | awk '{print $2}' RS=',' ORS='')
    fi

    if [[ $QL_UP_TO_DATE == 'false' ]]; then
        echo 1
    else
        echo 0
    fi
}

update_if_required() {
    if [[ check_outdated -eq 1 ]]; then
        $0 update
    fi
}
