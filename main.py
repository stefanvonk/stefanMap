import pasive, active, onSystem

# definieren variabelen

def main():
    print("Hello, this is honey-detect. Welcome! This script is created by Stefan Vonk, for purpose of honeypot detection.\n")
    print("Choose one of the integers below to execute a detection script:\n")
    print("1    : Pasive detection")
    print("2    : Active detection")
    print("3    : On system detection\n")

    keuze = input("Make your choice: ")

    if keuze == "1":
        print("1")
        pasive.pasive()
    elif keuze == "2":
        print("2")
        active.active()
    elif keuze == "3":
        print("3")
        onSystem.onSystem()

main()