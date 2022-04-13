import logging
from typing import List

from odl.odl_helper import ODLHelperFunctions
from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.nova.nova_details import Nova
from topology.link import Link
from topology.node import Node
from topology.server import Server
from topology.topology import Topology

LOG = logging.getLogger(__name__)


class ComputeToSwitchLinks:
    def __init__(self, compute: str, switch: str, port: str):
        self.compute = compute
        self.switch = switch
        self.port = port


class TopologyBuilder:

    def __init__(self, topology_id):
        self.__id = topology_id
        self.odl = ODLHelperFunctions()
        self.switches = self.odl.get_topology_switches()
        self.links = self.odl.get_topology_links(self.switches)
        self.servers: List[Server] = []
        self.hypervisors = Nova(AuthenticateConnection().get_connection()).get_hypervisor_list()
        n = len(self.switches)
        for hypervisor in self.hypervisors:
            server = Server(n, hypervisor)
            self.servers.append(server)
            n = n + 1
        self.hardcoded_links()

    @property
    def id(self):
        return self.__id

    def build_topology(self) -> Topology:
        topology = Topology(self.__id, self.links, self.servers, self.switches)
        topology.build()
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
            LOG.debug(to_print.format(src, dst))
            LOG.debug("link id: {}".format(link.int_id))

        print("no of links: {}".format(len(topology.links)))
        print("no of servers: {}".format(len(topology.servers)))
        print("no of switches: {}".format(len(topology.switches)))
        for server in topology.servers:
            print("Server ID: {}, Server Name: {}, int_id: {}".format(server.id, server.name, server.int_id))
            print("In link ID: {}".format(server.in_links.id))
            print("Out link ID: {}".format(server.out_links.id))

        for switch in topology.switches:
            print("Switch ID: {}, int_id: {}".format(switch.id, switch.int_id))
            for port in switch.get_ports():
                print("Port ID: {}, in_link: {}, out_link: {}".format(port.id, port.in_link, port.out_link))
                if port.in_link is not None:
                    print("In link ID: {}".format(port.in_link.id))
                if port.out_link is not None:
                    print("Out link ID: {}".format(port.out_link.id))
        return topology

    def hardcoded_links(self):
        mapped_physical_links: List[ComputeToSwitchLinks] = [ComputeToSwitchLinks(compute="compute01",
                                                                                  switch="switch3", port="11"),
                                                             ComputeToSwitchLinks(compute="compute02",
                                                                                  switch="switch4", port="10"),
                                                             ComputeToSwitchLinks(compute="compute03",
                                                                                  switch="switch3", port="10")]
        for element in mapped_physical_links:
            print(element.compute + " <=> " + element.switch + ":" + element.port)
            self.add_physical_link(element)

        """
        # compute01 <--> switch03[port11]
        links_length = len(self.links)
        self.links.append(Link(_id="compute01-switch03", int_id=links_length,
                               dst_node_id=self.get_node_by_id("openflow:3"),
                               src_node_id=self.get_node_by_id("b755b8b1-363f-40dc-ba6e-8b55dd3a4767"),
                               dst_port_id="openflow:3:11"))
        links_length = links_length + 1
        self.links.append(Link(_id="switch03-compute01", int_id=links_length,
                               dst_node_id=self.get_node_by_id("b755b8b1-363f-40dc-ba6e-8b55dd3a4767"),
                               src_node_id=self.get_node_by_id("openflow:3"),
                               src_port_id="openflow:3:11"))
        # compute02 <--> switch04[port10]
        links_length = links_length + 1
        self.links.append(Link(_id="compute02-switch04", int_id=links_length,
                               dst_node_id=self.get_node_by_id("openflow:4"),
                               src_node_id=self.get_node_by_id("97582edb-4ab7-4190-ab14-243349e43c67"),
                               dst_port_id="openflow:4:10"))
        links_length = links_length + 1
        self.links.append(Link(_id="switch04-compute02", int_id=links_length,
                               dst_node_id=self.get_node_by_id("97582edb-4ab7-4190-ab14-243349e43c67"),
                               src_node_id=self.get_node_by_id("openflow:4"),
                               src_port_id="openflow:4:10"))

        # compute03 <--> switch03[port10]
        links_length = links_length + 1
        self.links.append(Link(_id="compute03-switch03", int_id=links_length,
                               dst_node_id=self.get_node_by_id("openflow:3"),
                               src_node_id=self.get_node_by_id("97582edb-4ab7-4190-ab14-243349e43c67"),
                               dst_port_id="openflow:3:10"))
        links_length = links_length + 1
        self.links.append(Link(_id="switch03-compute03", int_id=links_length,
                               dst_node_id=self.get_node_by_id("97582edb-4ab7-4190-ab14-243349e43c67"),
                               src_node_id=self.get_node_by_id("openflow:3"),
                               src_port_id="openflow:3:10"))
        """

    def add_physical_link(self, element: ComputeToSwitchLinks):
        links_length = len(self.links)
        LOG.debug("links_length: {}".format(links_length))
        id_name = element.compute + "-" + element.switch
        print(f"id_name: {id_name}, dst_node: {self.get_node_by_name(element.switch).name}, src_node: {self.get_node_by_name(element.compute).name}")
        switch = self.get_node_by_name(element.switch)
        switch_id = switch.id
        switch_node_id = switch.int_id
        switch_port_id = switch_id + ":" + element.port
        compute_node_id = self.get_node_by_name(element.compute).int_id
        self.links.append(Link(_id=id_name, int_id=links_length,
                               dst_node_id=switch_node_id,
                               src_node_id=compute_node_id,
                               dst_port_id=switch_port_id))
        links_length = links_length + 1
        id_name = element.switch + "-" + element.compute
        self.links.append(Link(_id=id_name, int_id=links_length,
                               dst_node_id=compute_node_id,
                               src_node_id=switch_node_id,
                               src_port_id=switch_port_id))

    def get_node_by_name(self, node_name) -> Node:
        for switch in self.switches:
            if node_name == switch.name:
                return switch

        for server in self.servers:
            if node_name == server.name:
                return server

    def get_node_by_id(self, node_id) -> int:
        for switch in self.switches:
            if node_id == switch.id:
                return switch.int_id

        for server in self.servers:
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


if __name__ == "__main__":
    main()
