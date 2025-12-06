from scapy.all import sr1, sr, ICMP, conf
from scapy.layers.inet import IP, UDP
from colorama import Fore, Back, Style, init
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

print(Fore.WHITE)

conf.verb = 0
init(autoreset=True)

from scapy.all import sr1, IP, UDP, ICMP, conf
from colorama import Fore, init
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
conf.verb = 0
init(autoreset=True)

def traceroute(destination, max_hops=30, timeout=2, retries=2, max_consecutive_timeouts=5):
    hops = []
    port = 33434
    ttl = 1
    consecutive_timeouts = 0
    destination_reached = False

    while ttl <= max_hops and not destination_reached:
        reply = None

        # --- Try UDP probe first ---
        for attempt in range(retries):
            packet = IP(dst=destination, ttl=ttl) / UDP(dport=port)
            reply = sr1(packet, timeout=timeout, verbose=0)
            if reply:
                break

        # --- If no UDP reply, try ICMP Echo ---
        if reply is None:
            for attempt in range(retries):
                icmp_pkt = IP(dst=destination, ttl=ttl) / ICMP()
                reply = sr1(icmp_pkt, timeout=timeout, verbose=0)
                if reply:
                    break

        if reply is None:
            print(Fore.YELLOW + f"*No reply at TTL {ttl}" + Fore.WHITE)
            consecutive_timeouts += 1
            if consecutive_timeouts >= max_consecutive_timeouts:
                print(Fore.RED + "Too many consecutive timeouts, aborting." + Fore.WHITE)
                break
        else:
            consecutive_timeouts = 0
            src_ip = reply.src
            icmp_layer = reply.getlayer(ICMP)

            if icmp_layer:
                if icmp_layer.type == 11:  # Time Exceeded
                    hops.append(src_ip)
                    print(Fore.CYAN + f"Hop {ttl}: {src_ip}" + Fore.WHITE)
                elif icmp_layer.type in (0, 3):  # Echo Reply or Port Unreachable
                    hops.append(src_ip)
                    print(Fore.GREEN + f"Destination reached at TTL {ttl}: {src_ip}" + Fore.WHITE)
                    destination_reached = True
                else:
                    hops.append(src_ip)
                    print(Fore.CYAN + f"Hop {ttl}: {src_ip} (ICMP type {icmp_layer.type})" + Fore.WHITE)
            else:
                hops.append(src_ip)
                print(Fore.CYAN + f"Hop {ttl}: {src_ip}" + Fore.WHITE)

            # Extra safeguard: if reply.src == destination, stop
            if src_ip == destination:
                print(Fore.GREEN + "Destination reached by IP match!" + Fore.WHITE)
                destination_reached = True

        ttl += 1

    if not destination_reached:
        print(Fore.RED + "Destination NOT reached!" + Fore.WHITE)

    return hops
