import socket
import logging

def isOpen(ip, port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      # send data via socket to the port on ip
      s.connect((ip, int(port)))
      s.shutdown(2)
      logging.info("Port " + port + " on " + ip + " is open.")
      return True
   except Exception as e:
      logging.warning("Exception when testing if port " + port + " on " + ip + " is open:" + str(e) + ".")
      logging.info("Port " + port + " on " + ip + " is closed.")
      return False