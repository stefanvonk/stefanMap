# with this script you can test whether the machine where you are on is a honeypot or not.
# This script is standalone with no dependencies.

import os
import subprocess


def detectionmethod1():
    print("\n#1: Check if there are standard honeypot accounts on the machine:")

    # write the content of the /etc/passwd file to a variable
    if os.path.isdir('/etc/passwd') or os.path.exists('/etc/passwd'):
        file = open('/etc/passwd', 'r')
        content = file.read()
        file.close()
        # check if the variable contains a standard honeypot configuration
        if "kippo" in content:
            print("A kippo user account found.")
        elif "cowrie" in content:
            print("A cowrie user account found.")
        elif "tsec" in content or "tpot" in content:
            print("A t-pot user account found.")
        # the other honeypots don't have a standard user account
        else:
            print("No standard honeypot account configuration found.")
    else:
        print("No such file or directory: '/etc/passwd'. This machine is probably not a honeypot because it isn't"
              " running a linux system.")


def no_honeypot(number, name):
    if number > 10:
        print("A filesystem configuration with standard", name, "honeypot files and folders found.")
        return False
    else:
        return True


def detectionmethod2():
    print("\n#2: Check if there are standard honeypot files or folders on the machine:")

    # declare variables
    cowrie = 0
    kippo = 0
    sshesame = 0
    mhn = 0
    dionaea = 0
    tpot = 0

    try:
        # set root directory to check from
        root_dir = '/'
        # walk through each subdirectory
        for dirName, subdirList, fileList in os.walk(root_dir):
            folder_name = '%s' % dirName
            # check if the honeypot strings are in the folder names
            if "cowrie" in folder_name:
                cowrie += 1
            if "kippo" in folder_name:
                kippo += 1
            if "sshesame" in folder_name:
                sshesame += 1
            if "mhn" in folder_name:
                mhn += 1
            if "dionaea" in folder_name:
                dionaea += 1
            if "tpot" in folder_name:
                tpot += 1

            # loop through each filename
            for fname in fileList:
                file_name = fname
                # check if the honeypot strings are in the filenames
                if "cowrie" in file_name:
                    cowrie += 1
                if "kippo" in file_name:
                    kippo += 1
                if "sshesame" in file_name:
                    sshesame += 1
                if "mhn" in file_name:
                    mhn += 1
                if "dionaea" in file_name:
                    dionaea += 1
                if "tpot" in file_name:
                    tpot += 1
    except Exception as e:
        print("The following error raise when trying to map the filesystem:", str(e), ".")

    # if one of the variables > 10, a standard honeypot configuration is found
    if (no_honeypot(mhn, "mhn") & no_honeypot(tpot, "t-pot") & no_honeypot(cowrie, "cowrie") &
            no_honeypot(kippo, "kippo") & no_honeypot(sshesame, "sshesame") & no_honeypot(dionaea, "dionaea")):
        print("No standard honeypot filesystem configuration found.")


def no_honeypot_service(output, strings, name):
    match = 0
    for string in strings:
        if string in output:
            match += 1
    if match == len(strings):
        print("A running", name, "honeypot service found.")
        return False
    else:
        return True


def detectionmethod3():
    print("\n#3: Check if there are standard honeypot services on the machine:")

    # run service command
    command = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
    output = command.stdout.read()
    content = output.decode("utf-8")

    # set search variables
    mhn = ["/mhn/env/bin/python", "/mhn/env/bin/celery", "/mhn/env/bin/uwsgi", "mhn.tasks", "--loglevel=", "mhn:mhn"]
    tpot = ["/opt/tpot", "/etc/tpot.yml", "suricata", "honeytrap", "p0f", "cowrie", "rdpy", "vnclowpot", "dionaea"]
    cowrie = ["home/cowrie", "cowrie.python.logfile.logger", "cowrie-env/bin/python", "cowrie.pid",
              "cowrie-env/bin/twistd"]
    kippo = ["home/kippo/", ".local/bin/twistd", "kippo.tac", "kippo.log", "kippo.pid"]
    sshesame = ["./sshesame"]
    dionaea = ["/opt/dionaea", "/bin/dionaea"]

    # if strings are in output, a honeypot service is found
    if (no_honeypot_service(content, mhn, "mhn") & no_honeypot_service(content, tpot, "t-pot") &
            no_honeypot_service(content, cowrie, "cowrie") & no_honeypot_service(content, kippo, "kippo") &
            no_honeypot_service(content, sshesame, "sshesame") & no_honeypot_service(content, dionaea, "dionaea")):
        print("No standard running honeypot service found.")

    # print blank line
    print("")


def local():
    print("\nThe following actions are done by the script:")

    detectionmethod1()  # detection of standard honeypot account configuration
    detectionmethod2()  # detection of standard honeypot files and folders
    detectionmethod3()  # check services of machine


local()
