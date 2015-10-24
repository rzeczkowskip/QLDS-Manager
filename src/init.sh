#!/bin/bash
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
