import requests  # library should be installed
from requests.auth import HTTPBasicAuth
import json
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from configuration_constants import ConfigurationConstants
from odl.odl_constants import ODLConstants
import time
import pprint


def flow_id_generator():
    return round(time.time() * 1000000)  # create flow_id based on time


class OpenFlow:

    def __init__(self):
        self.auth = HTTPBasicAuth(ConfigurationConstants.ODL_USERNAME, ConfigurationConstants.ODL_PASSWORD)

    def http_get_request_json(self, query):
        return dict(json.loads(requests.get(query, headers=ODLConstants.HEADER, auth=self.auth).text))

    def http_post_request_json(self, query):
        return dict(json.loads(requests.post(query, headers=ODLConstants.HEADER, auth=self.auth).text))

    def http_put_request_json(self, url, body):

        response = requests.put(url, data=json.dumps(body), headers=ODLConstants.HEADER, auth=self.auth,
                                allow_redirects=True)
        return response

    def http_put_request_xml(self, url, body):
        response = requests.put(url, data=str(body), headers=ODLConstants.PUT_XML_HEADER, auth=self.auth,
                                allow_redirects=True)
        return response

    def http_delete_request_json(self, query):
        return dict(json.loads(requests.delete(query, headers=ODLConstants.HEADER, auth=self.auth).text))

    # arp_op request:1 and reply:2
    def create_arp_flow(self, node_id, output, arp_opcode, table=0, hard_timeout=0, idle_timeout=0, cookie=1,
                        priority=101):
        print("Create ARP from switch {} on port {} with apr code {}".format(node_id, output, arp_opcode))

        flow_id = flow_id_generator()
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
        flow_id = flow_id_generator()
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
        xml_body = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + xml_body
        # create url for ip
        ip_url = ODLConstants.PUT_FLOW_URL.format(node_id=node_id, table=table, flow_id=flow_id)
        print(f"body:\n{xml_body}\nip_url: {ip_url}")
        print(f"Response: {self.http_put_request_xml(ip_url, xml_body)}")

    def json_forwarding_flow_install(self, node_id, output, src_ip, dst_ip, table=0, hard_timeout=0, idle_timeout=0,
                                     cookie=1, priority=666):

        print("Create Data flow from switch {} on port {} with dst ip {}".format(node_id, output, dst_ip))
        flow_id = flow_id_generator()
        flow_json_body = json.loads(ODLConstants.FLOW_JSON)
        # flow_json_body['flow-node-inventory:flow'][0]['flow-name']='json_test'
        flow_json_body['flow-node-inventory:flow'][0]['id'] = 10
        flow_json_body['flow-node-inventory:flow'][0]['hard-timeout'] = hard_timeout
        flow_json_body['flow-node-inventory:flow'][0]['idle-timeout'] = idle_timeout
        flow_json_body['flow-node-inventory:flow'][0]['cookie'] = cookie
        flow_json_body['flow-node-inventory:flow'][0]['priority'] = priority
        flow_json_body['flow-node-inventory:flow'][0]['table_id'] = table
        flow_json_body['flow-node-inventory:flow'][0]['match']['ipv4-source'] = src_ip
        flow_json_body['flow-node-inventory:flow'][0]['match']['ipv4-destination'] = dst_ip
        flow_json_body['flow-node-inventory:flow'][0]['match']['ethernet-match']['ethernet-type'][
            'type'] = ODLConstants.ETHER_TYPE_IP_MATCHER
        flow_json_body['flow-node-inventory:flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0][
            'output-action']['output-node-connector'] = output
        # print(flow_json_body['flow-node-inventory:flow'][0]['instructions']['instruction'][0]['apply-actions'][
        # 'action'][0]['output-action']['output-node-connector'] ) pprint.pprint((flow_json_body))
        print(json.dumps(flow_json_body))
        # print((ODLConstants.HEADER))
        # create url for ip
        ip_url = ODLConstants.PUT_FLOW_URL.format(node_id=node_id, table=table, flow_id=10)
        print(f"ip_url: {ip_url}")
        print(f"Response: {self.http_put_request_json(ip_url, flow_json_body)}")


def main():
    # ------test
    a = OpenFlow()
    # url, body = a.create_arp_flow('openflow:3', 77, 1)
    # print(url, '\n', body)
    a.json_forwarding_flow_install('openflow:2', 77, '1.1.1.1/32', "2.2.2.2/32")
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

if __name__ == "__main__":
    main()
