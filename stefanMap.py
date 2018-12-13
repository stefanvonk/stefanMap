import ipaddress
import logging
import subprocess
import sys

import active
import fullNetworkScan
import help
import passive


def arp_scan():
    logging.info("Start passive arp scan")

    try:
        print("The results of a passive arp scan on the network of your machine:")
        # run arp-scan
        subprocess.call(["sudo", "arp-scan", "-l"])
        logging.info("The passive arp scan was running without errors")
    # exception when arp-scan is not installed
    except Exception as err:
        logging.warning("The following error raise when running arp-scan: " + str(err))
        print("Error: please install arp-scan before run this full network scan. "
              "(Run 'sudo apt-get install arp-scan')\n")

    logging.info("End passive arp scan")


def get_ip():
    # ask user to enter ip address for scanning
    ip = input("Enter a valid host IP address for scanning: ")
    try:
        # check ip address
        ipaddress.ip_address(ip)
        logging.info("Entered host IP is: " + str(ip))
        # return ip address
        return ip
    # exception when the entered ip is not a IPv4 or IPv6 address
    except:
        print("Your input does not appear to be an IPv4 or IPv6 address, please try again.")
        return get_ip()


def process_input():
    # choose scan method
    print("\nChoose your scan method:")
    choise = input("p    : passive scan\na    : active scan\nf    : full (active) network scan"
                   "\n\nMake your choice: ")
    if choise == "p":
        logging.info("Passive detection selected")
        ip = get_ip()
        passive.passive(ip)
    elif choise == "a":
        logging.info("Active detection selected")
        ip = get_ip()
        active.active(ip)
    elif choise == "f":
        logging.info("Full (active) network scan selected")
        ip = get_ip()
        fullNetworkScan.scan_network(ip)
    else:
        logging.info("Help function is showing")
        help.help_function()


def run_again():
    print("Do you want to run one of the scan methods of stefanMap again or close the program?")
    again = input("Typ 'a' for run again or 'c' for close:")

    if again == "a":
        logging.info("Run stefanMap again selected")
        process_input()
        run_again()
    elif again == "c":
        logging.info("Close stefanMap selected")
        sys.exit(0)
    else:
        print("Your input is not true, please try again.")
        run_again()


def stefanmap():
    # setup logging: logfile stefanMap.log, add date and time to logging, add log level to the logging
    logging.basicConfig(filename='stefanMap.log', format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    # append data to logfile
    logging.info("stefanMap started")

    # run an full network arp scan
    arp_scan()
    # read choise and execute a function
    process_input()
    # run the program again
    run_again()


try:
    stefanmap()
# except when pressed ctrl + c
except KeyboardInterrupt as e:
    logging.warning("The following error raise: Ctrl + c is pressed")
    print("\nClosing stefanMap...")
    logging.info("stefanMap stopped\n")
    sys.exit(0)
# except when system exit
except SystemExit as e:
    print("Closing stefanMap...")
    logging.info("stefanMap finished\n")
    sys.exit(0)
