def onSystem():
    file = open('/etc/passwd', 'r')
    content = file.read()
    file.close()

    print(content)