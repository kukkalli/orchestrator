import logging
from typing import List, Dict

from odl.odl_helper import ODLHelperFunctions
from odl.openflow import OpenFlow
from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.nova.nova_details import Nova
from topology.link import Link
from topology.node import Node
from topology.compute_server import ComputeServer
from topology.server import Server
from topology.switch import Switch
from topology.switch_port import SwitchPort
from topology.topology import Topology

LOG = logging.getLogger(__name__)


class ServerSwitchLinks:
    def __init__(self, server: str, switch: str, port: str, capacity: int = 10000000, link_length: float = 0.001,
                 delay_per_km: float = 0.035):
        self.server = server
        self.switch = switch
        self.port = port
        self.capacity = capacity
        self.link_length = link_length  # length in km
        self.delay = link_length * delay_per_km  # in microseconds
        self.delay_per_km = delay_per_km  # in microseconds


class TopologyBuilder:

    def __init__(self, topology_id):
        self.__id = topology_id
        self.odl = ODLHelperFunctions()
        self.switches: List[Switch] = []  # TODO remove later
        self.get_topology_switches()  # TODO remove later
        # self.switches = self.odl.get_topology_switches() # TODO Uncomment later
        self.links: List[Link] = []  # TODO remove later
        self.get_topology_links()  # TODO remove later
        # self.links = self.odl.get_topology_links(self.switches) # TODO Uncomment later
        self.compute_servers: List[ComputeServer] = []
        self.other_servers: List[Server] = []
        self.hypervisors = Nova(AuthenticateConnection()).get_hypervisor_list()
        int_id = len(self.switches)

        for hypervisor in self.hypervisors:
            server = ComputeServer(int_id, hypervisor)
            self.compute_servers.append(server)
            int_id = int_id + 1
        self.add_external_servers(int_id, "controller", "controller")
        int_id = int_id + 1
        self.add_external_servers(int_id, "rrh", "rrh")
        self.hardcoded_links()

    def get_topology_switches(self):
        for i in range(4):
            self.switches.append(Switch(i, f"switch{i + 1}", f"switch{i + 1}"))
            # print(f"the value of i is : {i}")

    def get_topology_links(self):
        source_dest: List[List] = [[0, 2], [2, 0], [0, 3], [3, 0], [1, 2], [2, 1], [1, 3], [3, 1]]
        for i in range(len(source_dest)):
            # print(f"the value of i is : {i}")
            capacity = 40000000
            link_length = 0.001
            delay_per_km = 0.035

            self.links.append(Link(f"link_{i}", i, source_dest[i][1], source_dest[i][0],
                                   f"switch{source_dest[i][1] + 1}_switch{source_dest[i][0] + 1}",
                                   f"switch{source_dest[i][0] + 1}_switch{source_dest[i][1] + 1}",
                                   capacity, link_length, delay_per_km))

            self.switches[source_dest[i][0]].add_port(SwitchPort(f"switch{source_dest[i][0] + 1}",
                                                                 f"switch{source_dest[i][0] + 1}_"
                                                                 + f"switch{source_dest[i][1] + 1}"))
        # print(f"break point")

    @property
    def id(self):
        return self.__id

    def build_topology(self) -> Topology:
        topology = Topology(self.__id, self.links, self.compute_servers, self.switches, self.other_servers)
        topology.build()
        # LOG.info("no of links: {}".format(len(topology.links)))
        # LOG.info("no of servers: {}".format(len(topology.compute_servers)))
        # LOG.info("no of switches: {}".format(len(topology.switches)))
        return topology

    def add_external_servers(self, int_id: int, str_id: str, name: str):
        server = Server(int_id, str_id, name)
        self.other_servers.append(server)

    def hardcoded_links(self):
        link_length = 0.001
        delay_per_km = 0.035
        mapped_physical_links: List[ServerSwitchLinks] = [ServerSwitchLinks(server="compute02", switch="switch4",
                                                                            port="10", link_length=link_length,
                                                                            delay_per_km=delay_per_km),
                                                          ServerSwitchLinks(server="compute03", switch="switch3",
                                                                            port="10", link_length=link_length,
                                                                            delay_per_km=delay_per_km),
                                                          ServerSwitchLinks(server="compute01", switch="switch3",
                                                                            port="11", link_length=link_length,
                                                                            delay_per_km=delay_per_km),
                                                          ServerSwitchLinks(server="controller", switch="switch3",
                                                                            port="9", link_length=link_length,
                                                                            delay_per_km=delay_per_km),
                                                          ServerSwitchLinks(server="rrh", switch="switch4",
                                                                            port="11", link_length=link_length,
                                                                            delay_per_km=delay_per_km)
                                                          ]
        """
        Create DHCP Flows to controller
        ovs-ofctl add-flow br-tuc11 tp_src=67,actions=10,11,9
        ovs-ofctl add-flow br-tuc11 tp_src=68,actions=10,11,9
        """
        # of = OpenFlow()

        for element in mapped_physical_links:
            # LOG.debug(element.server + " <=> " + element.switch + ":" + element.port)
            # print(element.server + " <=> " + element.switch + ":" + element.port)
            self.add_physical_link(element)

    def add_physical_link(self, element: ServerSwitchLinks):
        links_length = len(self.links)
        # LOG.debug("links_length: {}".format(links_length))
        id_name = element.server + "-" + element.switch
        # print(f"element.server: {element.server}")
        # LOG.debug(f"element.server: {element.server}")
        # print(f"id_name: {id_name}, dst_node: {self.get_node_by_name(element.switch).name},"
        #       f" src_node: {self.get_node_by_name(element.server).name}")
        # LOG.debug(f"id_name: {id_name}, dst_node: {self.get_node_by_name(element.switch).name},"
        #           f" src_node: {self.get_node_by_name(element.server).name}")
        switch = self.get_node_by_name(element.switch)
        switch_id = switch.id
        switch_node_id = switch.int_id
        switch_port_id = switch_id + ":" + element.port
        server_node_id = self.get_node_by_name(element.server).int_id
        available_capacity = 10000000
        self.links.append(Link(_id=id_name, int_id=links_length,
                               dst_node_id=switch_node_id,
                               src_node_id=server_node_id,
                               dst_port_id=switch_port_id,
                               capacity=available_capacity,
                               length_of_link=element.link_length))
        self.switches[switch_node_id].add_port(SwitchPort(f"switch{switch_node_id + 1}",
                                                          switch_port_id))
        links_length = links_length + 1
        id_name = element.switch + "-" + element.server
        self.links.append(Link(_id=id_name, int_id=links_length,
                               dst_node_id=server_node_id,
                               src_node_id=switch_node_id,
                               src_port_id=switch_port_id,
                               capacity=available_capacity,
                               length_of_link=element.link_length))

    def get_node_by_name(self, node_name) -> Node:
        for switch in self.switches:
            if node_name == switch.name:
                return switch

        for compute_server in self.compute_servers:
            if node_name == compute_server.name:
                return compute_server

        for server in self.other_servers:
            if node_name == server.name:
                return server

    def get_node_int_id_by_node_id(self, node_id) -> int:
        for switch in self.switches:
            if node_id == switch.id:
                return switch.int_id

        for server in self.compute_servers:
            if node_id == server.id:
                return server.int_id


def main():
    builder = TopologyBuilder("hanif")
    topology = builder.build_topology()
    for link in topology.links:
        to_print = "link {}->{}"
        src = ""
        dst = ""
        if link.src_port_id is not None:
            src = link.src_port_id
        else:
            src = link.src_node_id
        if link.dst_port_id is not None:
            dst = link.dst_port_id
        else:
            dst = link.dst_node_id
        print(to_print.format(src, dst))
        print("link id: {}".format(link.int_id))
    print("End of topology Builder main")


if __name__ == "__main__":
    main()
