import subprocess
import sys
import passive
import active
import fullNetworkScan
import help
import logging
import ipaddress


def arpScan():
    logging.info("Start passive arp scan")

    try:
        print("The results of a passive arp scan on the network of your machine:")
        # run arp-scan
        subprocess.call(["sudo", "arp-scan", "-l"])
        logging.info("The passive arp scan was running without errors")
    # exception when arp-scan is not installed
    except Exception as e:
        logging.warning("The following error raise when running arp-scan: " + str(e))
        print("Error: please install arp-scan before run this full network scan. "
              "(Run 'sudo apt-get install arp-scan')\n")

    logging.info("End passive arp scan")


def getIP():
    # ask user to enter ip address for scanning
    ip = input("Enter a valid host IP address for scanning: ")
    try:
        # check ip address
        ipaddress.ip_address(ip)
        logging.info("Entered host IP is: " + str(ip))
        # return ip address
        return ip
    # exception when the entered ip is not a IPv4 or IPv6 address
    except Exception as e:
        print("Your input does not appear to be an IPv4 or IPv6 address, please try again.")
        return getIP()


def processInput():
    # choose scan method
    print("\nChoose your scan mehod:")
    choise = input("p    : passive scan\na    : active scan\nf    : full (active) network scan"
                   "\n\nMake your choice: ")
    if choise == "p":
        logging.info("Passive detection selected")
        ip = getIP()
        passive.passive(ip)
    elif choise == "a":
        logging.info("Active detection selected")
        ip = getIP()
        active.active(ip)
    elif choise == "f":
        logging.info("Full (active) network scan selected")
        ip = getIP()
        fullNetworkScan.scanNetwork(ip)
    else:
        logging.info("Help function is showing")
        help.help()


def runAgain():
    print("Do you want to run one of the scan methods of stefanMap again or close the program?")
    again = input("Typ 'a' for run again or 'c' for close:")

    if again == "a":
        logging.info("Run stefanMap again selected")
        processInput()
        runAgain()
    elif again == "c":
        logging.info("Close stefanMap selected")
        sys.exit(0)
    else:
        print("Your input is not true, please try again.")
        runAgain()


def stefanMap():
    # setup logging: logfile stefanMap.log, add date and time to logging, add loglevel to the logging
    logging.basicConfig(filename='stefanMap.log', format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    # append data to logfile
    logging.info("stefanMap started")

    #TODO check for installation of ssh, nmap and arp-scan

    # run an full network arp scan
    arpScan()
    # read choise and execute a function
    processInput()
    # run the program again
    runAgain()

try:
    stefanMap()
# except when pressed ctrl + c
except KeyboardInterrupt as e:
    logging.warning("The following error raise: " + str(e))
    print("\nClossing stefanMap...")
    logging.info("stefanMap stopped\n")
    sys.exit(0)
# except when system exit
except SystemExit as e:
    logging.warning("The following error raise: " + str(e))
    print("Clossing stefanMap...")
    logging.info("stefanMap finished\n")
    sys.exit(0)