# Make sure python can see the miflora module
import sys
sys.path.append("/home/pi/miflora")

from miflora.miflora_poller import MiFloraPoller
from miflora.backends.bluepy import BluepyBackend
from datetime import datetime
import time
import json
import requests
from configparser import ConfigParser


# Read config file
config = ConfigParser()
config.read('raspberrypi.cfg')
mac = config.get('MiFlora', 'mac')
url = config.get('Flask', 'url')

# Take measurement
poller = MiFloraPoller(mac, BluepyBackend)
poller.fill_cache()
measurement = poller._parse_data()

# Add timestamp
measurement["timestamp"] = str(datetime.utcnow())

# Append to a csv file for the device
csvfile = "/home/pi/plant_monitor/measurements/{}.csv".format(mac.replace(':', ''))
with open(csvfile, "a") as f:
    # Make sure the entries are in the correct order
    f.write(measurement["timestamp"] + ", " +
            measurement["moisture"] + ", " +
            measurement["temperature"] + ", " +
            measurement["conductivity"] + ", " +
            measurement["light"] + "\n")

# Add device id
measurement["device"] = mac

# Upload to server
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
requests.post(url + "/measurement", data=json.dumps(measurement), headers=headers)
