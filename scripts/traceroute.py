import socket
import struct
import time
from scapy.all import *
import argparse

from scapy.layers.inet import IP, UDP


def traceroute(destination, max_hops=30, timeout=2):
    hops = []
    destination_ip = socket.gethostbyname(destination)
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
            print(f"{ttl}\t*")
        elif reply.type == 3:
            # Destination reached, print the details
            #print(f"{ttl}\t{reply.src}")
            hops.append(reply.src)
            break
        else:
            # Printing the IP address of the intermediate hop
            #print(f"hop {ttl}\t{reply.src}")
            hops.append(reply.src)

        ttl += 1

        if ttl > max_hops:
            break
    return hops
