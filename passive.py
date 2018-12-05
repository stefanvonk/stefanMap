from p0f import P0f, P0fException
import logging


def passive(ip):
    data = None
    p0f = P0f("p0f.sock")  # point this to socket defined with "-s" argument.
    try:
        data = p0f.get_info(ip)
    except P0fException as e:
        logging.warning("p0f error: Invalid query was sent to p0f, maybe the API is changed: " + str(e))
    except KeyError as e:
        logging.warning("p0f error: No data is available for this IP address: " + str(e))
    except ValueError as e:
        logging.warning("p0f error: p0f returned invalid constant values, maybe the API is changed: " + str(e))

    if data:
        print("First seen:", data["first_seen"])
        print("Last seen:", data["last_seen"])
        print("Total connections:", data["total_conn"])
        print("Uptime:", data["uptime"])
        print("Uptime (min):", data["uptime_min"])
        print("Uptime (sec):", data["uptime_sec"])
        print("Uptime (days):", data["up_mod_days"])
        print("Last nat connection:", data["last_nat"])
        print("Last OS mismatch:", data["last_chg"])
        print("System distance:", data["distance"])
        print("User-Agent or Server strings accuracy:", data["bad_sw"], "// 0: User-Agent not present, 1: OS difference, 2: outright mismatch")
        print("OS match quality:", data["os_match_q"], "// 0: normal match, 1: fuzzy, 2: generic signature, 3: both")
        print("Name of matched OS:", data["os_name"])
        print("OS version:", data["os_flavor"])
        print("Last identified HTTP application:", data["http_name"])
        print("Version of this HTTP application:", data["http_flavor"])
        print("Network link type:", data["link_type"])
        print("System language:", data["language"])

        logging.info("p0f good")
    else:
        print("p0f not good")
        logging.info("p0f not good")