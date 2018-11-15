import kippoDetect
import detectKippoCowrie

def active():
    status = 0

    ip = input("\nEnter host IP for scanning: ")
    print("\n")

    # Test 1, score 0 - 1
    status += kippoDetect.checkKippo(ip)

    # Test 2, score 0 - 3
    status += detectKippoCowrie.checkKippoCowrie(ip)







    result = str(status) + " / 4"

    return result