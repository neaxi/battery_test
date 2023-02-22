#!/bin/bash

#source venv/bin/activate

echo "Enter battery ID"
read battery_id

if [[ $1 = "venv" ]]; then
    venv/bin/python3 client.py $battery_id &
else
    python3 client.py $battery_id &
fi

# once the power supply is disconnected
while [[ $(cat "/sys/class/power_supply/AC/online") -eq 1 ]]; do
    echo "AC connected, waiting..."
    sleep 10
done

# load 1 core to 100%
# for more complex/multicore methods see following
# https://superuser.com/questions/443406/how-can-i-produce-high-cpu-load-on-a-linux-server
echo "Activating mild CPU stress"
cat /dev/zero >/dev/null
