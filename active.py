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
    kippodetect = kippoDetect.checkKippo(ip)
    logging.info("Finishing kippoDetect")

    # test 2 detectKippoCowrie, score 0 - 3
    logging.info("Starting detectKippoCowrie")
    detectkippocowrie = detectKippoCowrie.checkKippoCowrie(ip)
    logging.info("Finishing detectKippoCowrie")

    # test 3 T-Pot dashboard - ip:64297, score 0 - 1
    logging.info("Starting check T-Pot daschboard")
    if isPortOpen.isOpen(ip, 64297):
        tpotdashboard = 1
        logging.info("Port 64297 on " + str(ip) + " is open. This is possible the dashboard of a T-Pot honeynetwork.")
    else:
        tpotdashboard = 0
        logging.info("Port 64297 on " + str(ip) + " is closed. It is not the dashboard of a T-Pot honeynetwork.")
    logging.info("Finishing check T-Pot daschboard")


    ############### mhn dashboard

    # test 4 checkOpenPorts, score 0 - 1
    logging.info("Starting checkOpenPorst")
    nm = nmap.PortScanner()
    nm.scan(hosts=ip + '/24', arguments='-n -sP -PE -PA21,23,80,3389')
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    for host, status in hosts_list:
        print('{0}:{1}'.format(host, status))
    logging.info("Finishing checkOpenPorst")
    ######## not ready

    result = str(status) + " / 5"

    return result


    ######## detect virtual machine
