#!/bin/bash
if [[ $HOME == '' ]]; then
    echo "No home dir available"
    exit 1
fi

STEAMCMD_DIR="$HOME/steamcmd"
QL_DIR="$HOME/QLserver"

QLDS_MANAGER_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

QL_APPID="349090"
STEAMCMD_URL="https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
STEAMCMD_ARCHIVE="steamcmd_linux.tar.gz"

STEAMAPI_VERSION_CHECK="https://api.steampowered.com/ISteamApps/UpToDateCheck/v1/?&format=json&appid=282440&version="
