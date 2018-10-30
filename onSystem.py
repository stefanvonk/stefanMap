def onSystem():
    file = open('/etc/passwd', 'r')
    content = file.read()
    file.close()

    if content.find("kippo") or content.find("Kippo"):
        print("Kippo detected")
    elif content.find("cowrie") or content.find("Cowrie"):
        print("Cowrie detected")
    elif content.find("tsec") or content.find("Tsec") or content.find("tpot") or content.find("Tpot"):
        print("T-potce detected")
    else:
        print("No honeypot account configuration found.")