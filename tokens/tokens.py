import sys
import peepdf
import zipfile
import os
import shutil


def pdf():
    # analyze pdf file
    filename = input("Enter the path of the PDF file you will check (for example: D:/Stefan Vonk/Desktop/file.pdf): ")
    try:
        # parse the pdf file with the peepdf library
        pdf_file = peepdf.PDFCore.PDFParser().parse(filename, forceMode=True)
        # peepdf need this vtKey to execute his functions
        vt_key = 'fc90df3f5ac749a94a94cb8bf87e05a681a2eb001aef34b6a0084b8c22c97a64'

        # create a buffer (with stdout) to put the output of the peepdf library in a variable
        class MyBuffer(object):
            def __init__(self):
                self.buffer = []

            def write(self, *args, **kwargs):
                self.buffer.append(args)

        # change stdout
        old_stdout = sys.stdout
        sys.stdout = MyBuffer()

        # execute the peepdf library in the buffer
        # whit this library read object 16 from the pdf file
        peepdf.PDFConsole.PDFConsole(pdf_file[1], vt_key).do_object(argv="16")

        # set buffer to variable my_buffer and rechange stdout
        my_buffer, sys.stdout = sys.stdout, old_stdout

        # put the buffer to the variable content
        content = str(my_buffer.buffer)

        # check if part of canarytoken url is in the content of object 16 of the pdf
        if "/URI http://" in content and ".canarytokens.net/" in content and "/S /URI" in content:
            print("\nThis PDF file is probably a Canarytoken.")
        else:
            print("\nThis PDF file is probably not a Canarytoken.")

    # print possible error messages
    except Exception as e:
        print("\n" + str(e))

    # close program
    sys.exit(0)


def folder():
    # analyze windows folder
    foldername = input("Enter the path of the Windows Folder you will check "
                       "(for example: D:/Stefan Vonk/Desktop/My Documents/): ")
    # desktop.ini contains the possible canarytokens url
    filename = "/desktop.ini"
    try:
        # open file and read the content to variable
        file = open(foldername + filename, 'r', encoding='utf-16')
        content = str(file.read())
        file.close()

        # check if part of canarytoken url is in the file content of desktop.ini
        if "%USERNAME%.%USERDOMAIN%.INI." in content and ".canarytokens.com" in content and "resource.dll" in content:
            print("\nThis Windows Folder is probably a Canarytoken.")
        else:
            print("\nThis Windows Folder is probably not a Canarytoken.")

    # print possible error messages
    except Exception as e:
        print("\n" + str(e))

    # close program
    sys.exit(0)


def word():
    # analyze microsoft word file
    wordfile = input("Enter the path of the Microsoft Word file you will check"
                     " (for example: D:/Stefan Vonk/Desktop/file.docx): ")
    try:
        # remove old unzip-docx directory
        if os.path.isdir("unzip-docx"):
            shutil.rmtree("unzip-docx")

        # create unzip-docx directory
        os.mkdir("unzip-docx")

        # unzip word file to unzip-docx directory
        zip_file = zipfile.ZipFile(wordfile)
        zip_file.extractall("unzip-docx")

        # if exists, open file footer2.xml and read the content to a variable
        if os.path.exists('unzip-docx/word/footer2.xml'):
            file = open("unzip-docx/word/footer2.xml", 'r')
            content = file.read()
            file.close()
            # check if part of canarytoken url is in the file content of footer2.xml
            if 'INCLUDEPICTURE  "http://canarytokens.com/feedback/images/terms/' in content \
                    and '/contact.php" \d  \* MERGEFORMAT' in content:
                print("\nThis Windows Folder is probably a Canarytoken.")
            else:
                print("\nThis Windows Folder is probably not a Canarytoken.")
        else:
            print("\nThis Windows Folder is probably not a Canarytoken.")

    # print possible error messages
    except Exception as e:
        print("\n" + str(e))

    # close program
    sys.exit(0)


def tokens():
    # main function
    print("Hello, this is a proof of concept to detect honeytokens. Welcome! This script is created by Stefan Vonk, "
          "for purpose of analyze whether files or directories are canarytokens or not.\n")
    print("Choose the sort of token you want to analyze:")

    choise = input("a    : PDF file\nb    : Windows Folder\nc    : Microsoft Word Document\n\nMake your choice: ")

    if choise == "a":
        pdf()
    elif choise == "b":
        folder()
    elif choise == "c":
        word()
    else:
        print("you have entered a wrong input.\n")
        tokens()


# execute main function
tokens()
