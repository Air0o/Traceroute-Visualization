from locator import locate_ip, print_ip_data, is_private
from traceroute import traceroute
from window_manager import start_window
import socket

print("Insert an IP address to trace")
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