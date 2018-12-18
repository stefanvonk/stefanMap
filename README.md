# stefanMap
This tool is created by Stefan Vonk and does detection of honeypots and honeytokens. Using this tool is at your own risk!

The tool has two functionalities.

### 1. Honeypots
This function can be used to detect if a machine in a network is a honeypot.

It works with three detection levels:
1. Passive detection;
2. Active detection;
3. Local detection.

There is also a possibility to do a full network scan witch returns 
all networks machines with the open ports of every machine.

You can start the script by running stefanMap.py (passive and active scanning) and 
local.py (local scanning). You need to run this in Python 3 with root permissions.

This script has been tested on Ubuntu 18.04 and runs on the following dependencies:
- Python libraries:
    - paramiko
    - getmac
    - validators
- Ubuntu packages:
    - ssh
    - nmap
    - arp-scan
    - tshark

The script local.py doesn't have any dependencies.

This function implements especially the detection of a number of specific honeypot.
This honeypots are:
1. T-pot (from T-Mobile);
2. Kippo honeypot;
3. Cowrie honeypot;
4. Sshesame honeypot;
5. Modern Honeynetwork;
6. Dionaea honeypot.

### 2. Honeytokens
Another function of the tool is to detect whether a file is a honeytoken or not.
The tool implements especially the detection of three types of honeytokens from
the provider Canarytokens (https://canarytokens.org/generate).

These three types of honeytokens are:
1. PDF files;
2. Windows Folders;
3. Microsoft Word Documents.

This script can be started by running tokens/tokens.py.
You need to run this in Python 3 with root permissions.

This script has been tested on Windows 10 and runs on the following dependencies:
- Python libraries:
    - peepdf