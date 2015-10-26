#!/bin/bash
command_monitor() {
    load_server_list "$1"

    #If no ID is passed, get all IDs and re-run minitor for each id
    if [[ $2 == '' ]]; then
        #get keys from $SERVER
        for ID in ${!SERVER[*]}; do
            $0 monitor "$1" "$ID" &
        done
    else
        until $0 run "$1" "$2"; do
            echo "Restarting server $2"
            sleep 1 # sleep, so if server always exits unexpectedly, we won't kill server
        done
    fi
}
