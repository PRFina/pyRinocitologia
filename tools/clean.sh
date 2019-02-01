#!/usr/bin/env bash

EXTENSION=".png"

case "$0" in
"cellule")
    find cellule -name "*$EXTENSION" -type f -delete
    echo "cellule directory cleaned"
    ;;
"out")
    find out -name "*$EXTENSION" -type f -delete
    echo "out directory cleaned"
    ;;
"*")
    find cellule -name "*$EXTENSION" -type f -delete
    find out -name "*$EXTENSION" -type f -delete
    echo "directories cleaned"
    ;;
esac






