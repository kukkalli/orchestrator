def extract_mac(obj, id):
    for item in obj["ports"]:
        if item['id'] == id:
            return item['mac_address']


def extract_ip(obj, id):
    for item in obj["ports"]:
        if item['id'] == id:
            return item["fixed_ips"][0]["ip_address"]
