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
`start_client.sh` - single launchpoint for the client. Collects battery ID and loads CPU when it detects AC has been disconnected.  
`pwr.sh` - attempt to prevent screen sleep and locking. As the live linux flashdrive was disconnected once client started, it was needed to ensure no new application will start (ie lock screen). For best result verify the setting has changed in power manager GUI.

`csv_split.sh` - creates a separate .csv file for each battery ID
`master_csv.py` - creates a table suitable for a graph; time series column + data series columns