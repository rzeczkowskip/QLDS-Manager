#!/bin/bash
command_steamcmd() {
    if [[ -d "$STEAMCMD_DIR" ]]; then
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

        echo "Please wait, while packages are checked..."

        $SUDO dpkg --add-architecture i386
        $SUDO apt-get -qq update
        $SUDO apt-get -q install lib32stdc++6
    fi

    mkdir "$STEAMCMD_DIR"
    cd "$STEAMCMD_DIR"

    if [[ check_wget ]]; then
        wget "$STEAMCMD_URL"
    elif [[ check_curl ]]; then
        curl -O "$STEAMCMD_URL"
    else
        cd "$QLDS_MANAGER_DIR"
        rm -r "$STEAMCMD_DIR"
        download_error
    fi

    tar zxf "$STEAMCMD_ARCHIVE"
    chmod +x "$STEAMCMD_DIR/steamcmd.sh"

    echo "SteamCMD installed in $STEAMCMD_DIR"
}
