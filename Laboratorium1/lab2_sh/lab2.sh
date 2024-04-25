number=1
rm *.txt
rm web.html
for i in {00..99}; do
    for j in {000..999}; do
        curl -L "https://www.geonames.org/postalcode-search.html?q=$i-$j&country=PL" >web.html
        grep -Eo "[0-9]{2}-[0-9]{3}" web.html >greped.txt
        grep -Eo "[0-9]{2}().([0-9])+)?/[0-9]{2}(.([0-9])+)?" web.html >greped2.txt
        grep -Eo "</small></td><td>[a-zA-ZżźćńółęąśŻŹĆĄŚĘŁÓŃ ]+" web.html >greped3.txt
        line_number=1
        while IFS= read -r line; do
            if [ $line_number -eq 3 -a $line = "$i-$j" ]; then
                geo=$(head -n 1 greped2.txt)
                city=$(head -n 1 greped3.txt)
                if ! [[ -z $geo ]]; then
                    echo "$line" >>zip_codes.txt
                    echo "$geo" >>geographics.txt
                    echo "$city" >>cities.txt
                fi
            fi
            ((line_number++))
        done <greped.txt
    done
done
sed 's/<\/small><\/td><td>//' cities.txt >cities_final.txt
