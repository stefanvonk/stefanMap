# This code is a modified version of a github library

# !/usr/bin/python3
# detectKippoCowrie.py
#
# Proof of concept to detect Kippo and Cowrie SSH honeypots
#
# by Julio Cesar Fort
# Copyright 2016-2018 Blaze Information Security

import sys
import socket
import logging
import isPortOpen

CRED = '\033[91m'
CEND = '\033[0m'

DEFAULT_BANNER = "SSH-2.0-OpenSSH_"
DEFAULT_KIPPOCOWRIE_BANNERS = ["SSH-2.0-OpenSSH_5.1p1 Debian-5", "SSH-1.99-OpenSSH_4.3", "SSH-1.99-OpenSSH_4.7",
                               "SSH-1.99-Sun_SSH_1.1", "SSH-2.0-OpenSSH_4.2p1 Debian-7ubuntu3.1",
                               "SSH-2.0-OpenSSH_4.3", "SSH-2.0-OpenSSH_4.6", "SSH-2.0-OpenSSH_5.1p1 Debian-5",
                               "SSH-2.0-OpenSSH_5.1p1 FreeBSD-20080901", "SSH-2.0-OpenSSH_5.3p1 Debian-3ubuntu5",
                               "SSH-2.0-OpenSSH_5.3p1 Debian-3ubuntu6", "SSH-2.0-OpenSSH_5.3p1 Debian-3ubuntu7",
                               "SSH-2.0-OpenSSH_5.5p1 Debian-6", "SSH-2.0-OpenSSH_5.5p1 Debian-6+squeeze1",
                               "SSH-2.0-OpenSSH_5.5p1 Debian-6+squeeze2",
                               "SSH-2.0-OpenSSH_5.8p2_hpn13v11 FreeBSD-20110503",
                               "SSH-2.0-OpenSSH_5.9p1 Debian-5ubuntu1", "SSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u2",
                               "SSH-2.0-OpenSSH_5.9", "SSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u2"]

DEFAULT_PORT = 22
VERBOSE = True
ERROR = -1


def get_ssh_banner(banner_from_server):
    """
    This function receives the banner of the SSH server. It returns true if
    the server advertises itself as OpenSSH.
    """
    banner = banner_from_server.decode('utf-8').strip()

    if banner in DEFAULT_KIPPOCOWRIE_BANNERS:
        logging.info("[!] Heads up: the banner of this server is on Kippo/Cowrie's default list. May be promising...")

    return DEFAULT_BANNER in banner


def connect_to_ssh(host, port):
    try:
        socket.setdefaulttimeout(5)
        sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockfd.connect((host, port))

        banner = sockfd.recv(1024)

        if get_ssh_banner(banner):
            if VERBOSE:
                logging.info("[+] %s:%d advertised itself as OpenSSH. Continuing..." % (host, port))
            else:
                logging.info("[!] %s:%d does not advertise itself as OpenSSH. Quitting..." % (host, port))
                return False

    except Exception as err:
        logging.info("[!] Error connecting to %s port %d: %s" % (host, port, str(err)))
        return False

    return sockfd


def probe_bad_version(sockfd):
    try:
        sockfd.sendall('SSH-1337\n'.encode('utf-8'))
    except Exception as err:
        logging.info("[!] Error sending probe #1: %s" % str(err))

    response = sockfd.recv(1024)
    sockfd.close()

    if VERBOSE:
        # logging.info(str(response))
        return

    if b"bad version" in response:
        if VERBOSE:
            logging.info("[*] Got 'bad version' in response to probe #1. Might be a honeypot!")
        return True
    else:
        return False


# this probe works against Cowrie, but also some misconfigured versions of OpenSSH 5.3
def probe_spacer_packet_corrupt(sockfd):
    try:
        sockfd.sendall("SSH-2.0-OpenSSH\n\n\n\n\n\n\n\n\n\n".encode('utf-8'))
    except Exception as err:
        logging.info("[!] Error sending probe #2: %s" % str(err))

    response = sockfd.recv(1024)
    sockfd.close()

    if b"corrupt" in response or b"mismatch" in response:
        if VERBOSE:
            logging.info("[*] Got 'packet corrupt' or 'protocol mismatch' in response of probe #2. "
                         "Might be a honeypot!")
            return True
        else:
            return False


def probe_double_banner(sockfd):
    try:
        sockfd.sendall("SSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u2\nSSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u2\n".encode('utf-8'))
    except Exception as err:
        logging.info("[!] Error sending probe #3: %s" % str(err))

    response = sockfd.recv(1024)
    sockfd.close()

    if b"corrupt" in response or b"mismatch" in response:
        if VERBOSE:
            logging.info("[*] Got 'packet corrupt' or 'protocol mismatch' in response of probe #3. "
                         "Might be a honeypot!")
        return True
    else:
        return False


def detect_kippo_cowrie(host, port):
    score = 0

    logging.info("[+] Detecting Kippo/Cowrie technique #1 - bad version")
    sockfd = connect_to_ssh(host, port)

    if sockfd:
        if probe_bad_version(sockfd):
            score += 1
    else:
        logging.info("Socket error in probe #1")
        sys.exit(ERROR)

    logging.info("[+] Detecting Kippo/Cowrie technique #2 - spacer")
    sockfd = connect_to_ssh(host, port)

    if sockfd:
        if probe_spacer_packet_corrupt(sockfd):
            score += 1
    else:
        logging.info("Socket error in probe #2")
        sys.exit(ERROR)

    logging.info("[+] Detecting Kippo/Cowrie technique #3 - double banner")
    sockfd = connect_to_ssh(host, port)

    if sockfd:
        if probe_double_banner(sockfd):
            score += 1
    else:
        logging.info("Socket error in probe #3")
        sys.exit(ERROR)

    return score


def check_kippo_cowrie(ip, port):
    if isPortOpen.is_open(ip, port):
        return detect_kippo_cowrie(ip, port)
    else:
        return 0
