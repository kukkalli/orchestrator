import logging
from typing import List, Dict

from topology.link import Link
from topology.node import Node
from topology.compute_server import ComputeServer
from topology.server import Server
from topology.switch import Switch

LOG = logging.getLogger(__name__)


class Topology:

    def __init__(self, _id: str, links: List[Link], compute_servers: List[ComputeServer], switches: List[Switch],
                 others_servers: List[Server]):
        self.__id = _id
        self.links = links
        self.nodes: List[Node] = []
        self.compute_servers = compute_servers
        self.compute_servers_dict: Dict[int, ComputeServer] = {}
        for compute_server in compute_servers:
            self.compute_servers_dict[compute_server.int_id] = compute_server
            self.nodes.append(compute_server)
        self.switches = switches
        self.switches_dict: Dict[int, Switch] = {}
        for switch in switches:
            self.switches_dict[switch.int_id] = switch
            self.nodes.append(switch)
        self.other_servers = others_servers
        self.other_servers_dict: Dict[int, Server] = {}
        for other_server in others_servers:
            self.other_servers_dict[other_server.int_id] = other_server
            self.nodes.append(other_server)

    @property
    def id(self):
        return self.__id

    def build(self):
        LOG.info(f"Building Network Topology of the data-center network - Started")
        for link in self.links:
            switch_id, port_id = "", ""
            try:
                switch_id = link.dst_node_id
                port_id = link.dst_port_id
                if link.dst_port_id is not None:
                    print(f"link: dst-nid: {link.dst_node_id}, dst-pid: {link.dst_port_id}")
                    self.switches_dict[link.dst_node_id].ports_dict[link.dst_port_id].set_in_link(link)
                elif link.dst_node_id in self.compute_servers_dict:
                    self.compute_servers_dict[link.dst_node_id].add_in_link(link)
                else:
                    self.other_servers_dict[link.dst_node_id].add_in_link(link)
                switch_id = link.src_node_id
                port_id = link.src_port_id
                if link.src_port_id is not None:
                    print(f"link: src-nid: {link.src_node_id}, src-pid: {link.src_port_id}")
                    self.switches_dict[link.src_node_id].ports_dict[link.src_port_id].set_out_link(link)
                elif link.src_node_id in self.compute_servers_dict:
                    self.compute_servers_dict[link.src_node_id].add_out_link(link)
                else:
                    self.other_servers_dict[link.src_node_id].add_out_link(link)
            except RuntimeError:
                LOG.error(f"Invalid switch {switch_id} or switch port {port_id}")
                print(f"Invalid switch {switch_id} or switch port {port_id}")
        LOG.info(f"Building Network Topology of the data-center network - Complete")

    def add_compute_server(self, compute_server: ComputeServer) -> None:
        LOG.debug(f"Added Compute Server: {compute_server.name}")
        self.compute_servers.append(compute_server)

    def add_switch(self, switch: Switch) -> None:
        LOG.debug(f"Added Switch: {switch.name}")
        self.switches.append(switch)

    def add_link(self, link: Link) -> None:
        LOG.debug(f"Added Link: {link.id}")
        self.links.append(link)

    def get_switch_by_int_id(self, int_id: int) -> Switch:
        return self.switches_dict[int_id]
