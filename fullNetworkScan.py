import subprocess
import logging


def scanNetwork(ip):
    try:
        print("\nThe results of a full network scan on " + ip + "/24")
        # run nmap scan
        subprocess.run(["sudo", "nmap", "-T4", "-F", ip + "/24"])
        logging.info("The nmap scan was running without errors")
    # exception when nmap is not installed
    except Exception as e:
        logging.warning("The following error raise when running nmap: " + str(e))
        print("Error: please install nmap before run this full network scan. (Run 'sudo apt-get install nmap')")

    print("\n\nFor details about the process of scanning, check the logfile 'stefanMap.log'.\n")
