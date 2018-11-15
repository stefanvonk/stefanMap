# This code is from a github library

import socket, sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

spacer = b'\n\n\n\n\n\n\n\n'

#Detection is achived by issuing unexpected data to the running ssh service and checking
#'Protocol Mismatch' error or a 'bad packet length' error, both are non standard error messages.

def checkKippo(ip):
	s.connect((ip, 22))
	banner = s.recv(1024)
	s.send(banner + spacer)
	response = s.recv(1024)
	if (b'Protocol mismatch' in response or b'bad packet length' in response):
		return 0
	else:
		return 1

def kippoDetect(ipaddress):
	try:
		ip = ipaddress
		status = checkKippo(ip)
		if (status == 0):
			return 1
		else:
			return 0
	except KeyboardInterrupt:
		print ('\n[*] Exiting...')