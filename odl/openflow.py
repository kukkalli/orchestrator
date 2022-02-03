import requests  # library should be installed
from requests.auth import HTTPBasicAuth
import json
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from configuration_constants import ConfigurationConstants
from odl.odl_constants import ODLConstants
import time


class OpenFlow:

    def __init__(self):
        self.auth = HTTPBasicAuth(ConfigurationConstants.ODL_USERNAME, ConfigurationConstants.ODL_PASSWORD)

    def http_get_request_json(self, query):
        return dict(json.loads(requests.get(query, headers=ODLConstants.HEADER, auth=self.auth).text))

    def http_post_request_json(self, query):
        return dict(json.loads(requests.post(query, headers=ODLConstants.HEADER, auth=self.auth).text))

    def http_put_request_xml(self, url, body):
        response = requests.put(url, data=str(body), headers=ODLConstants.PUT_XML_HEADER, auth=self.auth,
                                allow_redirects=True)
        return response

    def http_delete_request_json(self, query):
        return dict(json.loads(requests.delete(query, headers=ODLConstants.HEADER, auth=self.auth).text))

    def flow_id_generator(self):
        return round(time.time() * 1000000)  # create flow_id based on time

    # arp_op request:1 and reply:2
    def create_arp_flow(self, node_id, output, arp_opcode, table=0, hard_timeout=0, idle_timeout=0, cookie=1,
                        priority=101):
        print("Create ARP from switch {} on port {} with apr code {}".format(node_id, output, arp_opcode))

        flow_id = self.flow_id_generator()
        arp_xml_body = ODLConstants.FLOW_XML.format(hard_timeout=hard_timeout, idle_timeout=idle_timeout,
                                                    cookie=cookie, priority=priority, flow_id=flow_id,
                                                    table=table, output_action=output)
        # important to register name space otherwise we get ns0 for each element
        ET.register_namespace('', "urn:opendaylight:flow:inventory")

        tree = ET.ElementTree(ET.fromstring(arp_xml_body))
        root = tree.getroot()
        match = ET.Element("match")
        root.insert(1, match)  # the first element shows the position
        ethernet_match = ET.SubElement(match, "ethernet-match")
        ethernet_type = ET.SubElement(ethernet_match, "ethernet-type")
        _type = ET.SubElement(ethernet_type, "type")
        _type.text = ODLConstants.ETHER_TYPE_ARP_MATCHER
        arp_op = ET.SubElement(match, "arp-op")
        if arp_opcode == 1:
            arp_op.text = ODLConstants.ARP_REQUEST_OP
        elif arp_opcode == 2:
            arp_op.text = ODLConstants.ARP_REPLY_OP
        xml_body = ET.tostring(root).decode()

        # create url for this specific flow
        arp_url = ODLConstants.PUT_FLOW_URL.format(node_id=node_id, table=table, flow_id=flow_id)
        self.http_put_request_xml(arp_url, xml_body)

    # ip format: ip with subnet 10.0.1.1/32
    def create_traffic_forwarding(self, node_id, output, src_ip, dst_ip, table=0, hard_timeout=0, idle_timeout=0,
                                  cookie=1, priority=101):
        print("Create Data flow from switch {} on port {} with dst ip {}".format(node_id, output, dst_ip))
        flow_id = self.flow_id_generator()
        flow_xml_body = ODLConstants.FLOW_XML.format(hard_timeout=hard_timeout, idle_timeout=idle_timeout,
                                                     cookie=cookie, priority=priority, flow_id=flow_id,
                                                     table=table, output_action=output)

        # important to register name space otherwise we get ns0 for each element
        ET.register_namespace('', "urn:opendaylight:flow:inventory")
        tree = ElementTree.ElementTree(ElementTree.fromstring(flow_xml_body))
        root = tree.getroot()
        match = ElementTree.Element("match")
        root.insert(1, match)  # the first element shows the position
        ethernet_match = ElementTree.SubElement(match, "ethernet-match")
        ethernet_type = ElementTree.SubElement(ethernet_match, "ethernet-type")
        _type = ElementTree.SubElement(ethernet_type, "type")
        _type.text = ODLConstants.ETHER_TYPE_IP_MATCHER
        ipv4_source = ElementTree.SubElement(match, "ipv4-source")
        ipv4_source.text = src_ip  # src ip with subnet 10.0.1.1/24
        ipv4_destination = ElementTree.SubElement(match, "ipv4-destination")
        ipv4_destination.text = dst_ip  # dst ip with subnet 10.0.1.1/24
        xml_body = ElementTree.tostring(root).decode()
        xml_body = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_body
        # create url for ip
        ip_url = ODLConstants.PUT_FLOW_URL.format(node_id=node_id, table=table, flow_id=flow_id)
        print(f"body:\n{xml_body}\nip_url: {ip_url}")
        print(f"Response: {self.http_put_request_xml(ip_url, xml_body)}")


# ------test
a = OpenFlow()
# url, body = a.create_arp_flow('openflow:3', 77, 1)
# print(url, '\n', body)
a.create_traffic_forwarding('openflow:2', 77, '1.1.1.1/32', "10.10.0.10/32")
# print(a.http_put_request_xml(url,body))


"""
<flow xmlns="urn:opendaylight:flow:inventory">
    <hard-timeout>0</hard-timeout>
    <match><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match><ipv4-source>1.1.1.1/32</ipv4-source><ipv4-destination>10.10.0.10/32</ipv4-destination></match><idle-timeout>0</idle-timeout>
    <cookie>1</cookie>
    <priority>101</priority>
    <id>1641468195592085</id>
    <table_id>0</table_id>
    <instructions>
        <instruction>
            <order>0</order>
            <apply-actions>
                <action>
                    <output-action>
                        <output-node-connector>77</output-node-connector>
                    </output-action>
                    <order>0</order>
                </action>
            </apply-actions>
        </instruction>
    </instructions>
</flow>

"""