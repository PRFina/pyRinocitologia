#!/usr/bin/env bash

EXTENSION=".png"

case $1 in
"cellule")
    find assets/cellule -name "*$EXTENSION" -type f -delete
    echo "cellule directory cleaned"
    ;;
"out")
    find assets/out -name "*$EXTENSION" -type f -delete
    echo "out directory cleaned"
    ;;
".")
    find assets/cellule -name "*$EXTENSION" -type f -delete
    find assets/out -name "*$EXTENSION" -type f -delete
    echo "directories cleaned"
    ;;
esac






