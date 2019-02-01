#!/usr/bin/env bash

folders=("eosinofili" "epiteliali" "linfociti" "mastcellule" "mucipare" "neutrofili" "others")

cd ..
for folder in "${folders[@]}"; do
    mkdir out/$folder
done
