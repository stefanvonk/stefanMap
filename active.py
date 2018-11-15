import kippoDetect
import detectKippoCowrie
import isPortOpen

def active():
    status = 0

    ip = input("\nEnter a host IP for scanning: ")
    print("\n")

    # Test 1, score 0 - 1
    status += kippoDetect.checkKippo(ip)

    # Test 2, score 0 - 3
    status += detectKippoCowrie.checkKippoCowrie(ip)

    # T-Pot dashboard - ip:64297, score 0 - 1
    if isPortOpen.isOpen(ip, 64297):
        status += 1
        print("[*] Port 64297 is open. It is possible the dashboard of a T-Pot honeynetwork.")





    result = str(status) + " / 5"

    return result