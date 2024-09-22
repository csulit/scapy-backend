import multiprocessing
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1
import pusher
import time
import socket
import os
from dotenv import load_dotenv

load_dotenv()

def is_valid_address(address):
    try:
        socket.gethostbyname(address)
        return True
    except socket.error:
        return False

def send_ping(target, iface=None):
    if not is_valid_address(target):
        return f"{target} is an invalid address"
    
    response = sr1(IP(dst=target)/ICMP(), timeout=2, iface=iface)
    if response is None:
        return f"{target} is unreachable"
    else:
        return f"{target} is reachable"

def notify_pusher(message):
    pusher_client = pusher.Pusher(
        app_id=os.getenv('PUSHER_APP_ID'),
        key=os.getenv('PUSHER_KEY'),
        secret=os.getenv('PUSHER_SECRET'),
        cluster=os.getenv('PUSHER_CLUSTER')
    )
    pusher_client.trigger('my-channel', 'my-event', {'message': message})

def ping_and_notify(target_hosts, iface=None):
    # Create a multiprocessing pool with a larger number of processes
    pool = multiprocessing.Pool(processes=100)
    
    # Send ping requests in parallel
    results = pool.starmap(send_ping, [(target, iface) for target in target_hosts])
    
    for target, result in zip(target_hosts, results):
        print(result)
        if "unreachable" in result or "invalid address" in result:
            notify_pusher(result)

if __name__ == "__main__":
    target_hosts = [
        "google.com", "facebook.com", "amazon.com", "apple.com", "microsoft.com",
        "netflix.com", "yahoo.com", "wikipedia.org", "twitter.com", "linkedin.com",
        "instagram.com", "reddit.com", "pinterest.com", "tumblr.com", "paypal.com",
        "github.com", "stackoverflow.com", "dropbox.com", "spotify.com", "adobe.com",
        "bing.com", "quora.com", "medium.com", "twitch.tv", "ebay.com",
        "salesforce.com", "oracle.com", "zoom.us", "slack.com", "airbnb.com",
        "uber.com", "lyft.com", "snapchat.com", "tiktok.com", "wechat.com",
        "baidu.com", "alibaba.com", "jd.com", "hulu.com", "disneyplus.com"
    ]
    
    # Specify the network interface to use
    network_interface = "en0"  # Replace with your network interface name
    
    try:
        while True:
            ping_and_notify(target_hosts, iface=network_interface)
            time.sleep(60)  # Wait for 1 minute before the next execution
    except KeyboardInterrupt:
        pass