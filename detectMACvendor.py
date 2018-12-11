import logging
import getmac
import requests
import validators


def macVendor(ip):
    # set api url
    url = "https://api.macvendors.com/"
    vendor = "Could not get the MAC vendor"

    try:
        # get mac address from ip, via passive arp scanning (no network request)
        mac = str(getmac.get_mac_address(ip=str(ip), network_request=False))
        logging.info("The mac address of the machine is: " + mac)
        # check mac address
        if validators.mac_address.mac_address(mac):
            try:
                # Make a get request to get response from the macvendors api
                response = requests.get(url + mac)
                # set response to variable
                vendor = response.content.decode("utf-8")
            except Exception as e:
                logging.warning("The following error raise when trying to get response from macvendors.com:" + str(e))
        else:
            logging.warning("The MAC address of the machine is not valid")
    except Exception as e:
        logging.warning(
            "The following error raise when trying to get the MAC address from the network machine:" + str(e))

    return str(vendor)
