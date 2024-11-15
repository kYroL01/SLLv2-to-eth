[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)
[![Generic badge](https://img.shields.io/badge/Python-green.svg)](https://www.python.org/)
[![Generic badge](https://img.shields.io/badge/Networking-orange.svg)](networking)


# SLLv2-to-eth
Convert pcap from SLL2 (Linux cooked capture v2) to Ethernet

## Prerequisite
To run the code provided, you need to install Python and the **Scapy** library (https://scapy.net)

1. Install Python
```bash
sudo apt update
sudo apt install python3 python3-pip
```
2. Install Scapy
```bash
sudo pip3 install scapy
```

## Run
```
python3 sllv2-to-eth.py input.pcap output.pcap --src-mac aa:bb:cc:dd:ee:11 --dst-mac ff:ee:dd:cc:bb:22
```
NOTE: if you don't specify `--src-mac` and `--dst-mac` the default values are `aa:bb:cc:dd:ee:ff` and `ff:ee:dd:cc:bb:aa`

### Disclaimer
This script intends to cover the problem of importing pcap with DLT_LINUX_SLL2 as Data Link layer, which is not recognized for some application
