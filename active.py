import ipaddress
import kippoDetect
import detectKippoCowrie
import isPortOpen
import logging
import socket
import urllib.request


def portScan(ip):
    result = 0

    def scan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            # send data via socket to the port on ip
            s.connect((ip, int(port)))
            s.shutdown(2)
            return 1
        except Exception as e:
            return 0

    r = 1
    for x in range(1, 1024):
        result += scan(r)
        r += 1
    return result


def detectionMethod1(ip):
    # kippoDetect, score 0 - 1
    logging.info("Start kippoDetect")

    try:
        kippodetect = kippoDetect.checkKippo(ip)
    except Exception as e:
        logging.warning("The following error raise when running kippoDetect: " + str(e))
        kippodetect = 0

    print("\n#1: The possibility that this ip runs a kippo honeypot:\n" + str(kippodetect) + "/1")
    logging.info("Result kippoDetect: " + str(kippodetect) + "/1")

    logging.info("End kippoDetect")


def detectionMethod2(ip):
    # detectKippoCowrie, score 0 - 3
    logging.info("Start detectKippoCowrie")

    try:
        detectkippocowrie = detectKippoCowrie.checkKippoCowrie(ip)
    except Exception as e:
        logging.warning("The following error raise when running detectKippoCowrie: " + str(e))
        detectkippocowrie = 0

    print("\n#2: The possibility that this ip runs a kippo or cowrie honeypot:\n" + str(detectkippocowrie) + "/3")
    logging.info("Result detectKippoCowrie: " + str(detectkippocowrie) + "/3")

    logging.info("End detectKippoCowrie")


def detectionMethod3(ip):
    # T-Pot dashboard - ip:64297, score 0 - 1
    logging.info("Start check T-Pot daschboard")

    if isPortOpen.isOpen(ip, 64297):
        logging.info("Port 64297 on " + str(ip) + " is open")
        tpotdashboard = 1
    else:
        logging.info("Port 64297 on " + str(ip) + " is closed")
        tpotdashboard = 0
    print(
        "\n#3: The possibility that this ip runs a T-pot honeynetwork with a dashboard:\n" + str(tpotdashboard) + "/1")
    logging.info("Result T-pot dashboard: " + str(tpotdashboard) + "/1")

    logging.info("End check T-Pot daschboard")


def detectionMethod4(ip):
    # mhn dashboard - ip:80, score 0 - 1
    logging.info("Start check mhn daschboard")

    if isPortOpen.isOpen(ip, 80):
        logging.info("Port 80 on " + str(ip) + " is open")
        contentWebPage = str(urllib.request.urlopen(ip).read())
        if "Modern Honeypot Network" in contentWebPage and "Modern Honeynet Framework" in contentWebPage \
                and "threatstream.com" in contentWebPage:
            logging.info("This webpage is a dashboard from a mhn honeypot")
            mhndashboard = 1
        else:
            logging.info("This webpage is not a dashboard from a mhn honeypot")
            mhndashboard = 0
    else:
        logging.info("Port 80 on " + str(ip) + " is closed, there is definitely no mhn dashboard on this port")
        mhndashboard = 0
    print("\n#4: The possibility that this ip runs a mhn honeynetwork with a dashboard:\n" + str(mhndashboard) + "/1")
    logging.info("Result mhn dashboard: " + str(mhndashboard) + "/1")

    logging.info("End check mhn daschboard")


def detectionMethod5(ip):
    # check open ports, score 0 - 1
    logging.info("Start portScan")

    # if there are more than 10 ports open, it gives a true positive
    openports = portScan(ip)
    if openports > 10:
        print("\n#5: The possibility that this ip runs a honeypot is on subject of open ports:\n1/1")
        logging.info("Result portScan: 1/1")
        logging.info(
            "There are: " + str(openports) + " open ports and " + str(1023 - openports) +
            " closed ports on ip " + str(ip))
    else:
        print("\n#5: The possibility that this ip runs a honeypot is on subject of open ports:\n0/1")
        logging.info("Result portScan: 0/1")
        logging.info(
            "There are: " + str(openports) + " open ports and " + str(1023 - openports) +
            " closed ports on ip " + str(ip))

    logging.info("End checkOpenPorst")


def detectionMethod6(ip):
    # detect virtual machine
    return


def active():
    # ask user to enter ip address for scanning
    ip = input("Enter a valid host IP address for scanning: ")
    logging.info("Entered host IP is: " + str(ip))

    try:
        # check ip address
        ipaddress.ip_address(ip)

        # run all detection methods
        detectionMethod1(ip)
        detectionMethod2(ip)
        detectionMethod3(ip)
        detectionMethod4(ip)
        detectionMethod5(ip)
        detectionMethod6(ip)#TODO

    # exception when the entered ip is not a IPv4 or IPv6 address
    except Exception as e:
        logging.warning("The following error raise when checking the IP address: " + str(e))
        print("Your input does not appear to be an IPv4 or IPv6 address, please try again.")
        active()
