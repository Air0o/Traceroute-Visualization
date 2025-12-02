from scapy.all import *
from scapy.layers.inet import IP, UDP
from colorama import Fore, Back, Style, init
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

print(Fore.WHITE)

def traceroute(destination, max_hops=30, timeout=1):
    hops = []
    port = 33434
    ttl = 1

    while True:
        ip_packet = IP(dst=destination, ttl=ttl)
        udp_packet = UDP(dport=port)

        packet = ip_packet / udp_packet

        reply = sr1(packet, timeout=timeout, verbose=0)

        if reply is None:
            # No reply
            print(Fore.YELLOW + f"*No reply (TTL:{ttl})" + Fore.WHITE)
        elif reply.type == 3:
            # Destination reached
            print(Fore.GREEN + "Destination reached!")
            print("Drawing complete journey:" + Fore.WHITE)
            hops.append(reply.src)
            break
        else:
            # Printing the IP of the hop
            hops.append(reply.src)
            print(f"Hop (TTL:{ttl})")

        ttl += 1

        if ttl > max_hops:
            print(Fore.RED + "Destination NOT reached!")
            print("Drawing successful hops:" + Fore.WHITE)
            break
    return hops
