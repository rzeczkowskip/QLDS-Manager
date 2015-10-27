#!/bin/bash
check_outdated() {
    QL_VERSION=$(strings $QL_DIR/qzeroded.x86 | grep "linux-i386" | awk '{print $1}' ORS='')
    QL_UP_TO_DATE="false"

    if [ check_wget ]; then
        QL_UP_TO_DATE=$(wget -qO- $STEAMAPI_VERSION_CHECK$QL_VERSION | grep "up_to_date" | awk '{print $2}' RS=',' ORS='')
    elif [ check_curl ]; then
        QL_UP_TO_DATE=$(curl -s $STEAMAPI_VERSION_CHECK$QL_VERSION | grep "up_to_date" | awk '{print $2}' RS=',' ORS='')
    else
        download_error
    fi

    if [[ $QL_UP_TO_DATE == 'false' ]]; then
        echo 1
    else
        echo 0
    fi
}

update_if_required() {
    if [[ check_outdated -eq 1 ]]; then
        "$0" update
    fi
}
