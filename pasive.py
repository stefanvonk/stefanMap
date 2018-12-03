import subprocess

def pasive():
    network = "192.168.11.0/24"
    p = subprocess.Popen(["sudo", "nmap", "-sP", network], stdout=subprocess.PIPE)

    for line in p.stdout:
        print(line)