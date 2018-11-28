import os
from pathlib import Path

# Analyse PDF file
def pdf():
   print("pdf")

# Analyse Windows Folder
def folder():
   foldername = input("Enter the path of the Windows Folder you will check: ")
   foldername = "D:/Stefan Vonk/Desktop/My Documents/"
   filename = "/desktop.ini"
   # file = None
   try:
      file = open(foldername + filename, 'r')
      print(file)
      content = file.read()
      file.close()
      print(content)
      if "IconResource=\\%USERNAME%.%USERDOMAIN%.INI." in content or ".com\resource.dll" in content:
         print("This Windows Folder is probably a Canarytoken.\n")
      else:
         print("This Windows Folder is probably not a Canarytoken.\n")
   except Exception as e:
      print(str(e))
   # finally:
   #    file.close()

# Analyse Microsoft Word file
def word():
   print("word")

# Main function
def honeytoken():
    print("Choose the Canarytoken to analyse.")

    choise = input("a    : pdf\nb    : Windows Folder\nc    : Microsoft Word Document\nd    : full nmap system scan\n\nMake your choice: ")

    if choise == "a":
        result = pdf()
    elif choise == "b":
        folder()
    elif choise == "c":
       result = word()
    else:
       print("you have entered a wrong input.")
       honeytoken()

    if "result" in locals() or "result" in globals():
        print(result)

# Execute main function
honeytoken()