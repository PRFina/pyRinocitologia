#!/usr/bin/env bash
# 3 lines shell script to generate unique dataset id based on a sha1 hashed timestamp
timestamp=$(date +'%d/%m/%Y %H:%M:%S')
hash=$(echo $timestamp | sha1sum) #read from stdin
echo "Generated dataset id:" ${hash//-/}  "(copy and paste to metainfo.json file)" #remove "-" literal from sha1sum output

