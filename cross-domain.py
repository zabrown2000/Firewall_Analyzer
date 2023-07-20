# cross-domain.py
import requests
from scapy.all import *
import threading
import os
url = 'http://192.168.1.209/'
headers = {
    'Origin': 'http://evil.com'
}

# Shared flag variable between threads
stop_execution = False

# Sniff the ICMP response packets in a separate thread
def sniff_icmp_response():
    global stop_execution
    global success

    packets = sniff(filter="icmp and dst host 192.168.1.101", count=1)
    if packets:
        icmp_type = packets[0][ICMP].type
        print("Cross domain - ICMP Type:", icmp_type)

        if icmp_type == 3:
            #stop_execution = True  # Set the flag to stop execution
            success = False
            print("Stopping cross domain execution due to Type 3 ICMP response.")
            return success

    else:
        print("Cross domain - No ICMP response captured.")

def main():
    # Start the packet sniffing thread
    sniff_thread = threading.Thread(target=sniff_icmp_response)
    sniff_thread.start()

    try:
        response = requests.get(url, headers=headers)
        response_code = response.status_code
        print("Cross domain request successful. Response code:", response_code)
        success = True
    except requests.exceptions.RequestException as e:
        print("Cross domain request failed. Exception:", e)
        success = False
    finally:
        # Check if execution should be stopped
        #if stop_execution:
        #    print("Stopping cross domain execution due to Type 3 ICMP response.")
        #    os._exit(0)  # Stop execution immediately

        # Wait for the sniffing thread to complete
        sniff_thread.join()

        print("Cross domain execution completed.")
        return success

    
