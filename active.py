import kippoDetect

def active():
    status = 0

    ip = input("\nEnter host IP for scanning: ")
    print("\n")
    status += kippoDetect.kippoDetect(ip)







    result = str(status) + " / 1"

    return result