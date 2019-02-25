#!/usr/bin/env bash

EXTENSION=".png"
ASSETS_PATH="data/assets"

case $1 in
"cellule")
    find $ASSETS_PATH/cellule -name "*$EXTENSION" -type f -delete
    echo "cellule directory cleaned"
    ;;
"out")
    find $ASSETS_PATH/out -name "*$EXTENSION" -type f -delete
    echo "out directory cleaned"
    ;;
"*")
    find $ASSETS_PATH -name "*$EXTENSION" -type f -delete
    find $ASSETS_PATH -name "*$EXTENSION" -type f -delete
    echo "directories cleaned"
    ;;
esac






