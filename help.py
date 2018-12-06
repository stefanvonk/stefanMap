import sys


def help():
    print("Hello, this is the help function of honey-detect. Welcome! This script is created by Stefan Vonk, "
          "for purpose of honeypot detection.")
    print("This script is created to run on a Linux distribution.\n")
    print("You can run the following scan methods:")
    print("p    : Passive detection")
    print("a    : Active detection")
    print("f    : Full(active) network scan\n")
    print("For this python tool you must install the following linux tools:")
    print("sudo pip3 install paramiko")
    print("sudo apt-get install ssh")
    print("sudo apt-get install nmap")
    print("sudo apt-get install arp-scan")

    sys.exit(0)
