# with this script you can test whether the machine where you are on is a honeypot or not.
# This script is standalone with no dependencies.

import os
import struct
import subprocess


# source: https://gist.github.com/mojaves/3480749
def cpuHypervisorID():
    # we cannot (yet) use _cpuid because of the different unpack format.
    HYPERVISOR_CPUID_LEAF = 0x40000000
    with open('/dev/cpu/0/cpuid', 'rb') as f:
        f.seek(HYPERVISOR_CPUID_LEAF)
        c = struct.unpack('I12s', f.read(16))
        return c[1].strip('\x00')


# source: https://gist.github.com/mojaves/3480749
def cpuModelName():
    with open('/proc/cpuinfo', 'rt') as f:
        for line in f:
            if ':' in line:
                k, v = line.split(':', 1)
                k = k.strip()
                if k == 'model name':
                    return v.strip()
    return ''


def noHoneypot(number, name):
    if number > 10:
        print("A machine configuration with standard", name, "honeypot files and folders found.")
        return False
    else:
        return True


def detectionMethod1():
    print("\n#1: Check if there are standard honeypot accounts on the machine.")

    # write the content of the /etc/passwd file to a variable
    if os.path.isdir('/etc/passwd') or os.path.exists('/etc/passwd'):
        file = open('/etc/passwd', 'r')
        content = file.read()
        file.close()
        # check if the variable contains a standard honeypot configuration
        if "kippo" in content or "Kippo" in content:
            print("Kippo useraccount detected")
        elif "cowrie" in content or "Cowrie" in content:
            print("Cowrie useraccount detected")
        elif "tsec" in content or "Tsec" in content or "tpot" in content or "Tpot" in content:
            print("T-potce useraccount detected")
        elif "t-sec" in content or "T-sec" in content or "t-pot" in content or "T-pot" in content:
            print("T-potce useraccount detected")
        # the other honeypots don't have a standard user account
        else:
            print("No standard honeypot account configuration found.")
    else:
        print("No such file or directory: '/etc/passwd'. This machine is probably not a honeypot because it isn't"
              " running a linux system.")


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
            if "t-pot" in folderName or "tpot" in folderName or "t-sec" in folderName or "tsec" in folderName:
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
                if "t-pot" in fileName or "tpot" in fileName or "t-sec" in fileName or "tsec" in fileName:
                    tpot += 1
    except Exception as e:
        print("The following error raise when trying to map the filesystem: " + str(e))

    # if one of the variables > 10, a standard honeypot configuration is found
    if (noHoneypot(mhn, "mhn") & noHoneypot(tpot, "t-pot") & noHoneypot(cowrie, "cowrie") &
            noHoneypot(kippo, "kippo") & noHoneypot(sshesame, "sshesame") & noHoneypot(dionaea, "dionaea")):
        print("No standard honeypot machine configuration found.")


def detectionMethod3():
    print("\n#3: Check the networktraffic of the machine.")



def detectionMethod4():
    print("\n#4: check the services of the machine.")

    # run service command
    command = subprocess.Popen(["service", "--status-all"], stdout=subprocess.PIPE)
    output = command.stdout.read()

    # set variables
    i = 0
    running = 0
    notrunning = 0

    # check running or not running for each line in the output of the service command
    for line in output.decode("utf-8").splitlines():
        i += 1
        if " [ + ]  " in line:
            running += 1
        elif " [ - ]  " in line:
            notrunning += 1

    # print results
    print("There are", i, "processes available on the machine.", running, "of this processes are running and"
          , notrunning, "not.")

    # if there are less than 20 processes and less than 10 running processes, based on the services,
    # the machine is not a normal network machine
    if i < 20 and running < 10:
        print("Based on the services, this machine seems to be not a normal used network machine.\n")
    else:
        print("Based on the services, this machine seems to be a normal used network machine.\n")


def local():
    print("\nThe following actions are done by the script:")

    detectionMethod1() # detection of standard honeypot account configuration
    detectionMethod2() # detection of standard honeypot files and folders
    detectionMethod3() # TODO check network traffic of the machine
    detectionMethod4() # TODO check services of machine


local()
