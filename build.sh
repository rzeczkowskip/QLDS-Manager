#!/bin/bash
QLDS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
QLDS_OUT="$QLDS_DIR/qlds.sh"

FILES="src/config.sh
src/check_wget.sh
src/update_check.sh
src/list_load.sh
src/command/*
src/init.sh"

OUT="#!/bin/bash
# https://github.com/rzeka/QLDS-Manager
"

for F in $FILES; do
    #echo $F
    OUT="$OUT
$(cat $F | (read; cat))"
done

echo "$OUT" > "$QLDS_OUT"
chmod +x "$QLDS_OUT"
