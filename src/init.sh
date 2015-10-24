#!/bin/bash
# https://github.com/rzeka/QLDS-Manager

if [[ $1 == "steamcmd" ]]; then
    command_steamcmd
elif [[ $1 == "update" ]]; then
    command_update
elif [[ $1 == "supervisor-update" ]]; then
    command_supervisor_update
elif [[ $1 == "run" ]]; then
    command_run $2 $3
else
    echo "Available commands: steamcmd, update, run"
    echo "    $0 steamcmd - installs steamcmd"
    echo "    $0 update - updates QL server files"
    echo "    $0 run [server config file] [server id] - run server using specified config and id"
    echo "    $0 supervisor-update - disables all server managed by supervisord and performs an update"
fi
