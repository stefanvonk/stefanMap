import nmap

def scanSystem():
    ip = input("\nEnter a host IP for scanning the entire network where this IP participate: ")

    ######################################################################## check ip

    print("\n")

    nm = nmap.PortScanner()
    nm.scan(hosts=ip + '/24', arguments='-n -sP -PE')
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    for host, status in hosts_list:
        print('{0}:{1}'.format(host, status))