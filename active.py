import kippoDetect
import detectKippoCowrie
import isPortOpen
import logging
import nmap

def active():
    status = 0
    # ask user to enter ip-address for scanning
    ip = input("\nEnter a host IP for scanning: ")
    logging.info("Entered host ip is: " + str(ip) + ".")
    print("\n")

    # test 1 kippoDetect, score 0 - 1
    logging.info("Starting kippoDetect")
    try:
        kippodetect = kippoDetect.checkKippo(ip)
    except Exception as e:
        logging.info("The following error raise when running kippoDetect: " + str(e))
        kippodetect = 0
    logging.info("Finishing kippoDetect")

    # test 2 detectKippoCowrie, score 0 - 3
    logging.info("Starting detectKippoCowrie")
    try:
        detectkippocowrie = detectKippoCowrie.checkKippoCowrie(ip)
    except Exception as e:
        print("The following error raise when running detectKippoCowrie: " + str(e))
        detectkippocowrie = 0
    logging.info("Finishing detectKippoCowrie")

    # test 3 T-Pot dashboard - ip:64297, score 0 - 1
    logging.info("Starting check T-Pot daschboard")
    if isPortOpen.isOpen(ip, 64297):
        logging.info("Port 64297 on " + str(ip) + " is open. This is possible the dashboard of a T-Pot honeynetwork.")
        tpotdashboard = 1
    else:
        logging.info("Port 64297 on " + str(ip) + " is closed. It is not the dashboard of a T-Pot honeynetwork.")
        tpotdashboard = 0
    logging.info("Finishing check T-Pot daschboard")


    ############### mhn dashboard

    # test 4 checkOpenPorts, score 0 - 1
    logging.info("Starting checkOpenPorst")
    nm = nmap.PortScanner()
    try:
        openports = nm.scan(hosts=ip, ports="0-1023")
    except Exception as e:
        logging.info("The following error raise when running portscan: " + str(e))
        openports = "0"

    print("Open ports:\n" + openports)

    logging.info("Finishing checkOpenPorst")

    result = str(status) + " / 5"

    return result


    ######## detect virtual machine
