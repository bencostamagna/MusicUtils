#! /bin/bash
#
# filetypes.sh
# Copyright (C) 2018 chupacabra <chupacabra@diziet>
#
# Distributed under terms of the GPL3 license.
#

if [ $# -ne 1 ]
then
    exit 1
fi

folder="$1"
declare -A filetypes
while read l
do
    if [ -f "$l" ]
    then
	type=$(echo "$l" | awk -F"." '{print $NF}')
	
	if [[ "$l" != *.* ]] || [ ${#type} -ge 6 ]
	then
	    echo "Error: $l"
	else
	    if [ -v "filetypes[$type]" ]
	    then
		filetypes[$type]=$((${filetypes[$type]} + 1))
	    else
		filetypes[$type]=1
	   fi
       fi
    fi
done < <(find $folder)

for t in "${!filetypes[@]}"
do
    echo "$t -> ${filetypes[$t]}"
done | sort -rn -k3

