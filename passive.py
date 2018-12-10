import ipaddress
import subprocess
import getmac
import requests
import logging

def enterSniffDuration():
    # get duration of network sniffing from user
    try:
        duration = int(input("Enter the time of the duration of networksniffing in seconds (between 1 and 3600):"))
        if duration > 0 and duration < 3600:
            return duration
        else:
            print("Your input cannot be processed. Please enter an integer between 1 and 3600.")
            return enterSniffDuration()
    except:
        print("Your input cannot be processed. Please enter an integer between 1 and 3600.")
        return enterSniffDuration()


def sniffNetwork(duration):
    # sniff network traffic to file
    logging.info("Start sniff network traffic")

    try:
        # run tshark network sniff
        subprocess.run(["sudo", "touch", "networksniff.pcap"])
        subprocess.run(["sudo", "tshark", "-a duration:" + duration, "-w networksniff.pcap"])
        logging.info("The network traffic of the last " + duration + " seconds is saved to the file networksniff.pcap")
    except Exception as e:
        logging.warning("The following error raise when running tshark: " + str(e))
        print("Error: please install tshark before run this full network scan. "
              "(Run 'sudo apt-get install tshark')\n")

    logging.info("End sniff network traffic")


def detectionMethod1(ip):
    # analyze network sniff file
    logging.info("Start analyze network traffic")

    try:
        # run tshark network sniff
        subprocess.run(["sudo", "tshark", "-r networksniff.pcap", "-Y 'ip.src == " + ip + "/24'", "-z ip_hosts,tree"])
        logging.info("File networksniff.pcap analyzing is done")
    except Exception as e:
        logging.warning("The following error raise when running tshark: " + str(e))
        print("Error: please install tshark before run this full network scan. "
              "(Run 'sudo apt-get install tshark')\n")

    logging.info("End analyze network traffic")


def detectionMethod2(ip):
    # detect virtual machine vendor
    logging.info("Start check MAC address vendor")

    # set api url
    url = "https://api.macvendors.com/"
    vendor = "Could not get the MAC vendor"

    try:
        # get mac address from ip, via passive arp scanning (no network request)
        mac = getmac.get_mac_address(ip=ip, network_request=False)
        try:
            # Make a get request to get response from the macvendors api
            response = requests.get(url + mac)
            # set response to variable
            vendor = response.content.decode("utf-8")
        except Exception as e:
            logging.warning("The following error raise when trying to get response from macvendors.com:" + str(e))
    except Exception as e:
        logging.warning("The following error raise when trying to get the MAC address from the network machine:" + str(e))

    print("#2: The vendor of the MAC address of this machine is: " + str(vendor))
    print("Check manually whether this is virtual machine vendor.")
    logging.info("Result of MAC address vendor: " + str(vendor))

    logging.info("End check MAC address vendor")


def passive(ip):
    # get duration of network sniffing
    duration = enterSniffDuration()
    # sniff entire network for duration
    sniffNetwork(duration)

    print("\nThe results of the passive honeypot scan on " + ip + ":")
    # run all detection methods
    detectionMethod1(ip) # analyze network sniff file
    detectionMethod2(ip) # virtual machine/MAC vendor

    print("\n\nFor details about the process of scanning, check the logfile 'stefanMap.log'.\n")
