#!/bin/bash
# https://github.com/rzeka/QLDS-Manager

if [[ $HOME == '' ]]; then
    echo "No home dir available"
    exit 1
fi

STEAMCMD_DIR="$HOME/steamcmd"
QL_DIR="$HOME/QLserver"

QLDS_MANAGER_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

QL_APPID="349090"
STEAMCMD_URL="https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
STEAMCMD_ARCHIVE="steamcmd_linux.tar.gz"

STEAMAPI_VERSION_CHECK="https://api.steampowered.com/ISteamApps/UpToDateCheck/v1/?&format=json&appid=282440&version="
check_wget () {
  if [ ! -x "$(command -v wget)" ]; then
    return 0
  else
    return 1
  fi
}

check_curl() {
    if [ ! -x "$(command -v curl)" ]; then
        return 0
    else
        return 1
    fi
}

download_error() {
    echo "Neither \"curl\" nor \"wget\" is installed."
    echo "Please install one and re-run this script."
    exit 1
}
check_outdated() {
    QL_VERSION=$(strings $QL_DIR/qzeroded.x86 | grep "linux-i386" | awk '{print $1}' ORS='')
    QL_UP_TO_DATE="false"

    if [ check_wget ]; then
        QL_UP_TO_DATE=$(wget -qO- $STEAMAPI_VERSION_CHECK$QL_VERSION | grep "up_to_date" | awk '{print $2}' RS=',' ORS='')
    elif [ check_curl ]; then
        QL_UP_TO_DATE=$(curl -s $STEAMAPI_VERSION_CHECK$QL_VERSION | grep "up_to_date" | awk '{print $2}' RS=',' ORS='')
    else
        download_error
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
load_server_list() {
    if [[ $1 == '' || ! -f $1 ]]; then
        echo "You have to pass server-list file location as parameter eg.:"
        echo "$0 run ~/myconfig server_id"
        exit 1
    fi

    . $1
}
command_monitor() {
    load_server_list $1

    #If no ID is passed, get all IDs and re-run minitor for each id
    if [[ $2 == '' ]]; then
        #get keys from $SERVER
        for ID in ${!SERVER[*]}; do
            $0 monitor $1 $ID &
        done
    else
        until $0 run $1 $2; do
            echo "Restarting server $2"
            sleep 1 # sleep, so if server always exits unexpectedly, we won't kill server
        done
    fi
}
command_run() {
    if [[ $2 == '' || $2 -lt 0 ]]; then
        echo "You have to pass server ID you want to start"
        exit 1
    fi

    load_server_list $1

    update_if_required

    if [ `uname -m` == 'x86_64' ]; then
        QL_EXEC="run_server_x64.sh"
    else
        QL_EXEC="run_server_x86.sh"
    fi

    SERVER_CONFIG=${SERVER[$2]}
    if [[ $SERVER_CONFIG == '' ]]; then
        echo "Server config $2 doesn't exists!"
    else
        exec $QL_DIR/$QL_EXEC $SERVER_CONFIG
    fi
}
command_steamcmd() {
    if [[ -d $STEAMCMD_DIR ]]; then
        echo "SteamCMD directory already exists - remove it before installing SteamCMD again"
        exit 1
    fi

    if [[ $1 == '' && `uname -m` == 'x86_64' ]]; then
        SUDO=''
        if [ `id -u` -ne 0 ]; then
            SUDO='sudo'
        fi

        echo "Script has to check if \"lib32stdc++6\" is installed and may try"
        echo "to use \"sudo\" to do that. If you don't trust it, install"
        echo "\"lib32stdc++6\" manually and re-run this command with additional"
        echo "argument like:"
        echo "$0 steamcmd no-root"
        echo
        echo "Press [ENTER] to continue"

        read

        $SUDO dpkg --add-architecture i386
        $SUDO apt-get -qq update
        $SUDO apt-get -q install lib32stdc++6
    fi

    mkdir $STEAMCMD_DIR
    cd $STEAMCMD_DIR

    if [[ check_wget ]]; then
        wget $STEAMCMD_URL
    elif [[ check_curl ]]; then
        curl -O $STEAMCMD_URL
    else
        cd "$QLDS_MANAGER_DIR"
        rm -rf $STEAMCMD_DIR
        download_error
    fi

    tar zxf $STEAMCMD_ARCHIVE
    chmod +x steamcmd.sh

    echo "SteamCMD installed in $STEAMCMD_DIR"
}
command_supervisor_update() {
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
        exit 0
    fi
}
command_update() {
    if [[ ! -f $STEAMCMD_DIR/steamcmd.sh || ! -x $STEAMCMD_DIR/steamcmd.sh ]]; then
        echo "Cannot find SteamCMD"
        exit 1
    fi

    echo "Updating QLDS files"
    exec $STEAMCMD_DIR/steamcmd.sh +login anonymous +force_install_dir $QL_DIR +app_update $QL_APPID +quit
    echo "QLDS updated"
}
# https://github.com/rzeka/QLDS-Manager

if [[ $1 == "steamcmd" ]]; then
    command_steamcmd $2
elif [[ $1 == "update" ]]; then
    command_update
elif [[ $1 == "supervisor-update" ]]; then
    command_supervisor_update
elif [[ $1 == "run" ]]; then
    command_run $2 $3
elif [[ $1 == "monitor" ]]; then
    command_monitor $2 $3
else
    echo "Usage: $0 [command] arg, arg..."
    echo
    echo "Available commands: steamcmd, update, run"
    echo
    echo "    steamcmd - installs steamcmd"
    echo "    update - updates QL server files"
    echo "    run [server config file] [server id] - run server using specified config"
    echo "    monitor [server config file] [server id:optional] - run server in"
    echo "            auto-restart mode"
    echo "            * if no ID is given, all server will run in auto-restart mode"
    echo "            * auto-restart mode means that, if server quitsunexpectedly, it"
    echo "              will automatically restart"
    echo "    supervisor-update - disables all server managed by supervisord and"
    echo "                        performs an update"
fi
