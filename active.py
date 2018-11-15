import kippoDetect, detectKippoCowrie

def active():
    status = 0

    ip = input("\nEnter host IP for scanning: ")
    print("\n")

    # Test 1
    status += kippoDetect.main(ip)

    # Test 2
    status += detectKippoCowrie(ip)







    result = str(status) + " / 1"

    return result