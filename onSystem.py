import os

def onSystem():
    if os.path.isdir('/etc/passwd') or os.path.exists('/etc/passwd'):
        file = open('/etc/passwd', 'r')
        content = file.read()
        file.close()

        if "kippo" in content or "Kippo" in content:
            print("Kippo detected")
        elif "cowrie" in content or "Cowrie" in content:
            print("Cowrie detected")
        elif "tsec" in content or "Tsec" in content or "tpot" in content or "Tpot" in content:
            print("T-potce detected")
        elif "t-sec" in content or "Tsec" in content or "tpot" in content or "Tpot" in content:
            print("T-potce detected")
        else:
            print("No honeypot account configuration found.")
    else:
        print("No such file or directory: '/etc/passwd'.")