import socket
import logging


def is_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # send data via socket to the port on ip
        s.connect((ip, int(port)))
        s.shutdown(2)
        logging.info("Port " + str(port) + " on " + str(ip) + " is open")
        return True
    except Exception as e:
        logging.warning("Exception when testing if port " + str(port) + " on " + str(ip) + " is open:" + str(e))
        logging.info("Port " + str(port) + " on " + str(ip) + " is closed")
        return False
