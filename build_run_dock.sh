#!/bin/bash
tag_name=$(cat src/VERSION.TXT)
data_folder=$(pwd)/data
log_folder=$(pwd)/logging

PS3='Build What?: '
options=("dev" "acc" "prod" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "dev")
            echo "your choice is DEV"
            break
            ;;
        "acc")
            echo "your choice is ACC"
            break
            ;;
        "prod")
            echo "your choice is PROD"
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done

docker build --target $opt -t energie-prijzen-bot${tag_name} .

docker run -it -d -v $data_folder:/src/data -v $log_folder:/src/logging -e TZ=Europe/Amsterdam energie-prijzen-bot${tag_name}

docker ps -a