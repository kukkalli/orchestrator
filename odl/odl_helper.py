from typing import List, Dict

# libraries should be installed
from requests import get
from requests.auth import HTTPBasicAuth
import json

from configuration_constants import ConfigurationConstants
from odl.odl_constants import ODLConstants
from topology.link import Link
from topology.port_stats import PortStats
from topology.switch import Switch
from topology.switch_port import SwitchPort
from topology.topology import Topology
from odl.inventory_nodes import InventoryNodes


def get_src_dst(switches: List[Switch], node_id: str) -> int:
    for switch in switches:
        if switch.id == node_id:
            return switch.int_id


class ODLHelperFunctions:
    def __init__(self):
        self.auth = HTTPBasicAuth(ConfigurationConstants.ODL_USERNAME, ConfigurationConstants.ODL_PASSWORD)

    def http_get_request_json(self, query):
        return dict(json.loads(get(query, headers=ODLConstants.HEADER, auth=self.auth).text))

    def get_topology_info(self):
        return self.http_get_request_json(ODLConstants.TOPOLOGY)

    def get_nodes_from_inventory(self):
        root = self.http_get_request_json(ODLConstants.NODES)
        return InventoryNodes(root)

    def get_switch_port_data(self, switch_id: str, port_id: str) -> SwitchPort:
        port_info = self.http_get_request_json(ODLConstants.PORT.format(switch_id, port_id))
        port = port_info['node-connector'][0]
        name = port.get('flow-node-inventory:name')
        number = port.get('flow-node-inventory:port-number')
        capacity = port.get('flow-node-inventory:maximum-speed')

        port_stats = port_info['node-connector'][0][
            'opendaylight-port-statistics:flow-capable-node-connector-statistics']
        _port_stats = PortStats(port_stats)
        switch_port = SwitchPort(_id=port_id, name=name, port_number=number, switch_id=switch_id, capacity=capacity,
                                 port_stats=_port_stats)
        switch_port.set_mac(port.get('flow-node-inventory:hardware-address'))
        return switch_port

    def get_topology_switches(self) -> List[Switch]:
        topology = self.get_topology_info()
        print("topology: {}".format(topology))
        nodes = topology["network-topology"]["topology"][0]["node"]
        # print("nodes: {}".format(nodes))
        switch_list: List[Switch] = []
        n = 0
        for node in nodes:
            switch = Switch(node['node-id'], n)
            for port in node['termination-point']:
                if "LOCAL" not in port['tp-id']:
                    switch.add_port(self.get_switch_port_data(switch.id, port['tp-id']))
            switch_list.append(switch)
            n = n + 1
        return switch_list

    def get_topology_links(self, switches: List[Switch]) -> List[Link]:
        topology = self.get_topology_info()
        links: List[Link] = []
        n = 0
        for link in topology["network-topology"]["topology"][0]["link"]:
            _id = link['link-id']
            int_id = n
            dst_node_id = link['destination']['dest-node']
            dst_port_id = link['destination']['dest-tp']
            src_node_id = link['source']['source-node']
            src_port_id = link['source']['source-tp']
            _link = Link(_id, int_id, get_src_dst(switches, dst_node_id), get_src_dst(switches, src_node_id),
                         dst_port_id, src_port_id)
            links.append(_link)
            n = n + 1
        return links

    def get_switch_by_id(self, switch_id: str):
        return self.http_get_request_json(ODLConstants.NODE.format(switch_id))

    def build_topology(self, _id: str) -> Topology:
        switches = self.get_topology_switches()
        links = self.get_topology_links(switches)
        topology = Topology(_id, links, [], switches)
        topology.build()
        return topology


def main():
    odl = ODLHelperFunctions()
    node = odl.get_nodes_from_inventory().get_node_by_id("openflow:2")
    print(f'Node: {node.id}')
    flow_table = node.get_flow_table_by_id(0)
    print(f'Flow Table: {flow_table.id}')
    # flow = flow_table.get_flow_by_src_ip_dest_ip("", "10.11.1.213/32")
    flow = flow_table.get_flow_by_src_ip_dest_ip("10.11.1.213/32", "10.11.1.0/24")
    print(f'Flow: {flow.id}')
    flow_by_id = flow_table.get_flow_by_id("#UF$TABLE*0-63")
    print(f'Flow By Id: #UF$TABLE*0-63: {flow.to_string()}')
    flow_statistics = flow.flow_statistics
    print(f'Flow Statistics: {flow_statistics.to_string()}')
    packet_count = flow_statistics.packet_count
    print(f'Packet Count: {packet_count}')
    # topology = odl.build_topology("my topology")
    # print("Switch ID {}".format(topology.get_switch_by_int_id(1).id))
    # for link in topology.links:
    #    print("link {}".format(link.id))
    #    print(odl.get_switch_port_data('openflow:4', 'openflow:4:10').port_stats.receive_errors)


if __name__ == "__main__":
    main()
