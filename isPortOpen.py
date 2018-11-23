import socket
import logging

def isOpen(ip, port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except Exception as e:
      logging.warning("Exception when testing if port " + port + " on " + ip + " is open:" + str(e))
      print("Port " + port + " is closed, there is probably not a (working) honeypot on this port.")
      return False