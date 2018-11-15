# This code is a modified version of a github library

import socket, sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format

import isPortOpen

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

spacer = b'\n\n\n\n\n\n\n\n'

#Detection is achived by issuing unexpected data to the running ssh service and checking
#'Protocol Mismatch' error or a 'bad packet length' error, both are non standard error messages.

def main(ip):
    if isPortOpen.isOpen(ip, 22):
        s.connect((ip, 22))
        banner = s.recv(1024)
        s.send(banner + spacer)
        response = s.recv(1024)
        if (b'Protocol mismatch' in response or b'bad packet length' in response):
            return 1
        else:
            return 0
    else:
        print("Port 22 is closed, this is probably not a (working) SSH honeypot.")
        return 0