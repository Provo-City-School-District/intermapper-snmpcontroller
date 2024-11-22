# intermapper-snmpcontroller
Simple flask app to interact with OID's using snmpset to manipulate devices

## Requirements
- Python 3.6+
- Flask
- PySNMP(optional)
- snmp

## Installation
1. Clone the repository
2. Install the requirements
```bash
sudo apt install python3 python3-pip python3-pysnmp4 python3-flask snmp
```
You can just run the app with the following command:
```bash
python3 app.py
```
I like to make a service personally, so I can run it in the background. Here is an example of a service file:
```bash
[Unit]
Description=SNMP App
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/intermapper-snmpcontroller/app.py
WorkingDirectory=/home/pi/intermapper-snmpcontroller
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
You can save this file in /etc/systemd/system/snmp-app.service and then run the following commands:
```bash
sudo systemctl snmp-app enable
sudo systemctl snmp-app start
```
This will start the service and run it in the background. You can check the status/restart/stop the service with the following command:
```bash
#status
sudo systemctl status snmpapp
#restart
sudo systemctl restart snmpapp
#stop
sudo systemctl stop snmpapp
```
## Usage
the application expects your scripts you want to run to be in the scripts folder. The scripts hierarchy should be in the following format:
```bash
scripts/
├── location1/
│   ├── script1.py
│   └── script2.py
├── location2/
│   ├── script3.py
│   └── script4.py
└── location3/
    ├── script5.py
    └── script6.py
```
The scripts should be in the following format:
Simplified commands sending through system
```python
from time import sleep
import os
import sys

#while True:
os.system('snmpset -v 3 -u group -l AuthPriv -a SHA -A password -x AES -X password IP OID i value')
sleep(30)
os.system('snmpset -v 3 -u group -l AuthPriv -a SHA -A password -x AES -X password ip ODI i value')
```
using pysnmp
```python
import time
from pysnmp.hlapi import *

def snmp_set(target, username, auth_password, priv_password, oid, value, data_type):
    # Using SNMPv3 with User-based Security Model (USM) with SHA and AES
    iterator = setCmd(
        SnmpEngine(),
        UsmUserData(
            username, 
            authKey=auth_password,  # Use authKey for authentication password
            authProtocol=usmHMACSHAAuthProtocol,  # SHA for authentication
            privKey=priv_password,  # Use privKey for privacy password
            privProtocol=usmAesCfb128Protocol  # AES for encryption
        ),
        UdpTransportTarget((target, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid), data_type(value))
    )
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(f"Error: {errorIndication}")
    elif errorStatus:
        print(f"Error: {errorStatus.prettyPrint()} at {errorIndex}")
    else:
        for varBind in varBinds:
            print(f"Success: {varBind}")

def run_script_with_delay(target, username, auth_password, priv_password, oid, data_type):
    # First value
    print("shutting down port...")
    snmp_set(target, username, auth_password, priv_password, oid, 2, data_type)  # Pass 2
    time.sleep(30)  # Wait for 30 seconds

    # Second value
    print("starting port...")
    snmp_set(target, username, auth_password, priv_password, oid, 1, data_type)  # Pass 1

if __name__ == "__main__":
    # Replace these values with your SNMPv3 parameters
    target_ip = "ip"  # Target device IP
    username = "group"  # SNMPv3 username/group
    auth_password = "password"  # Authentication password (SHA)
    priv_password = "password"  # Privacy password (AES)
    oid = "OID"  # Object identifier
    data_type = Integer  # Correct data type for setting an integer

    # Run the script with delay
    run_script_with_delay(target_ip, username, auth_password, priv_password, oid, data_type)

```
