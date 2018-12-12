# with this script you can test whether the machine where you are on is a honeypot or not.
# This script is standalone with no dependencies.

import os
import struct
import subprocess


def detectionMethod1():
    print("\n#1: Check if there are standard honeypot accounts on the machine.")

    # write the content of the /etc/passwd file to a variable
    if os.path.isdir('/etc/passwd') or os.path.exists('/etc/passwd'):
        file = open('/etc/passwd', 'r')
        content = file.read()
        file.close()
        # check if the variable contains a standard honeypot configuration
        if "kippo" in content:
            print("Kippo useraccount detected")
        elif "cowrie" in content:
            print("Cowrie useraccount detected")
        elif "tsec" in content or "tpot" in content:
            print("t-pot useraccount detected")
        # the other honeypots don't have a standard user account
        else:
            print("No standard honeypot account configuration found.")
    else:
        print("No such file or directory: '/etc/passwd'. This machine is probably not a honeypot because it isn't"
              " running a linux system.")


def noHoneypot(number, name):
    if number > 10:
        print("A machine configuration with standard", name, "honeypot files and folders found.")
        return False
    else:
        return True


def detectionMethod2():
    print("\n#2: Check if there are standard honeypot files or folders on the machine.")

    # declare variables
    cowrie = 0
    kippo = 0
    sshesame = 0
    mhn = 0
    dionaea = 0
    tpot = 0

    try:
        # set root directory to check from
        rootDir = '/'
        # walk through each subdirectory
        for dirName, subdirList, fileList in os.walk(rootDir):
            folderName = '%s' % dirName
            # check if the honeypot strings are in the folder names
            if "cowrie" in folderName:
                cowrie += 1
            if "kippo" in folderName:
                kippo += 1
            if "sshesame" in folderName:
                sshesame += 1
            if "mhn" in folderName:
                mhn += 1
            if "dionaea" in folderName:
                dionaea += 1
            if "tpot" in folderName:
                tpot += 1

            # loop through each filename
            for fname in fileList:
                fileName = fname
                # check if the honeypot strings are in the filenames
                if "cowrie" in fileName:
                    cowrie += 1
                if "kippo" in fileName:
                    kippo += 1
                if "sshesame" in fileName:
                    sshesame += 1
                if "mhn" in fileName:
                    mhn += 1
                if "dionaea" in fileName:
                    dionaea += 1
                if "tpot" in fileName:
                    tpot += 1
    except Exception as e:
        print("The following error raise when trying to map the filesystem: " + str(e))

    # if one of the variables > 10, a standard honeypot configuration is found
    if (noHoneypot(mhn, "mhn") & noHoneypot(tpot, "t-pot") & noHoneypot(cowrie, "cowrie") &
            noHoneypot(kippo, "kippo") & noHoneypot(sshesame, "sshesame") & noHoneypot(dionaea, "dionaea")):
        print("No standard honeypot filesystem configuration found.")


def noHoneypotService(output, strings, name):
    match = 0
    for string in strings:
        if string in output:
            match += 1
    if match == len(strings):
        print("A running", name, "honeypot service found.")
        return False
    else:
        return True


def detectionMethod3():
    print("\n#3: check if there are standard honeypot services on the machine.")

    # run service command
    command = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
    output = command.stdout.read()
    content = output.decode("utf-8")

    # set search variables
    mhn = ["/mhn/env/bin/python", "/mhn/env/bin/celery", "/mhn/env/bin/uwsgi", "mhn.tasks", "--loglevel=", "mhn:mhn"]
    tpot = ["/opt/tpot", "/etc/tpot.yml", "suricata", "honeytrap", "p0f", "cowrie", "rdpy", "vnclowpot", "dionaea"]
    cowrie = ["home/cowrie", "cowrie.python.logfile.logger", "cowrie-env/bin/python", "cowrie.pid", "cowrie-env/bin/twistd"]
    kippo = ["home/kippo/", ".local/bin/twistd", "kippo.tac", "kippo.log", "kippo.pid"]
    sshesame = ["./sshesame"]
    dionaea = ["/opt/dionaea", "/bin/dionaea"]

    # if strings are in output, a honeypot service is found
    if (noHoneypotService(content, mhn, "mhn") & noHoneypotService(content, tpot, "t-pot") &
            noHoneypotService(content, cowrie, "cowrie") & noHoneypotService(content, kippo, "kippo") &
            noHoneypotService(content, sshesame, "sshesame") & noHoneypotService(content, dionaea, "dionaea")):
        print("No standard running honeypot service found.")

    # print blank line
    print("")


def local():
    print("\nThe following actions are done by the script:")

    detectionMethod1() # detection of standard honeypot account configuration
    detectionMethod2() # detection of standard honeypot files and folders
    detectionMethod3() # check services of machine


local()
