import multiprocessing
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1, srp
from scapy.layers.l2 import ARP, Ether
import time
import socket
from datetime import datetime

def is_valid_address(address):
    try:
        socket.gethostbyname(address)
        return True
    except socket.error:
        return False

def send_ping(target, iface=None):
    if not is_valid_address(target):
        return f"{target} is an invalid address"
    
    response = sr1(IP(dst=target)/ICMP(), timeout=2, iface=iface, verbose=False)
    if response is None:
        return f"{target} is unreachable"
    else:
        return f"{target} is reachable"

def log_messages(messages):
    for message in messages:
        print(f"Alert: {message}")

def get_ip_from_mac(mac_address, network_range, interface="eth0"):
    # Create an ARP request packet
    arp_request = ARP(pdst=network_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp_request

    # Send the packet and capture the response
    result = srp(packet, iface=interface, timeout=2, verbose=False)[0]

    # Iterate through the responses and match the MAC address
    for sent, received in result:
        if received.hwsrc.lower() == mac_address.lower():
            return received.psrc  # Return the IP address

    return None

def ping_and_notify(target_records, iface=None):
    # Dictionary to store MAC to IP mappings
    mac_to_ip = {}
    
    # First get all IP addresses for the MAC addresses
    for record in target_records:
        mac_address = record["mac_address"]
        network_range = record["network_range"]
        ip = get_ip_from_mac(mac_address, network_range, iface)
        if ip:
            mac_to_ip[mac_address] = ip
    
    # Create a list of IPs to ping
    ip_addresses = list(mac_to_ip.values())
    
    # Create a multiprocessing pool
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    
    # Send ping requests in parallel
    results = pool.starmap(send_ping, [(ip, iface) for ip in ip_addresses])
    
    # Process results
    unreachable_messages = []
    for mac_address, ip in mac_to_ip.items():
        result = results[ip_addresses.index(ip)]
        print(f"MAC: {mac_address} -> {result}")
        if "unreachable" in result or "invalid address" in result:
            unreachable_messages.append(result)
    
    if unreachable_messages:
        log_messages(unreachable_messages)

if __name__ == "__main__":
    # Sample target records with MAC addresses and network ranges
    target_records = [
        {"mac_address": "00:15:65:E8:0E:69", "network_range": "192.168.13.83/22"},
        {"mac_address": "88:43:E1:55:22:74", "network_range": "192.168.13.65/22"},
        {"mac_address": "00:02:FD:FF:9A:7D", "network_range": "192.168.12.68/22"},
        {"mac_address": "80:5E:C0:63:80:5A", "network_range": "192.168.12.207/22"}
        # Add more records as needed
    ]
    
    # Specify the network interface to use
    network_interface = "eth0"  # Replace with your network interface name
    
    try:
        while True:
            start_time = datetime.now()
            ping_and_notify(target_records, iface=network_interface)
            end_time = datetime.now()
            elapsed_time = (end_time - start_time).total_seconds()
            print(f"Time taken to ping all targets: finished in {elapsed_time:.2f} seconds")
            print(f"MAC address records count: {len(target_records)}")
            time.sleep(60)  # Wait for 1 minute before the next execution
    except KeyboardInterrupt:
        pass