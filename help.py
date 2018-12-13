import sys


def help():
    print("\n\nHello, this is the help function of stefanMap. Welcome! This script is created by Stefan Vonk, "
          "for purpose of honeypot detection.")
    print("This script is tested on an Ubuntu 18.04 distribution.\n")
    print("You can run the following scan methods:")
    print("p    : Passive detection")
    print("a    : Active detection")
    print("f    : Full (active) network scan\n")
    print("Run this tool as root!\n")
    print("For this python tool you need the following dependencies:")
    #print("sudo pip3 install paramiko")
    #print("sudo pip3 install getmac")
    #print("sudo pip3 install validators")
    #print("sudo apt-get install ssh")
    print("sudo apt-get install nmap")
    #print("sudo apt-get install arp-scan")
    #print("sudo apt-get install tshark")

    sys.exit(0)
