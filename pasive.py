import time
import math

def GetNetworkInterfaces():
    ifaces = []
    f = open("/proc/net/dev")
    data = f.read()
    f.close()
    data = data.split("\n")[2:]
    for i in data:
        if len(i.strip()) > 0:
            x = i.split()
            # Interface |                        Receive                          |                         Transmit
            #   iface   | bytes packets errs drop fifo frame compressed multicast | bytes packets errs drop fifo frame compressed multicast
            k = {
                "interface" :   x[0][:len( x[0])-1],
                "tx"        :   {
                    "bytes"         :   int(x[1]),
                    "packets"       :   int(x[2]),
                    "errs"          :   int(x[3]),
                    "drop"          :   int(x[4]),
                    "fifo"          :   int(x[5]),
                    "frame"         :   int(x[6]),
                    "compressed"    :   int(x[7]),
                    "multicast"     :   int(x[8])
                },
                "rx"        :   {
                    "bytes"         :   int(x[9]),
                    "packets"       :   int(x[10]),
                    "errs"          :   int(x[11]),
                    "drop"          :   int(x[12]),
                    "fifo"          :   int(x[13]),
                    "frame"         :   int(x[14]),
                    "compressed"    :   int(x[15]),
                    "multicast"     :   int(x[16])
                }
            }
            ifaces.append(k)
    return ifaces

def pasive():
    INTERVAL = 1  # 1 second
    AVG_LOW_PASS = 0.2  # Simple Complemetary Filter

    ifaces = {}

    print("Loading Network Interfaces")
    idata = GetNetworkInterfaces()
    print("Filling tables")
    for eth in idata:
        ifaces[eth["interface"]] = {
            "rxrate": 0,
            "txrate": 0,
            "avgrx": 0,
            "avgtx": 0,
            "toptx": 0,
            "toprx": 0,
            "sendbytes": eth["tx"]["bytes"],
            "recvbytes": eth["rx"]["bytes"]
        }

    while True:
        idata = GetNetworkInterfaces()
        for eth in idata:
            #   Calculate the Rate
            ifaces[eth["interface"]]["rxrate"] = (eth["rx"]["bytes"] - ifaces[eth["interface"]]["recvbytes"]) / INTERVAL
            ifaces[eth["interface"]]["txrate"] = (eth["tx"]["bytes"] - ifaces[eth["interface"]]["sendbytes"]) / INTERVAL

            #   Set the rx/tx bytes
            ifaces[eth["interface"]]["recvbytes"] = eth["rx"]["bytes"]
            ifaces[eth["interface"]]["sendbytes"] = eth["tx"]["bytes"]

            #   Calculate the Average Rate
            ifaces[eth["interface"]]["avgrx"] = int(
                ifaces[eth["interface"]]["rxrate"] * AVG_LOW_PASS + ifaces[eth["interface"]]["avgrx"] * (
                            1.0 - AVG_LOW_PASS))
            ifaces[eth["interface"]]["avgtx"] = int(
                ifaces[eth["interface"]]["txrate"] * AVG_LOW_PASS + ifaces[eth["interface"]]["avgtx"] * (
                            1.0 - AVG_LOW_PASS))

            #   Set the Max Rates
            ifaces[eth["interface"]]["toprx"] = ifaces[eth["interface"]]["rxrate"] if ifaces[eth["interface"]][
                                                                                          "rxrate"] > \
                                                                                      ifaces[eth["interface"]][
                                                                                          "toprx"] else \
            ifaces[eth["interface"]]["toprx"]
            ifaces[eth["interface"]]["toptx"] = ifaces[eth["interface"]]["txrate"] if ifaces[eth["interface"]][
                                                                                          "txrate"] > \
                                                                                      ifaces[eth["interface"]][
                                                                                          "toptx"] else \
            ifaces[eth["interface"]]["toptx"]

            print("%s: in B/S" % (eth["interface"]))
            print("\tRX - MAX: %s AVG: %s CUR: %s" % (
            ifaces[eth["interface"]]["toprx"], ifaces[eth["interface"]]["avgrx"], ifaces[eth["interface"]]["rxrate"]))
            print("\tTX - MAX: %s AVG: %s CUR: %s" % (
            ifaces[eth["interface"]]["toptx"], ifaces[eth["interface"]]["avgtx"], ifaces[eth["interface"]]["txrate"]))
            print("")
        time.sleep(INTERVAL)

    ######## network traffic