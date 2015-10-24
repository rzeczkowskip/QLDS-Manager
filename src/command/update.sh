#!/bin/bash
command_update() {
    if [[ ! -f $STEAMCMD_DIR/steamcmd.sh || ! -x $STEAMCMD_DIR/steamcmd.sh ]]; then
        echo "Cannot find SteamCMD"
        exit 1
    fi

    echo "Updating QLDS files"
    exec $STEAMCMD_DIR/steamcmd.sh +login anonymous +force_install_dir $QL_DIR +app_update $QL_APPID +quit
    echo "QLDS updated"
}
