#!/bin/bash
command_steamcmd() {
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
}
