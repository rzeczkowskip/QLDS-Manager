#!/bin/bash
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
