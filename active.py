import os
import subprocess
import sys

import kippoDetect
import detectKippoCowrie
import isPortOpen
import logging
import socket
import urllib.request
import paramiko
import detectMACvendor


def detectionMethod1(ip):
    # kippoDetect, score 0 - 1
    logging.info("Start kippoDetect")

    # declare variables
    kippodetect = 0
    kippodetect22 = 0
    kippodetect2222 = 0

    # try to detect kippo honeypot op port 22
    try:
        kippodetect22 = kippoDetect.checkKippo(ip, 22)
    except Exception as e:
        logging.warning("The following error raise when running kippoDetect: " + str(e))

    # try to detect kippo honeypot op port 2222
    try:
        kippodetect2222 = kippoDetect.checkKippo(ip, 2222)
    except Exception as e:
        logging.warning("The following error raise when running kippoDetect: " + str(e))

    # check results
    if kippodetect2222 > 0:
        kippodetect = 1
    if kippodetect22 > 0:
        kippodetect = 1

    print("\n#1: The possibility that this ip runs a kippo honeypot:\n" + str(kippodetect) + "/1")
    logging.info("Result kippoDetect: " + str(kippodetect) + "/1")

    logging.info("End kippoDetect")


def detectionMethod2(ip):
    # detectKippoCowrie, score 0 - 3
    logging.info("Start detectKippoCowrie")

    # declare variables
    detectkippocowrie = 0
    detectkippocowrie22 = 0
    detectkippocowrie2222 = 0

    # try to detect kippo or cowrie on port 22
    try:
        detectkippocowrie22 = detectKippoCowrie.checkKippoCowrie(ip, 22)
    except Exception as e:
        logging.warning("The following error raise when running detectKippoCowrie: " + str(e))

    # try to detect kippo or cowrie on port 2222
    try:
        detectkippocowrie2222 = detectKippoCowrie.checkKippoCowrie(ip, 2222)
    except Exception as e:
        logging.warning("The following error raise when running detectKippoCowrie: " + str(e))

    # check results
    if detectkippocowrie2222 > 0:
        detectkippocowrie = detectkippocowrie2222
    if detectkippocowrie22 > 0:
        detectkippocowrie = detectkippocowrie22

    print("\n#2: The possibility that this ip runs a kippo or cowrie honeypot:\n" + str(detectkippocowrie) + "/3")
    logging.info("Result detectKippoCowrie: " + str(detectkippocowrie) + "/3")

    logging.info("End detectKippoCowrie")


def detectionMethod3(ip):
    # T-Pot dashboard - ip:64297, score 0 - 1
    logging.info("Start check T-Pot daschboard")

    # check if port 64297 is open
    if isPortOpen.isOpen(ip, 64297):
        logging.info("There is probably an T-pot dashboard on this port")
        tpotdashboard = 1
    else:
        logging.info("There is probably no T-pot dashboard on this port")
        tpotdashboard = 0
    print("\n#3: The possibility that this ip runs a T-pot honeynetwork with a dashboard:"
          "\n" + str(tpotdashboard) + "/1")
    logging.info("Result T-pot dashboard: " + str(tpotdashboard) + "/1")

    logging.info("End check T-Pot daschboard")


def detectionMethod4(ip):
    # mhn dashboard - ip:80, score 0 - 1
    logging.info("Start check mhn daschboard")

    # check if port 80 is open
    if isPortOpen.isOpen(ip, 80):
        # read content of webpage
        contentWebPage = str(urllib.request.urlopen("http://" + ip).read())
        # check if strings are in the content of the webpage
        if "Modern Honeypot Network" in contentWebPage and "Modern Honeynet Framework" in contentWebPage \
                and "threatstream.com" in contentWebPage:
            logging.info("This webpage is a dashboard from a mhn honeypot")
            mhndashboard = 1
        else:
            logging.info("This webpage is not a dashboard from a mhn honeypot")
            mhndashboard = 0
    else:
        logging.info("There is probably no mhn dashboard on this port")
        mhndashboard = 0

    print("\n#4: The possibility that this ip runs a mhn honeynetwork with a dashboard:\n" + str(mhndashboard) + "/1")
    logging.info("Result mhn dashboard: " + str(mhndashboard) + "/1")

    logging.info("End check mhn daschboard")


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


def detectionMethod5(ip):
    # check open ports, score 0 - 1
    logging.info("Start portScan")

    # if there are more than 10 ports open, it gives a true positive
    openports = portScan(ip)
    if openports > 10:
        print("\n#5: The possibility that this ip runs a honeypot is on subject of more then 10 open ports:\n1/1")
        logging.info("Result portScan: 1/1")
        logging.info(
            "There are: " + str(openports) + " open ports and " + str(1023 - openports) +
            " closed ports on ip " + str(ip))
    else:
        print("\n#5: The possibility that this ip runs a honeypot is on subject of more then 10 open ports:\n0/1")
        logging.info("Result portScan: 0/1")
        logging.info(
            "There are: " + str(openports) + " open ports and " + str(1023 - openports) +
            " closed ports on ip " + str(ip))

    logging.info("End checkOpenPorst")


