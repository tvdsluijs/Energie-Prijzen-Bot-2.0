#!/bin/bash
tag_name=$(cat src/VERSION.TXT)
data_folder=$(pwd)/data
log_folder=$(pwd)/logging

docker build -t energie-prijzen-bot${tag_name} .

docker run -it -d -v $data_folder:/src/data -v $log_folder:/src/logging -e TZ=Europe/Amsterdam energie-prijzen-bot${tag_name}

docker ps -a