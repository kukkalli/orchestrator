import logging

import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import httplib2
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
import json

LOG = logging.getLogger(__name__)


# ODL links
# https://docs.opendaylight.org/projects/controller/en/latest/dev-guide.html
# https://docs.opendaylight.org/en/stable-oxygen/user-guide/openflow-plugin-project-user-guide.html

# smaple json for instal flow
# https://apan.net/meetings/apan47/files/35/35-01-06-01.pdf

# https://github.com/fredhsu/odl-scripts/blob/master/python/addflow/odl-addflow.py
# https://fredhsu.wordpress.com/2013/06/14/adding-flows-in-opendaylight-using-python-and-rest-api/
# admin:admin -H 'Content-Type: application/yang.data+xml' -X PUT -d @flow_data.xml
# http://192.168.1.196:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/10
# 'http://localhost:8181/restconf/operational/network-topology:network-topology'
def add_flow(h, uri, d):
    resp, content = h.request(
        uri=uri,
        method='POST',
        headers={'Content-Type': 'application/json'},
        body=json.dumps(d),
        auth=HTTPBasicAuth("admin", "admin")
    )
    return resp, content


class InstallFlow:
    def __init__(self, table, in_port, out_port, node_sw):
        self.table = table
        self.in_port = in_port
        self.out_port = out_port
        self.node_sw = node_sw

    def build_flow_entry(self):
        # *** Example flow: new_flow = {"installInHw":"false","name":"test2","node":{"@id":"00:00:00:00:00:00:00:07",
        # "@type":"OF"},    "ingressPort":"1","priority":"500","etherType":"0x800","nwSrc":"10.0.0.7",
        # "nwDst":"10.0.0.3","actions":"OUTPUT=2"}
        new_flow = {"installInHw": "false"}
        # new_flow.update({"table": self.table})

        new_flow.update({"node": self.node_sw})
        new_flow.update({"IN_PORT": "IN_PORT=" + self.in_port})
        new_flow.update({"actions": "OUTPUT=" + self.out_port})
        return new_flow


#
#
# r = requests.put('http://10.10.0.10:8000/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/10',
# data=open('flow_data.xml', 'rb'), headers={'Content-Type': 'application/yang.data+xml'},
# auth=('admin', 'admin'))
#
#
# f=install_flow('0','14','16','openflow:3')
# url='http://10.10.0.10:8181//restconf/config/opendaylight-inventory:nodes/node/'
# print(f.POST_flow(f.build_flow_entry(),url,))

# it is for local mininet
# url = 'http://10.10.0.10:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:3/table/0/flow/1'

# url = 'http://10.10.0.10:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:3/table/0/flow/1'
# flowtest = {"installInHw":"true","name":"flowtest","node":{"id":"00:00:00:00:00:00:00:03","type":"OF"},"IngressPort":"1","priority":"500","nwSrc":"10.0.0.1","actions":"OUTPUT=1"}

f = open("../post_xml.xml", "r")
data = str(f.read())
print(data)
ET.register_namespace('',
                      "urn:opendaylight:flow:inventory")  # important to register name space other vise we get ns0 for each element
tree = ElementTree.ElementTree(ElementTree.fromstring(data))
root = tree.getroot()
match = ElementTree.Element("match")
root.insert(1, match)  # the first element shows the position
ethernet_match = ElementTree.SubElement(match, "ethernet-match")
ethernet_type = ElementTree.SubElement(ethernet_match, "ethernet-type")
type = ElementTree.SubElement(ethernet_type, "type")
type.text = "666"
arp_op = ElementTree.SubElement(ethernet_match, "arp-op")
arp_op.text = "1"
ElementTree.dump(root)

'''
url = 'http://10.10.0.10:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:3/table/0/flow/111'
header = {"content-type": "application/xml"}

response = requests.put(url, headers=header, data=data, auth=HTTPBasicAuth("admin", "admin"), allow_redirects=True)
print('Response', response)
#
url_list = ['http://10.10.0.10:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:3/table/0/flow/111',

            ]
for url in url_list:
    response = requests.get(url, headers=header, auth=HTTPBasicAuth("admin", "admin"))
    print('Response', response)
'''
