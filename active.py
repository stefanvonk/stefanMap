import kippoDetect

def active():
    status = 0

    ip = input("Enter host IP for scanning: ")
    status += kippoDetect.kippoDetect(ip)







    result = status + " / 1"

    return result