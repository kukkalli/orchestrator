import logging

# libraries should be installed
from requests import get
from requests.auth import HTTPBasicAuth
import json

from configuration_constants import ConfigurationConstants
from odl.inventory_node import InventoryNode
from odl.odl_constants import ODLConstants
from topology.link import Link
from topology.switch import Switch
from topology.switch_port import SwitchPort
from odl.inventory_nodes import InventoryNodes

LOG = logging.getLogger(__name__)


def get_src_dst(switches: list[Switch], node_id: str) -> int:
    for switch in switches:
        if switch.id == node_id:
            return switch.int_id


class ODLHelperFunctions:
    def __init__(self):
        self.auth = HTTPBasicAuth(ConfigurationConstants.ODL_USERNAME, ConfigurationConstants.ODL_PASSWORD)

    def http_get_request_json(self, query) -> dict:
        return dict(json.loads(get(query, headers=ODLConstants.HEADER, auth=self.auth).text))

    def get_topology_info(self) -> dict:
        return self.http_get_request_json(ODLConstants.TOPOLOGY)

    def get_switches_from_inventory(self) -> InventoryNodes:
        root = self.http_get_request_json(ODLConstants.SWITCHES)
        return InventoryNodes(root)

    def get_switch_by_id(self, switch_id: str) -> InventoryNode:
        root = self.http_get_request_json(ODLConstants.SWITCH.format(switch_id=switch_id))
        return InventoryNode(root["node"][0])

    def get_switch_port_data(self, switch_id: str, port_id: str) -> SwitchPort:
        root = self.http_get_request_json(ODLConstants.PORT.format(switch_id=switch_id, port_id=port_id))
        return SwitchPort(switch_id, root['node-connector'][0])

    def get_topology_switches(self) -> list[Switch]:
        topology = self.get_topology_info()
        LOG.debug("topology: {}".format(topology))
        nodes = topology["network-topology"]["topology"][0]["node"]
        LOG.debug(f"nodes:\n{json.dumps(nodes, indent=4, sort_keys=True)}")
        switch_list: list[Switch] = []
        n = 0
        for node in nodes:
            node_id = node['node-id']
            switch_name_split = node_id.split(":")
            LOG.debug(f"switch_name_split: {switch_name_split}")
            switch = Switch(n, node['node-id'], "switch" + switch_name_split[1])
            LOG.debug(f"switch: {switch.name}")
            for port in node['termination-point']:
                if "LOCAL" not in port['tp-id']:
                    port_data = self.get_switch_port_data(switch.id, port['tp-id'])
                    if port_data.get_port_state().is_link_down() is False:
                        switch.add_port(port_data)
            switch_list.append(switch)
            n = n + 1
        return switch_list

    def get_topology_links(self, switches: list[Switch]) -> list[Link]:
        topology = self.get_topology_info()
        links: list[Link] = []
        n = 0
        for link in topology["network-topology"]["topology"][0]["link"]:
            LOG.debug(f'link: {link}')
            LOG.debug(f'link: {link}')
            _id = link['link-id']
            int_id = n
            dst_node_id = link['destination']['dest-node']
            dst_port_id = link['destination']['dest-tp']
            src_node_id = link['source']['source-node']
            src_port_id = link['source']['source-tp']
            LOG.debug(f'--------------------- link: ---------------------')
            LOG.debug(f"link  id: {_id}, int_id: {int_id}")
            LOG.debug(f"link: dst-nid: {dst_node_id}, dst-pid: {dst_port_id}")
            LOG.debug(f"link: src-nid: {src_node_id}, src-pid: {src_port_id}")
            src_port = self.get_switch_port_data(src_node_id, src_port_id)
            dst_port = self.get_switch_port_data(dst_node_id, dst_port_id)
            capacity = src_port.capacity
            if src_port.capacity > dst_port.capacity:
                capacity = dst_port.capacity

            _link = Link(_id, int_id, get_src_dst(switches, dst_node_id), get_src_dst(switches, src_node_id),
                         dst_port_id, src_port_id, capacity)
            links.append(_link)
            n = n + 1
        return links

    """
    def build_topology(self, _id: str) -> Topology:
        switches = self.get_topology_switches()
        links = self.get_topology_links(switches)
        topology = Topology(_id, links, [], switches, [])
        topology.build()
        return topology
    """


def main():
    odl = ODLHelperFunctions()
    switches = odl.get_topology_switches()
    for switch in switches:
        print(f"switch id: {switch.id}")
        for port in switch.get_ports():
            print(f"port id: {port.id}")
            print(f"is port link down: {port.get_port_state().is_link_down()}")
            print(f"port capacity: {port.capacity}")
            print(f"is port link down: {port.get_port_state().is_live()} {port.get_port_state().is_blocked()}")
    for link in odl.get_topology_links(switches):
        print(f"link: {link.id}")
        print(f"link: {link.capacity}")

    node = odl.get_switch_by_id("openflow:1")
    print(f"node id: {node.id}")
    print(f"node port_number: {node.port_number}")
    print(f"node ip_address: {node.ip_address.ip}")

    """
    node = odl.get_nodes_from_inventory().get_node_by_id("openflow:2")
    print(f'Node: {node.id}')
    flow_table = node.get_flow_table_by_id(0)
    print(f'Flow Table: {flow_table.id}')
    # flow = flow_table.get_flow_by_src_ip_dest_ip("", "10.11.1.213/32")
    flow = flow_table.get_flow_by_src_ip_dest_ip("1.1.1.1/8", "2.2.2.2/8")
    print(f'Flow: {flow.id}')
    # flow_by_id = flow_table.get_flow_by_id("#UF$TABLE*0-63")
    print(f'Flow By Id: {flow.id}: {flow.to_string()}')
    flow_statistics = flow.flow_statistics
    print(f'Flow Statistics: {flow_statistics.to_string()}')
    packet_count = flow_statistics.packet_count
    print(f'Packet Count: {packet_count}')
    # topology = odl.build_topology("my topology")
    # print("Switch ID {}".format(topology.get_switch_by_int_id(1).id))
    # for link in topology.links:
    #    print("link {}".format(link.id))
    #    print(odl.get_switch_port_data('openflow:4', 'openflow:4:10').port_stats.receive_errors)
    """


if __name__ == "__main__":
    main()
