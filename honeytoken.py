import configparser
import zipfile
import os
import shutil

# analyse pdf file
def pdf():
   print("pdf")

# analyse windows folder
def folder():
    # foldername = input("Enter the path of the Windows Folder you will check (for example: D:/Stefan Vonk/Desktop/files/): ")
    foldername = "D:/Stefan Vonk/Desktop/files/"
    filename = "/desktop.ini"
    try:
        # open file and read the content to variable
        file = open(foldername + filename, 'r', encoding='utf-16')
        content = str(file.read())
        file.close()
        print(content)
        #
        # if os.path.exists("honeytoken/desktop.txt"):
        #     os.remove("honeytoken/desktop.txt")
        #
        # file2 = open("honeytoken/desktop.txt", "w+")
        # file2.write(content)
        # file2.close()
        #
        # file3 = open("honeytoken/desktop.txt", 'r')
        # content2 = str(file3.read())
        # file3.close()
        # print(content2)

        # config = configparser.ConfigParser()
        #
        # config.read('D:/Stefan Vonk/Desktop/files/desktop.ini', encoding='utf-16')
        # file = config.get('.ShellClassInfo', 'IconResource')
        # content = open(file, 'r').read()

        # check if part of canarytoken url is in the filecontent
        #
        # !this is not working!
        if "USERNAME" in content:
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
        # remove old honeytoken/unzip-docx directory
        if os.path.isdir("honeytoken/unzip-docx"):
            shutil.rmtree("honeytoken/unzip-docx")

        # create new honeytoken/unzip-docx directory
        os.mkdir("honeytoken/unzip-docx")

        # unzip word file to honeytoken/unzip-docx directory
        zip = zipfile.ZipFile(wordfile)
        zip.extractall("honeytoken/unzip-docx")

        # if exists, open file footer3.xml and read the content to a variable
        if os.path.exists('honeytoken/unzip-docx/word/footer2.xml'):
            file = open("honeytoken/unzip-docx/word/footer2.xml", 'r')
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
    print("Choose the Canarytoken you want to analyse.")

    choise = input("a    : pdf\nb    : Windows Folder\nc    : Microsoft Word Document\n\nMake your choice: ")

    if choise == "a":
        result = pdf()
    elif choise == "b":
        folder()
    elif choise == "c":
       word()
    else:
       print("you have entered a wrong input.")
       honeytoken()

    if "result" in locals() or "result" in globals():
        print(result)

# execute main function
honeytoken()