def checkSshesame():
    if os.path.exists('stefanMap.log'):
        fileHandle = open('stefanMap.log', "r")
        lineList = fileHandle.readlines()
        fileHandle.close()
        if "sshesame" in str(lineList[len(lineList)-1]) or "sshesame" in str(lineList[len(lineList)-2]) \
                or "sshesame" in str(lineList[len(lineList)-3]) or "sshesame" in str(lineList[len(lineList)-4])\
                or "sshesame" in str(lineList[len(lineList)-5]):
            return True
        else:
            return False
    else:
        return False


def detectionMethod6(ip):
    # check if ssh is running correctly
    logging.info("Start check ssh server")

    sshesame = False

    if isPortOpen.isOpen(ip, 22):
        # set up ssh
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        logging.info("Try to connect ssh server on " + str(ip))
        # try to connect to ip:22
        try:
            client.connect(ip, 22, 'root', '123456')
            # check hostname of ssh-server
            sshesame = checkSshesame()
            logging.info("Authentication root, 123456: accepted")
            # try to execute command
            try:
                stdin, stdout, stderr = client.exec_command('ifconfig').decode("utf-8")
                # if there is no output, commands cannot be execute on the ssh-server
                if stdout == "" and stdin == "" and stderr == "":
                    logging.info('Commands execution not supported by this ssh server')
                    sshserver = 1
                else:
                    logging.info('Commands execution is supported by this ssh server')
                    sshserver = 0
            # if command execution failed
            except:
                logging.info('Commands execution not supported by this ssh server')
                sshserver = 1
        # authentication error
        except paramiko.ssh_exception.AuthenticationException:
            sshesame = checkSshesame()
            logging.info("Authentication root, 123456: failure")
            sshserver = 0
        # BadHostKeyException
        except paramiko.ssh_exception.BadHostKeyException:
            sshesame = checkSshesame()
            logging.info("This server is probably a ssh honeypot witch does a man-in-the-middle attack")
            sshserver = 1
        # other exceptions
        except Exception as e:
            sshesame = checkSshesame()
            logging.warning("The following error raise when trying connect to ssh server:" + str(e))
            sshserver = 0
    else:
        logging.info("This is not a running ssh server")
        sshserver = 0

    print("\n#6: The possibility that this ip runs a honeypot ssh server:"
          "\n" + str(sshserver) + "/1")
    logging.info("Result check ssh server: " + str(sshserver) + "/1")

    # check if the hostname of the machine is sshesame
    if sshesame:
        print("\n#6.1: The hostname of the ssh server is sshesame (a known honeypot):\n1/1")
        logging.info("Result of hostname ssh server is sshesame (a known honeypot): 1/1")
    else:
        print("\n#6.1: The hostname of the ssh server is sshesame (a known honeypot):\n0/1")
        logging.info("Result of hostname ssh server is sshesame (a known honeypot): 0/1")

    logging.info("End check ssh server")


def detectionMethod7(ip):
    # dionaeaDetect, score 0 - 1
    logging.info("Start dionaeaDetect")

    # set variables
    content = ""
    dionaeadetect = 0

    # check if port 443 is open
    if isPortOpen.isOpen(ip, 443):
        # try to connect to the ssl port of the machine and read the output
        try:
            logging.info("Try connection to the ssl port of the machine")

            # execute command to get ssl certificate info
            command = subprocess.Popen(["openssl", "s_client", "-connect", ip + ":443"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = command.stdout.read()
            content = output.decode("utf-8")

            logging.info("Ssl connection established")
        except Exception as e:
            logging.warning("The following error raise when trying connect to ssl port:" + str(e))

        # if the string dionaea is in the content of the output dionaeadetect = 1
        if "dionaea" in str(content):
            dionaeadetect = 1

    print("\n#7: The possibility that this ip runs a dionaea honeypot:\n" + str(dionaeadetect) + "/1")
    logging.info("Result dionaeaDetect: " + str(dionaeadetect) + "/1")

    logging.info("End dionaeaDetect")


def detectionMethod8(ip):
    # detect virtual machine vendor
    logging.info("Start check MAC address vendor")

    vendor = detectMACvendor.macVendor(ip)

    print("\n#8: The vendor of the MAC address of the machine is: " + vendor)
    print("Check manually whether this is virtual machine vendor.")
    logging.info("Result of MAC address vendor: " + vendor)

    logging.info("End check MAC address vendor")


def active(ip):
    print("\nThe results of the active honeypot scan on " + ip + ":")
    # run all detection methods
    detectionMethod1(ip) # kippoDetect
    detectionMethod2(ip) # detectKippoCowrie
    detectionMethod3(ip) # T-pot dashboard
    detectionMethod4(ip) # mhn dashboard
    detectionMethod5(ip) # port scan
    detectionMethod6(ip) # check ssh server
    detectionMethod7(ip) # detect dionaea
    detectionMethod8(ip) # virtual machine/MAC vendor

    print("\n\nFor details about the process of scanning, check the logfile 'stefanMap.log'.\n")