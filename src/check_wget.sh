#!/bin/bash
check_wget () {
  if [ ! -x "$(command -v wget)" ]; then
    return 0
  else
    return 1
  fi
}

check_curl() {
    if [ ! -x "$(command -v curl)" ]; then
        return 0
    else
        return 1
    fi
}

download_error() {
    echo "Neither \"curl\" nor \"wget\" is installed."
    echo "Please install one and re-run this script."
    exit 1
}
