#!/bin/bash
command_run() {
    if [[ $2 == '' || $2 -lt 0 ]]; then
        echo "You have to pass server ID you want to start"
        exit 1
    fi

    load_server_list "$1"

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
        exec "$QL_DIR/$QL_EXEC" "$SERVER_CONFIG"
    fi
}
