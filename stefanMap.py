import pasive
import active
import onSystem
import nmapSystemScan
import help
import logging

# definieren variabelen

def stefanMap():
    # setup logging: logfile stefanMap.log, add date and time to logging, add loglevel to the logging
    logging.basicConfig(filename='stefanMap.log',format='%(asctime)s %(levelname)-8s %(message)s',level=logging.INFO,datefmt='%Y-%m-%d %H:%M:%S')
    # append data to logfile
    logging.info("stefanMap started")

    choise = input("p    : pasive scanning\na    : active scanning\no    : on system scanning\nf    : full nmap network scan\n\nMake your choice: ")

    if choise == "p":
        logging.info("Pasive detection selected.")
        result = pasive.pasive()
    elif choise == "a":
        logging.info("Active detection selected.")
        result = active.active()
    elif choise == "o":
        logging.info("Local detection selected.")
        onSystem.onSystem()
    elif choise == "f":
        logging.info("Full nmap network scan selected.")
        result = nmapSystemScan.scanSystem()
    else:
        logging.info("Help function is showing.")
        help.help()

    if "result" in locals() or "result" in globals():
        print(result)

    print("This is an indication whether there is a honeypot running on the IP you have entered. For details check the logfile stefanMap.log")

    # append data to logfile
    logging.info("stefanMap Finished")

stefanMap()