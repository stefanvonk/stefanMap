import pasive
import active
import onSystem
import nmapSystemScan
import help

# definieren variabelen

def main():
    choise = input("p    : pasive scanning\na    : active scanning\no    : on system scanning\nf    : full nmap system scan\n\nMake your choice: ")

    if choise == "p":
        result = pasive.pasive()
    elif choise == "a":
        result = active.active()
    elif choise == "o":
        result = onSystem.onSystem()
    elif choise == "f":
        result = nmapSystemScan.scanSystem()
    else:
        help.help()

    print(result)

main()