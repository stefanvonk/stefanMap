import subprocess
import logging


def scanNetwork(ip):
    print("\nFor this full network scan you need a local nmap installation. (Run 'sudo apt-get install nmap')")

    try:
        # run nmap scan
        subprocess.run(["sudo", "nmap", "-sP", ip + "/24"])

    # exception when nmap is not installed
    except Exception as e:
        logging.warning("The following error raise when running nmap: " + str(e))
        print("Please install nmap before run this full network scan. (Run 'sudo apt-get install nmap')")


