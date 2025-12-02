from scapy.all import sr1, sr, ICMP, conf
from scapy.layers.inet import IP, UDP
from colorama import Fore, Back, Style, init
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

print(Fore.WHITE)

conf.verb = 0
init(autoreset=True)

def traceroute(destination, max_hops=30, timeout=2, retries=2):
    hops = []
    port = 33434
    ttl = 1

    while True:
        reply = None

        for attempt in range(retries):
            packet = IP(dst=destination, ttl=ttl) / UDP(dport=port)
            reply = sr1(packet, timeout=timeout, verbose=0)
            if reply is not None:
                break

        if reply is None:
            print(Fore.YELLOW + f"*No UDP reply (TTL:{ttl}), trying ICMP..." + Fore.WHITE)
            for attempt in range(retries):
                icmp_pkt = IP(dst=destination, ttl=ttl) / ICMP()
                reply = sr1(icmp_pkt, timeout=timeout, verbose=0)
                if reply is not None:
                    break

        if reply is None:
            # no reply
            print(Fore.YELLOW + f"*No reply at TTL {ttl}" + Fore.WHITE)
        else:
            icmp_layer = reply.getlayer(ICMP)
            if icmp_layer is not None:
                icmp_type = icmp_layer.type

                if icmp_type == 11:
                    hops.append(reply.src)
                    print(Fore.CYAN + f"Hop {ttl}: {reply.src}" + Fore.WHITE)
                elif icmp_type == 3 or icmp_type == 0:
                    print(Fore.GREEN + "Destination reached!" + Fore.WHITE)
                    hops.append(reply.src)
                    break
                else:
                    hops.append(reply.src)
                    print(Fore.CYAN + f"Hop {ttl}: {reply.src} (ICMP type {icmp_type})" + Fore.WHITE)
            else:
                try:
                    src = reply.src
                except Exception:
                    src = str(reply.summary())
                hops.append(src)
                print(Fore.CYAN + f"Hop {ttl}: {src}" + Fore.WHITE)

        ttl += 1

        if ttl > max_hops:
            print(Fore.RED + "Destination NOT reached!" + Fore.WHITE)
            break

    return hops
