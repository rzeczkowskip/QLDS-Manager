#!/bin/bash
check_wget () {
  if [ ! -x "$(command -v wget)" ]; then
    return 1
  else
    echo "\"wget\" is not installed. Please install \"wget\" and re-run this script."
    exit 1
  fi
}
