#!/bin/bash
command_run() {
    if [[ $1 == '' || ! -f $1 ]]; then
        echo "You have to pass config location as parameter eg.:"
        echo "$0 run ~/myconfig server_id"
        exit 1
    fi

    if [[ $2 == '' || $2 -lt 0 ]]; then
        echo "You have to pass server ID you want to start"
        exit 1
    fi

    update_if_required

    . $1

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
