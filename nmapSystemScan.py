import nmap

def scanSystem():
    ip = input("\nEnter a host IP for scanning the entire network where this IP participate: ")
    print("\n")

    nm = nmap.PortScanner()
    nm.scan(hosts=ip + '/24', arguments='-n -sP -PE -PA21,23,80,3389')
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    for host, status in hosts_list:
        print('{0}:{1}'.format(host, status))

