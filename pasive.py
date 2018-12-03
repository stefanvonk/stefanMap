import subprocess
from netaddr import IPNetwork

def pasive():
    network = "192.168.1.0/24"
    p = subprocess.Popen(["sudo", "nmap", "-sP", network], stdout=subprocess.PIPE)

    for line in p.stdout:
        print(line)