# With this script you can test whether the machine where you are on is a honeypot or not. This script is standalone with no dependencies.

import os

def onSystem():
    print("The following actions are done by the script:")

    # Check /etc/passwd if there are standard honeypots accounts
    print("\n#1: Check if there are standard honeypot accounts on the machine.")
    if os.path.isdir('/etc/passwd') or os.path.exists('/etc/passwd'):
        file = open('/etc/passwd', 'r')
        content = file.read()
        file.close()

        if "kippo" in content or "Kippo" in content:
            print("Kippo useraccount detected")
        elif "cowrie" in content or "Cowrie" in content:
            print("Cowrie useraccount detected")
        elif "tsec" in content or "Tsec" in content or "tpot" in content or "Tpot" in content:
            print("T-potce useraccount detected")
        elif "t-sec" in content or "T-sec" in content or "t-pot" in content or "T-pot" in content:
            print("T-potce useraccount detected")
        else:
            print("No honeypot account configuration found.")
    else:
        print("No such file or directory: '/etc/passwd'. This machine is probably not a honeypot because it isn't running a linux system.")

    # Check the whole filesystem if there are files or folders that are from honeypot configuration
    # print("\n#2: Check if there are standard honeypot directories on the machine.")
    # if os.path.isdir('/home/kippo'):
    #     print("Directory '/home/kippo' detected")
    # elif os.path.isdir('/home/cowrie'):
    #     print("Directory '/home/cowrie' detected")
    # else:
    #     print("No standard honeypot directory detected")

    rootDir = '/home/'
    for dirName, subdirList, fileList in os.walk(rootDir):
        folderName = '%s' % dirName
        if "cowrie" in folderName:
            print(folderName)
        elif "kippo" in folderName:
            print(folderName)
        elif "sshesame" in folderName:
            print(folderName)
        elif "mhn" in folderName:
            print(folderName)
        elif "dionaea" in folderName:
            print(folderName)
        elif "t-pot" in folderName:
            print(folderName)
        for fname in fileList:
            fileName = fname
            if "cowrie" in fileName:
                print(folderName+'/'+fileName)
            elif "kippo" in fileName:
                print(folderName+'/'+fileName)
            elif "sshesame" in fileName:
                print(folderName+'/'+fileName)
            elif "mhn" in fileName:
                print(folderName+'/'+fileName)
            elif "dionaea" in fileName:
                print(folderName+'/'+fileName)
            elif "t-pot" in fileName:
                print(folderName+'/'+fileName)