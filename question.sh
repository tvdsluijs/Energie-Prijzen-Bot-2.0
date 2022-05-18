PS3='Build What?: '
options=("DEV" "ACC" "PROD" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "DEV")
            echo "you chose choice DEV"
            break
            ;;
        "ACC")
            echo "you chose choice ACC"
            break
            ;;
        "PROD")
            echo "you chose choice $REPLY which is $opt"
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done

echo "Yes you want $opt"