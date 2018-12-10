import getmac
import requests
import pyshark
import logging


def detectionMethod1(ip):
    # scan network traffic
    logging.info("Start scan network traffic")

    capture = pyshark.LiveCapture(interface='eth0')
    capture.sniff(timeout=20)
    for packet in capture.sniff_continuously(packet_count=5):
        print('Just arrived:', packet)

    logging.info("End scan network traffic")


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
    print("\nThe results of the passive honeypot scan on " + ip + ":")
    # run all detection methods
    detectionMethod1(ip)#TODO
    detectionMethod2(ip)

    print("\n\nFor details about the process of scanning, check the logfile 'stefanMap.log'.\n")
