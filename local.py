# with this script you can test whether the machine where you are on is a honeypot or not.
# This script is standalone with no dependencies.

import os
import struct

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

def main():
    print("The following actions are done by the script:")

    ########## method 1 ##########
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
        # the other honeypots don't have a standard yser account
        else:
            print("No standard honeypot account configuration found.")
    else:
        print("No such file or directory: '/etc/passwd'. This machine is probably not a honeypot because it isn't"
              " running a linux system.")

    ########## method 2 ##########
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
        rootDir = '/home/'
        # walk through each subdirectory
        for dirName, subdirList, fileList in os.walk(rootDir):
            folderName = '%s' % dirName
            # check if the honeypot strings are in the folder names
            if "cowrie" in folderName:
                cowrie += 1
            elif "kippo" in folderName:
                kippo += 1
            elif "sshesame" in folderName:
                sshesame += 1
            elif "mhn" in folderName:
                mhn += 1
            elif "dionaea" in folderName:
                dionaea += 1
            elif "t-pot" in folderName or "tpot" in folderName or "t-sec" in folderName or "tsec" in folderName:
                tpot += 1

            # loop through each filename
            for fname in fileList:
                fileName = fname
                # check if the honeypot strings are in the filenames
                if "cowrie" in fileName:
                    cowrie += 1
                elif "kippo" in fileName:
                    kippo += 1
                elif "sshesame" in fileName:
                    sshesame += 1
                elif "mhn" in fileName:
                    mhn += 1
                elif "dionaea" in fileName:
                    dionaea += 1
                elif "t-pot" in fileName or "tpot" in fileName or "t-sec" in fileName or "tsec" in fileName:
                    tpot += 1
    except Exception as e:
        print("The following error raise when trying to map the filesystem: " + str(e))

    # if one of the variables > 10, a standard honeypot configuration is found
    if cowrie > 10:
        print("A machine configuration found with standard cowrie honeypot files and folders.")
    elif kippo > 10:
        print("A machine configuration found with standard kippo honeypot files and folders.")
    elif sshesame > 10:
        print("A machine configuration found with standard sshesame honeypot files and folders.")
    elif mhn > 10:
        print("A machine configuration found with standard modern honeynetwork files and folders.")
    elif dionaea > 10:
        print("A machine configuration found with standard dionaea honeypot files and folders.")
    elif tpot > 10:
        print("A machine configuration found with standard T-pot honeypot files and folders.")
    else:
        print("No standard honeypot machine configuration found.")

    ########## method 3 ##########
    print("\n#3: Check the networktraffic of the machine.")


    ########## method 4 ##########
    print("\n#4: check the services of the machine.")


    ########## method 5 ##########
    print("\n#5: Detect virtualization of the machine.")

    name = "0"
    hid = "0"
    hid2 = "0"
    try:
        hid = cpuHypervisorID()
        if hid == 'VMwareVMware':
            name = 'vmware'
        elif hid == 'Microsoft Hv':
            name = 'hyperv'
        elif hid == 'XenVMMXenVMM':
            name = 'xen'
        elif hid == 'KVMKVMKVM':
            name = 'kvm'
    except Exception as e:
        print("The following error raise when trying to detect virtualization: " + str(e))

    try:
        hid2 = cpuModelName()
        if 'QEMU' in hid2:
            name = 'qemu'
    except Exception as e:
        print("The following error raise when trying to detect virtualization: " + str(e))

    print(name)
    print(hid)
    print(hid2)

main()
