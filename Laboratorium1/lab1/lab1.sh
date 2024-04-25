#!/bin/bash
curl -L p.lodz.pl > web.html 
grep -Eo "(https://www\.|http://www\.|https://|http://)([a-zA-Z0-9./])+" web.html > greped.txt #regular expression
sort greped.txt > sorted.txt
line_number=1

while IFS= read -r line; do
    if [ $line_number -eq 26 ] || [ $line_number -eq 33 ]; then
        echo "Line $line_number: $line"
    fi
    ((line_number++))
done < sorted.txt