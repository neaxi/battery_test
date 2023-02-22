#!/bin/bash

#set -x

FOLDER=batteries
COMA_INSTEAD_SEMI=1
DISCHARGE=1

if [[ -z $1 ]]; then
    echo 'No source file provided. Usage "csv_split.sh [source_file]"'
    exit
else
    echo "Loading data from $1"
fi

mkdir -p $FOLDER

# find max battery ID
max_id=$(cat "$1" | cut -d ";" -f1 | sort -n | uniq | tail -n 1)

create_individual_battery_files() {
    for i in $(seq "$max_id"); do
        echo "Processing ID $i"

        printf -v fileno "%02d" "$i"
        filename="$fileno.csv"
        header=$(head -n 1 $1)
        data=$(grep "^$i;" <"$1")

        if [[ COMA_INSTEAD_SEMI -eq 1 ]]; then
            header="${header//;/,}"
            data="${data//;/,}"
        fi

        if [[ DISCHARGE -eq 1 ]]; then
            data=$(echo "$data" | grep "Discharging")
        fi

        echo "$header" >"$FOLDER\\$filename"
        echo "$data" >>"$FOLDER\\$filename"

    done
}

create_individual_battery_files "$@"
