import pasive, active, onSystem, help

# definieren variabelen

def main():
    choise = input("p    : pasive scanning\na    : active scanning\no    : on system scanning\n\nMake your choice: ")

    if choise == "p":
        result = pasive.pasive()
    elif choise == "a":
        result = active.active()
    elif choise == "o":
        result = onSystem.onSystem()
    else:
        help.help()

    print(result)

main()