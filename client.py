from string import Template
import logging
import sys
import subprocess
import json
import time
import datetime
import requests


INTERVAL = 10

# IP = input("Provide server IP: ")
IP = "127.0.0.1"
IP = "192.168.88.251"
SERVER = f"http://{IP}:5000"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DeltaTemplate(Template):
    delimiter = "%"


def strfdelta(tdelta, fmt):
    """timedelta formatter - https://stackoverflow.com/a/30536361/11534340"""
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = "{:02d}".format(hours)
    d["M"] = "{:02d}".format(minutes)
    d["S"] = "{:02d}".format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


class BatteryMonitor:
    def __init__(self, bid) -> None:
        self.status = None
        self.id = bid
        self.discharge_started = None
        self.data = None
        self.parse_data_from_system()

    def time_since_discharging(self):
        """calc and format how much time since the discharge process started"""
        if not self.discharge_started:
            return 0

        time_delta = datetime.datetime.now() - self.discharge_started
        timestamp = strfdelta(time_delta, "%H:%M:%S")
        return timestamp

    def collect_data(self):
        """collect data from system and extend them with ID and a timestamp"""
        hw_data = self.parse_data_from_system()
        self.data = {"ID": self.id, "timestamp": self.time_since_discharging()}

        self.data.update(hw_data)
        self.print_status()

    def print_status(self):
        """collect basic info and print it out for the user"""
        try:
            print(
                "\t".join(
                    [
                        self.data["timestamp"],
                        self.data["POWER_SUPPLY_STATUS"],
                        self.data["POWER_SUPPLY_CAPACITY"],
                    ]
                )
            )
        except KeyError:
            pass

    def parse_data_from_system(self):
        """collect battery data from /sys/class/power_supply/BAT0/uevent
        if battery started discharging (ie AC disconnected), log the timestamp
        as a start time, so it can be measured how long it ran on battery
        """
        logger.debug("Collecting data")
        procs = subprocess.check_output(["cat", "/sys/class/power_supply/BAT0/uevent"])
        data = {}
        for field in procs.decode().split("\n"):
            if not field:
                continue
            fsplit = field.split("=")
            data[fsplit[0]] = fsplit[1]
        try:
            if (
                not self.discharge_started
                and data["POWER_SUPPLY_STATUS"] == "Discharging"
            ):
                print("Discharging detected!")
                self.discharge_started = datetime.datetime.now()
        except BaseException as exc:
            print("Discharge detection failed")
            print(exc)

        return data

    def send_data_to_server(self):
        """format the collected data as JSON and send them to a server"""
        logger.debug("Updating server")

        headers = {"Content-Type": "application/json"}
        data = json.dumps(self.data)

        try:
            resp = requests.post(SERVER, headers=headers, data=data, timeout=5)
            if resp.status_code == 200:
                print("200 OK")
            else:
                print(resp.status_code)
        except BaseException as exc:
            print(exc)


# create an instance and run the loop
BAT_ID = sys.argv[1]
print(f"Battery ID: {BAT_ID}")
bat = BatteryMonitor(BAT_ID)

while True:
    bat.collect_data()
    bat.send_data_to_server()
    time.sleep(INTERVAL)
