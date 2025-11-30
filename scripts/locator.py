import requests
import ipaddress

def locate_ip(ip):
    token = "e91adaa77c8110"  # Get a free token from ipinfo.io
    url = f"https://ipinfo.io/{ip}?token={token}"

    response = requests.get(url)
    data = response.json()

    return data


def is_private(ip: str) -> bool:
    return ipaddress.ip_address(ip).is_private

def print_ip_data(data):
    print("Ip:", data.get("ip"))
    print("City:", data.get("city"))
    print("Region:", data.get("region"))
    print("Country:", data.get("country"))
    print("Location (lat,long):", data.get("loc"))
    print("ISP:", data.get("org"))
    print("=================")