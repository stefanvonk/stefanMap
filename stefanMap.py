import pasive
import active
import onSystem
import nmapSystemScan
import help
import logging

# definieren variabelen

def stefanMap():
    logging.basicConfig(filename='stefanMap.log',format='%(asctime)s %(levelname)-8s %(message)s',level=logging.INFO,datefmt='%Y-%m-%d %H:%M:%S')
    logging.info("stefanMap started")

    choise = input("p    : pasive scanning\na    : active scanning\no    : on system scanning\nf    : full nmap system scan\n\nMake your choice: ")

    if choise == "p":
        result = pasive.pasive()
    elif choise == "a":
        result = active.active()
    elif choise == "o":
        onSystem.onSystem()
    elif choise == "f":
        result = nmapSystemScan.scanSystem()
    else:
        help.help()

    if "result" in locals() or "result" in globals():
        print(result)

    logging.info("stefanMap Finished")

stefanMap()