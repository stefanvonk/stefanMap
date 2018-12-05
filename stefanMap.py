import pasive
import active
import fullNetworkScan
import help
import logging


def stefanMap():
    # setup logging: logfile stefanMap.log, add date and time to logging, add loglevel to the logging
    logging.basicConfig(filename='stefanMap.log', format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    # append data to logfile
    logging.info("stefanMap started")

    # choose scan method
    print("Choose your scan mehod:")
    choise = input("p    : pasive scan\na    : active scan\nf    : full network scan"
                   "\n\nMake your choice: ")

    if choise == "p":
        logging.info("Pasive detection selected.")
        pasive.pasive()
    elif choise == "a":
        logging.info("Active detection selected.")
        active.active()
    elif choise == "f":
        logging.info("Full network scan selected.")
        fullNetworkScan.scanNetwork()
    else:
        logging.info("Help function is showing.")
        help.help()

    print("\n\nFor details about the process check the logfile stefanMap.log.")

    # append data to logfile
    logging.info("stefanMap Finished\n")


stefanMap()
