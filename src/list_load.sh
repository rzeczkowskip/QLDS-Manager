#!/bin/bash
load_server_list() {
    if [[ $1 == '' || ! -f "$1" ]]; then
        echo "You have to pass server-list file location as parameter eg.:"
        echo "$0 run ~/myconfig server_id"
        exit 1
    fi

    . "$1"
}
