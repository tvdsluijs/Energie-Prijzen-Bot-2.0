#!/bin/bash

versie=$(cat src/VERSION.TXT)

echo 'Geef een omschrijving:'
read omschrijving

echo 'De huidige versie is' ${versie}
echo 'Geef de nieuwe versie op:'
read nieuwnummer

echo 'Nieuwe versie:' ${nieuwnummer}
echo ${nieuwnummer} > src/VERSION.TXT
echo 'Versie opgeslagen!'

# datum = date +"%dth %B, %Y"
datum=$( date '+%dth %B, %Y' )

sed -i '' "/Versiegeschiedenis/ a\\
\\
${datum} - versie: ${nieuwnummer} \\
- ${omschrijving} \\
" README.md

git add .
git commit -m "${omschrijving}"
git push

read -r -p "Tag deze commit? [Y/n] " input

case $input in
      [yY][eE][sS]|[yY])
            git tag ${nieuwnummer} -a -m "${omschrijving}"
            git push origin --tags
            ;;
      [nN][oO]|[nN])
            echo "Okay, dan zijn we klaar"
            ;;
      *)
            echo "Foute invoer, sorry."
            exit 1
            ;;
esac