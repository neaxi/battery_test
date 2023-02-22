# Battery logger

## Why

Bunch of batteries for Dell series E6440 had to be tested to figure out which should be thrown away and which can still be used. Therefore we had to charge each of them, put them under load and measure how long they can hold.  
To charge, stress test and measure the battery 9 laptops were used, each booted live linux from a flash drive reporting battery data to a server.  
Kali was used as it contains all required python libs by default => no additional setup needed.

## How

`server.py` - Flask server with a single endpoint.
Expects `.json` payload and stores it within `.csv` output file.  

`client.py` - executed on every client. Collects battery info provided by system, adds a battery ID and a timer when battery starts discharging and sends the data to a server.  

`install.sh` - ensures flask and requests libs are available  
`start_server.sh` - single launchpoint for the server  
`start_client.sh` - single launchpoint for the client. Collects battery ID (expects integer) and loads CPU when it detects AC has been disconnected.  
`pwr.sh` - attempt to prevent screen sleep and locking. As the live linux flashdrive was disconnected once client started, it was needed to ensure no new application will start (ie lock screen). For best result verify the setting has changed in power manager GUI.

`csv_split.sh` - creates a separate .csv file for each battery ID  
`master_csv.py` - creates a table suitable for a graph; time series column + data series columns

## Sample outputs

`server.py` output

```csv
ID;timestamp;POWER_SUPPLY_NAME;POWER_SUPPLY_TYPE;POWER_SUPPLY_STATUS;POWER_SUPPLY_PRESENT;POWER_SUPPLY_TECHNOLOGY;POWER_SUPPLY_CYCLE_COUNT;POWER_SUPPLY_VOLTAGE_MIN_DESIGN;POWER_SUPPLY_VOLTAGE_NOW;POWER_SUPPLY_CURRENT_NOW;POWER_SUPPLY_CHARGE_FULL_DESIGN;POWER_SUPPLY_CHARGE_FULL;POWER_SUPPLY_CHARGE_NOW;POWER_SUPPLY_CAPACITY;POWER_SUPPLY_CAPACITY_LEVEL;POWER_SUPPLY_MODEL_NAME;POWER_SUPPLY_MANUFACTURER;POWER_SUPPLY_SERIAL_NUMBER
1;00:19:33;BAT0;Battery;Discharging;1;Li-ion;0;11100000;10890000;2184000;5600000;2188000;1498000;68;Normal;DELL MKD6223;SMP;1229
5;0;BAT0;Battery;Charging;1;Li-ion;0;11100000;12290000;2683000;6000000;4398000;3636000;82;Normal;DELL HTX4D2A;SMP;1988
4;0;BAT0;Battery;Charging;1;Li-ion;0;11100000;13033000;216000;5900000;3354000;3320000;98;Normal;DELL 3VJJC46;Samsung SDI;21930
3;00:14:31;BAT0;Battery;Discharging;1;Li-ion;0;11100000;11664000;2165000;6000000;3600000;3084000;85;Normal;DELL HTX4D2A;SMP;2879
6;00:01:30;BAT0;Battery;Discharging;1;Li-ion;0;11100000;12226000;1979000;6000000;5644000;5592000;99;Normal;DELL 4KFGD42;LGC-LGC3.0;31955
2;0;BAT0;Battery;Charging;1;Li-ion;0;11100000;12674000;1177000;5600000;1452000;1437000;98;Normal;DELL 5CGM423;Samsung SDI;13118
```

![server csv output](/samples/server_output.png)  

After parsing server output with `master_csv.py`:  
![graph output](/samples/master_csv.png)  
