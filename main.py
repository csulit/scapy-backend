import multiprocessing
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1
import pusher
import time
import socket
import os
from dotenv import load_dotenv
from datetime import datetime

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
    # Create a multiprocessing pool with a number of processes equal to the number of CPUs
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    
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
        "baidu.com", "alibaba.com", "jd.com", "hulu.com", "disneyplus.com",
        "cnn.com", "bbc.com", "nytimes.com", "forbes.com", "bloomberg.com",
        "reuters.com", "wsj.com", "guardian.co.uk", "ft.com", "economist.com",
        "techcrunch.com", "wired.com", "engadget.com", "mashable.com", "theverge.com",
        "cnet.com", "gizmodo.com", "arstechnica.com", "zdnet.com", "venturebeat.com",
        "businessinsider.com", "huffpost.com", "buzzfeed.com", "vox.com", "slate.com",
        "vice.com", "theatlantic.com", "newyorker.com", "politico.com", "axios.com",
        "npr.org", "pbs.org", "cbsnews.com", "abcnews.go.com", "nbcnews.com",
        "foxnews.com", "msnbc.com", "usatoday.com", "latimes.com", "chicagotribune.com",
        "dailymail.co.uk", "mirror.co.uk", "thesun.co.uk", "telegraph.co.uk", "independent.co.uk",
        "metro.co.uk", "express.co.uk", "standard.co.uk", "eveningstandard.co.uk", "cityam.com",
        "boston.com", "sfgate.com", "seattletimes.com", "denverpost.com", "dallasnews.com",
        "miamiherald.com", "startribune.com", "azcentral.com", "freep.com", "detroitnews.com",
        "cleveland.com", "oregonlive.com", "tampabay.com", "philly.com", "baltimoresun.com",
        "newsday.com", "nypost.com", "nydailynews.com", "chron.com", "sacbee.com",
        "kcstar.com", "stltoday.com", "twincities.com", "desmoinesregister.com", "omaha.com",
        "indystar.com", "courier-journal.com", "cincinnati.com", "dispatch.com", "oklahoman.com",
        "arkansasonline.com", "clarionledger.com", "jacksonville.com", "orlandosentinel.com", "sun-sentinel.com",
        "heraldtribune.com", "tallahassee.com", "gainesville.com", "naplesnews.com", "news-press.com",
        "palmbeachpost.com", "myajc.com", "savannahnow.com", "augustachronicle.com", "macon.com",
        "ledger-enquirer.com", "thestate.com", "postandcourier.com", "greenvilleonline.com", "goupstate.com",
        "thesunnews.com", "islandpacket.com", "charlotteobserver.com", "newsobserver.com", "heraldsun.com",
        "fayobserver.com", "starnewsonline.com", "wilmingtonstar.com", "myrtlebeachonline.com", "charleston.net",
        "post-gazette.com", "phillytrib.com", "pennlive.com", "mcall.com", "yorkdispatch.com",
        "lancasteronline.com", "delcotimes.com", "timesleader.com", "citizensvoice.com", "thetimes-tribune.com",
        "triblive.com", "observer-reporter.com", "altoonamirror.com", "lewistownsentinel.com", "dailyitem.com",
        "sunburynews.com", "dailyamerican.com", "heraldstandard.com", "tribdem.com", "indianagazette.com",
        "thecourierexpress.com", "theprogressnews.com", "lockhaven.com", "williamsport.com", "sun-gazette.com",
        "thederrick.com", "meadvilletribune.com", "sharonherald.com", "thecranberryeagle.com", "butlereagle.com",
        "ellwoodcityledger.com", "beavercountytimes.com", "timesonline.com", "newcastleherald.com", "theherald.com.au",
        "smh.com.au", "theage.com.au", "brisbanetimes.com.au", "watoday.com.au", "canberratimes.com.au",
        "theaustralian.com.au", "dailytelegraph.com.au", "heraldsun.com.au", "couriermail.com.au", "adelaidenow.com.au",
        "perthnow.com.au", "ntnews.com.au", "themercury.com.au", "geelongadvertiser.com.au", "goldcoastbulletin.com.au",
        "townsvillebulletin.com.au", "cairnspost.com.au", "thechronicle.com.au", "sunshinecoastdaily.com.au", "northernstar.com.au",
        "dailyexaminer.com.au", "qt.com.au", "frasercoastchronicle.com.au", "gladstoneobserver.com.au", "themorningbulletin.com.au",
        "dailymercury.com.au", "theadvocate.com.au", "examiner.com.au", "thecourier.com.au", "standard.net.au",
        "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au",
        "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au",
        "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au",
        "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au",
        "canberratimes.com.au", "theland.com.au", "theadvocate.com.au", "examiner.com.au", "thecourier.com.au",
        "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au",
        "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au",
        "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au",
        "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au",
        "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au", "theadvocate.com.au", "examiner.com.au",
        "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au",
        "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au",
        "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au",
        "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au",
        "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au", "theadvocate.com.au",
        "examiner.com.au", "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au",
        "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au",
        "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au",
        "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au",
        "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au",
        "theadvocate.com.au", "examiner.com.au", "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au",
        "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au",
        "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au",
        "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au",
        "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au",
        "theland.com.au", "theadvocate.com.au", "examiner.com.au", "thecourier.com.au", "standard.net.au",
        "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au",
        "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au",
        "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au",
        "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au",
        "canberratimes.com.au", "theland.com.au", "theadvocate.com.au", "examiner.com.au", "thecourier.com.au",
        "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au",
        "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au",
        "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au",
        "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au",
        "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au", "theadvocate.com.au", "examiner.com.au",
        "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au",
        "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au",
        "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au",
        "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au",
        "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au", "theadvocate.com.au",
        "examiner.com.au", "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au",
        "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au",
        "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au",
        "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au",
        "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au",
        "theadvocate.com.au", "examiner.com.au", "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au",
        "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au",
        "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au",
        "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au",
        "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au",
        "theland.com.au", "theadvocate.com.au", "examiner.com.au", "thecourier.com.au", "standard.net.au",
        "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au",
        "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au",
        "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au",
        "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au",
        "canberratimes.com.au", "theland.com.au", "theadvocate.com.au", "examiner.com.au", "thecourier.com.au",
        "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au",
        "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au",
        "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au",
        "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au",
        "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au", "theadvocate.com.au", "examiner.com.au",
        "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au",
        "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au",
        "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au",
        "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au",
        "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au", "theadvocate.com.au",
        "examiner.com.au", "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au",
        "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au",
        "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au",
        "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au",
        "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au",
        "theadvocate.com.au", "examiner.com.au", "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au",
        "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au",
        "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au",
        "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au",
        "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au",
        "theland.com.au", "theadvocate.com.au", "examiner.com.au", "thecourier.com.au", "standard.net.au",
        "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au",
        "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au",
        "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au",
        "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au",
        "canberratimes.com.au", "theland.com.au", "theadvocate.com.au", "examiner.com.au", "thecourier.com.au",
        "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au",
        "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au",
        "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au",
        "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au",
        "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au", "theadvocate.com.au", "examiner.com.au",
        "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au",
        "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au",
        "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au",
        "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au",
        "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au", "theadvocate.com.au",
        "examiner.com.au", "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au",
        "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au",
        "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au",
        "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au",
        "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au",
        "theadvocate.com.au", "examiner.com.au", "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au",
        "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au",
        "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au",
        "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au",
        "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au",
        "theland.com.au", "theadvocate.com.au", "examiner.com.au", "thecourier.com.au", "standard.net.au",
        "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au",
        "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au",
        "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au",
        "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au",
        "canberratimes.com.au", "theland.com.au", "theadvocate.com.au", "examiner.com.au", "thecourier.com.au",
        "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au",
        "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au",
        "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au",
        "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au",
        "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au", "theadvocate.com.au", "examiner.com.au",
        "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au",
        "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au",
        "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au",
        "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au",
        "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au", "theadvocate.com.au",
        "examiner.com.au", "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au",
        "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au",
        "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au",
        "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au",
        "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au",
        "theadvocate.com.au", "examiner.com.au", "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au",
        "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au",
        "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au",
        "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au",
        "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au",
        "theland.com.au", "theadvocate.com.au", "examiner.com.au", "thecourier.com.au", "standard.net.au",
        "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au",
        "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au",
        "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au",
        "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au",
        "canberratimes.com.au", "theland.com.au", "theadvocate.com.au", "examiner.com.au", "thecourier.com.au",
        "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au",
        "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au",
        "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au",
        "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au",
        "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au", "theadvocate.com.au", "examiner.com.au",
        "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au",
        "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au",
        "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au",
        "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au",
        "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au", "theadvocate.com.au",
        "examiner.com.au", "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au",
        "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au",
        "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au",
        "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au",
        "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au", "theland.com.au",
        "theadvocate.com.au", "examiner.com.au", "thecourier.com.au", "standard.net.au", "thewarrnamboolstandard.com.au",
        "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au", "broomead.com.au",
        "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au", "augustamargaretrivermail.com.au",
        "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au", "bunburymail.com.au",
        "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au", "canberratimes.com.au",
        "theland.com.au", "theadvocate.com.au", "examiner.com.au", "thecourier.com.au", "standard.net.au",
        "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au", "albanyadvertiser.com.au",
        "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au", "busseltonmail.com.au",
        "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au", "colliemail.com.au",
        "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au", "goulburnpost.com.au",
        "canberratimes.com.au", "theland.com.au", "theadvocate.com.au", "examiner.com.au", "thecourier.com.au",
        "standard.net.au", "thewarrnamboolstandard.com.au", "thecouriermail.com.au", "thewest.com.au", "kalminer.com.au",
        "albanyadvertiser.com.au", "broomead.com.au", "geraldtonguardian.com.au", "pilbaranews.com.au", "soundtelegraph.com.au",
        "busseltonmail.com.au", "augustamargaretrivermail.com.au", "manjimupbridgetownmail.com.au", "harveyreporter.com.au", "donnybrookmail.com.au",
        "colliemail.com.au", "bunburymail.com.au", "southcoastregister.com.au", "illawarramercury.com.au", "southernhighlandnews.com.au",
        "baidu.com", "alibaba.com", "jd.com", "hulu.com", "disneyplus.com"
    ]
    
    # Specify the network interface to use
    network_interface = "eth0"  # Replace with your network interface name
    
    try:
        while True:
            start_time = datetime.now()
            ping_and_notify(target_hosts, iface=network_interface)
            end_time = datetime.now()
            elapsed_time = (end_time - start_time).total_seconds()
            print(f"Time taken to ping all targets: finished in {elapsed_time:.2f} seconds")
            print(f"DNS list count: {len(target_hosts)}")
            time.sleep(60)  # Wait for 1 minute before the next execution
    except KeyboardInterrupt:
        pass