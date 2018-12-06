import subprocess
import logging


def passive(ip):
    print("\nFor this passive arp scan you need a local arp-scan installation. (Run 'sudo apt-get install arp-scan')")

    # subprocess.run(["sudo", "arp-scan", "-l", ip])

    # data = None
    # p0f = P0f("/etc/p0f/p0f.fp")  # point this to socket defined with "-s" argument.
    # try:
    #     data = p0f.get_info(ip, True)
    #     p0f.close()
    # except P0fException as e:
    #     logging.warning("p0f error: Invalid query was sent to p0f, maybe the API is changed: " + str(e))
    # except KeyError as e:
    #     logging.warning("p0f error: No data is available for this IP address: " + str(e))
    # except ValueError as e:
    #     logging.warning("p0f error: p0f returned invalid constant values, maybe the API is changed: " + str(e))
    #
    # if data:
    #     print("Magic:", data["magic"])
    #     print("Status:", data["status"])
    #     print("First seen:", data["first_seen"])
    #     print("Last seen:", data["last_seen"])
    #     print("Total connections:", data["total_conn"])
    #     print("Uptime (min):", data["uptime_min"])
    #     print("Uptime (days):", data["up_mod_days"])
    #     print("Last nat connection:", data["last_nat"])
    #     print("Last OS mismatch:", data["last_chg"])
    #     print("System distance:", data["distance"])
    #     print("User-Agent or Server strings accuracy:", data["bad_sw"], "// 0: User-Agent not present, 1: OS difference, 2: outright mismatch")
    #     print("OS match quality:", data["os_match_q"], "// 0: normal match, 1: fuzzy, 2: generic signature, 3: both")
    #     print("Name of matched OS:", data["os_name"])
    #     print("OS version:", data["os_flavor"])
    #     print("Last identified HTTP application:", data["http_name"])
    #     print("Version of this HTTP application:", data["http_flavor"])
    #     print("Network link type:", data["link_type"])
    #     print("System language:", data["language"])
    #
    #     logging.info("p0f good")
    # else:
    #     print("p0f not good")
    #     logging.info("p0f not good")

    print("\n\nFor details about the process of scanning, check the logfile 'stefanMap.log'.\n")