import sys
import peepdf
import zipfile
import os
import shutil

# analyse pdf file
def pdf():
    filename = input("Enter the path of the PDF file you will check (for example: D:/Stefan Vonk/Desktop/file.pdf): ")
    try:
        # parse the pdf file with the peepdf library
        pdf = peepdf.PDFCore.PDFParser().parse(filename, forceMode=True)
        # peepdf need this vtKey to execute his functions
        VT_KEY = 'fc90df3f5ac749a94a94cb8bf87e05a681a2eb001aef34b6a0084b8c22c97a64'

        # create a buffer (with stdout) to put the output of the peepdf library in a variable
        class MyBuffer(object):
            def __init__(self):
                self.buffer = []

            def write(self, *args, **kwargs):
                self.buffer.append(args)

        old_stdout = sys.stdout
        sys.stdout = MyBuffer()

        # execute the peepdf library in the buffer
        peepdf.PDFConsole.PDFConsole(pdf[1], VT_KEY).do_object(argv="16")
        my_buffer, sys.stdout = sys.stdout, old_stdout

        # put the buffer to the variable content
        content = str(my_buffer.buffer)

        # check if part of canarytoken url is in the filecontent
        if "/URI http://" in content and ".canarytokens.net/" in content and "/S /URI" in content:
            print("\nThis PDF file is probably a Canarytoken.")
        else:
            print("\nThis PDF file is probably not a Canarytoken.")

    # print possible error messages
    except Exception as e:
        print("\n" + str(e))

# analyse windows folder
def folder():
    foldername = input("Enter the path of the Windows Folder you will check (for example: D:/Stefan Vonk/Desktop/My Documents/): ")
    filename = "/desktop.ini"
    try:
        # open file and read the content to variable
        file = open(foldername + filename, 'r', encoding='utf-16')
        content = str(file.read())
        file.close()

        # check if part of canarytoken url is in the filecontent
        if "%USERNAME%.%USERDOMAIN%.INI." in content and ".canarytokens.com" in content and "resource.dll" in content:
            print("\nThis Windows Folder is probably a Canarytoken.")
        else:
            print("\nThis Windows Folder is probably not a Canarytoken.")

    # print possible error messages
    except Exception as e:
        print("\n" + str(e))

# analyse microsoft word file
def word():
    wordfile = input("Enter the path of the Microsoft Word file you will check (for example: D:/Stefan Vonk/Desktop/file.docx): ")
    try:
        # remove old unzip-docx directory
        if os.path.isdir("unzip-docx"):
            shutil.rmtree("unzip-docx")

        # create unzip-docx directory
        os.mkdir("unzip-docx")

        # unzip word file to unzip-docx directory
        zip = zipfile.ZipFile(wordfile)
        zip.extractall("unzip-docx")

        # if exists, open file footer3.xml and read the content to a variable
        if os.path.exists('unzip-docx/word/footer2.xml'):
            file = open("unzip-docx/word/footer2.xml", 'r')
            content = file.read()
            file.close()
            # check if part of canarytoken url is in the filecontent
            if 'INCLUDEPICTURE  "http://canarytokens.com/feedback/images/terms/' in content and '/contact.php" \d  \* MERGEFORMAT' in content:
                print("\nThis Windows Folder is probably a Canarytoken.")
            else:
                print("\nThis Windows Folder is probably not a Canarytoken.")
        else:
            print("\nThis Windows Folder is probably not a Canarytoken.")

    # print possible error messages
    except Exception as e:
        print("\n" + str(e))

# main function
def honeytoken():
    print("Hello, this is a proof of concept to detect honeytokens. Welcome! This script is created by Stefan Vonk, "
          "for purpose of analyse whether files or directories are canarytokens or not.\n")
    print("Choose the sort of token you want to analyse:")

    choise = input("a    : PDF file\nb    : Windows Folder\nc    : Microsoft Word Document\n\nMake your choice: ")

    if choise == "a":
        pdf()
    elif choise == "b":
        folder()
    elif choise == "c":
        word()
    else:
       print("you have entered a wrong input.\n")
       honeytoken()

# execute main function
honeytoken()