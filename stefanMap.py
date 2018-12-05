import passive
import active
import fullNetworkScan
import help
import logging
import ipaddress

def getIP():
    # ask user to enter ip address for scanning
    ip = input("Enter a valid host IP address for scanning: ")
    logging.info("Entered host IP is: " + str(ip))
    try:
        # check ip address
        ipaddress.ip_address(ip)
        # return ip address
        return ip
    # exception when the entered ip is not a IPv4 or IPv6 address
    except Exception as e:
        logging.warning("The following error raise when checking the IP address: " + str(e))
        print("Your input does not appear to be an IPv4 or IPv6 address, please try again.")
        getIP()


def stefanMap():
    # setup logging: logfile stefanMap.log, add date and time to logging, add loglevel to the logging
    logging.basicConfig(filename='stefanMap.log', format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    # append data to logfile
    logging.info("stefanMap started")

    # choose scan method
    print("Choose your scan mehod:")
    choise = input("p    : passive scan\na    : active scan\nf    : full network scan"
                   "\n\nMake your choice: ")

    if choise == "p":
        logging.info("Passive detection selected.")
        ip = getIP()
        passive.passive(ip)
    elif choise == "a":
        logging.info("Active detection selected.")
        ip = getIP()
        active.active(ip)
    elif choise == "f":
        logging.info("Full network scan selected.")
        ip = getIP()
        fullNetworkScan.scanNetwork(ip)
    else:
        logging.info("Help function is showing.")
        help.help()

    print("\n\nFor details about the process check the logfile stefanMap.log.")

    # append data to logfile
    logging.info("stefanMap Finished\n")


stefanMap()
