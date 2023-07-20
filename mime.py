#mime.py
import requests
from scapy.all import *
import threading
import os
url = 'http://192.168.1.209/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Content-Type': 'text/html'
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
        print("Mime sniffing - ICMP Type:", icmp_type)

        if icmp_type == 3:
            #stop_execution = True  # Set the flag to stop execution
            success = False
            print("Stopping mime sniffing execution due to Type 3 ICMP response.")
            return success

    else:
        print("Mime sniffing - No ICMP response captured.")

def main():
    # Start the packet sniffing thread
    sniff_thread = threading.Thread(target=sniff_icmp_response)
    sniff_thread.start()

    try:
        response = requests.get(url, headers=headers)
        response_code = response.status_code
        print("Mime sniffing request successful. Response code:", response_code)
        success = True
    except requests.exceptions.RequestException as e:
        print("Mime sniffing request failed. Exception:", e)
        success = False
    finally:
        # Check if execution should be stopped
        #if stop_execution:
        #    print("Stopping mime sniffing execution due to Type 3 ICMP response.")
        #    os._exit(0)  # Stop execution immediately

        # Wait for the sniffing thread to complete
        sniff_thread.join()

        print("Mime sniffing execution completed.")
        return success

    