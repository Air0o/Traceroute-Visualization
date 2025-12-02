from locator import locate_ip, print_ip_data, is_private
from traceroute import traceroute
from window_manager import start_window
from colorama import Fore, Style, init
import socket
import requests
import ipaddress
import logging
import arcade
import screeninfo
import scapy
import ctypes

init(autoreset=False)

if not ctypes.windll.shell32.IsUserAnAdmin():
    print(Fore.RED + "You must run the program as administrator!" + Style.RESET_ALL)
    input()
    exit()

examples = [
    "google.com",
    "cloudflare.com",
    "1.1.1.1(Cloudflare DNS)",
    "8.8.8.8(Google DNS)",
    "debian.org",
    "ovh.com",
    "yahoo.co.jp",
    "baidu.com",
    "uol.com.br",
]

print("Insert an IP address to trace")
print("Examples: ")
for example in examples:
    print("-",example)
    
ip = str(socket.gethostbyname(str(input())))

hops = traceroute(ip)
coordinates = []

for hop in hops:
    if is_private(hop):
        print("Private Ip address!")
        continue
    data = locate_ip(hop)
    coordinates.append(data.get("loc").split(","))
    print_ip_data(data)

print("hops:", hops)
print("coordinates: ", coordinates)
start_window(coordinates)