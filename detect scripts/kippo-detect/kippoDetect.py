import socket, sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format

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

def main():
	cprint(figlet_format('Kippo Detect', font='big'), attrs=['bold'])
	try:
		ip = input ('Enter Host IP: ')
		status = checkKippo(ip)
		if (status == 0):
			print ('[+] Kippo Detected Running on:\t' + ip)
		else:
			print ('[-] Kippo Not Detected Running on:\t' + ip)
	except KeyboardInterrupt:
		print ('\n[*] Exiting...')

main()