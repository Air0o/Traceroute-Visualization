from scapy.all import *
from scapy.layers.inet import IP, UDP
from colorama import Fore, Back, Style, init
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

init(autoreset=False)  # enables ANSI on Windows
print(Fore.WHITE)

def traceroute(destination, max_hops=32, timeout=2):
    hops = []
    port = 33434
    ttl = 1

    while True:
        # Creating the IP and UDP headers
        ip_packet = IP(dst=destination, ttl=ttl)
        udp_packet = UDP(dport=port)

        # Combining the headers
        packet = ip_packet / udp_packet

        # Sending the packet and receive a reply
        reply = sr1(packet, timeout=timeout, verbose=0)

        if reply is None:
            # No reply, print * for timeout
            print(Fore.YELLOW + f"*No reply (TTL:{ttl})" + Fore.WHITE)
        elif reply.type == 3:
            # Destination reached, print the details
            print(Fore.GREEN + "Destination reached!")
            print("Drawing complete journey:" + Fore.WHITE)
            hops.append(reply.src)
            break
        else:
            # Printing the IP address of the intermediate hop
            #print(f"hop {ttl}\t{reply.src}")
            hops.append(reply.src)
            print(f"Hop (TTL:{ttl})")

        ttl += 1

        if ttl > max_hops:
            print(Fore.RED + "Destination NOT reached!")
            print("Drawing successful hops:" + Fore.WHITE)
            break
    return hops
