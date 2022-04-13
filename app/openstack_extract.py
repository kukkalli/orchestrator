import logging

LOG = logging.getLogger(__name__)


def extract_mac(obj, _id):
    for item in obj["ports"]:
        if item['id'] == _id:
            return item['mac_address']


def extract_ip(obj, _id):
    for item in obj["ports"]:
        if item['id'] == _id:
            return item["fixed_ips"][0]["ip_address"]
