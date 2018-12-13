# This code is a modified version of a github library
import socket
import isPortOpen
import logging

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
spacer = b'\n\n\n\n\n\n\n\n'


# detection is achived by issuing unexpected data to the running ssh service and checking
# 'Protocol Mismatch' error or a 'bad packet length' error, both are non standard error messages.

def checkKippo(ip, port):
    # check if port 22 is open on ip-address
    if isPortOpen.isOpen(ip, port):
        # send data via socket to port 22 on ip-address
        s.connect((ip, port))
        banner = s.recv(1024)
        s.send(banner + spacer)
        response = s.recv(1024)
        # test if the machine on ip-address is a kippo honeypot
        if (b'Protocol mismatch' in response or b'bad packet length' in response):
            logging.info(
                "Got 'Protocol mismatch' or 'bad packet length' in response of probe. This might be a kippo honeypot!")
            return 1
        else:
            logging.info(
                "Got no 'Protocol mismatch' or 'bad packet length' in response of probe. This might not be a kippo honeypot.")
            return 0
    else:
        return 0
