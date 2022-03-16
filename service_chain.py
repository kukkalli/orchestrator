import logging

from odl.openflow import OpenFlow
from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.virtual_machine import VirtualMachine
from optimization.optimizer import Optimize
from optimization.topology_builder import TopologyBuilder
from optimization.tosca_builder import TOSCABuilder
from templates.input_request import InputRequest
from templates.serviceprofiles import ServiceProfiles
from topology.topology import Topology
from tosca.tosca_input import TOSCAInput


class ServiceChain:

    def __init__(self, input_request: InputRequest):

        self.topology: Topology = TopologyBuilder(input_request.name).build_topology()
        self.tosca: TOSCAInput = TOSCABuilder(input_request).build_tosca()
        # self.tosca: TOSCAInput = tosca

    def create_service_chain(self) -> {}:
        _optimize = Optimize(self.topology, self.tosca)
        _optimize.optimize()
        """
        virtual_machine = VirtualMachine()

        of = OpenFlow()
        len_switches = len(self.topology.switches)
        # len_servers = len(self.topology.servers)

        for v_link in self.tosca.v_links:
            dst_v_node = self.tosca.vm_requirements_dict[v_link.dst_node_id]
            src_v_node = self.tosca.vm_requirements_dict[v_link.src_node_id]
            for link in v_link.implemented_links:
                if link.src_node_id < len_switches:
                    src_node = self.topology.switches_dict.get(link.src_node_id)
                else:
                    src_node = self.topology.servers_dict.get(link.src_node_id)

                if link.dst_node_id < len_switches:
                    dst_node = self.topology.switches_dict.get(link.dst_node_id)
                else:
                    dst_node = self.topology.servers_dict.get(link.dst_node_id)

                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print("Virtual Link Name: {}, Physical Link Name: {} : src->dst: {}->{}, src_ip: {}, dst_ip: {}".
                      format(v_link.id, link.id, src_node.id, dst_node.id, src_v_node.ip_address,
                             dst_v_node.ip_address))
                if src_node.is_switch:
                    of.create_arp_flow(src_node.id, src_node.ports_dict[link.src_port_id].port_number, 1)
                    of.create_traffic_forwarding(src_node.id, src_node.ports_dict[link.src_port_id].port_number,
                                                 src_v_node.ip_address, dst_v_node.ip_address + dst_v_node.subnet_mask)
                if dst_node.is_switch:
                    of.create_arp_flow(dst_node.id, dst_node.ports_dict[link.dst_port_id].port_number, 2)
                    of.create_traffic_forwarding(dst_node.id, dst_node.ports_dict[link.dst_port_id].port_number,
                                                 src_v_node.ip_address + src_v_node.subnet_mask)

                print("--------------------------------------------------------------------------------------------")

        for vm in self.tosca.vm_requirements:
            key_pair = "compute01"
            if "compute01" in vm.hypervisor_hostname:
                key_pair = "compute01"
            elif "compute02" in vm.hypervisor_hostname:
                key_pair = "compute02"

            print("Creating VM: {} on hypervisor: {} with key_pair: {}".format(vm.hostname, vm.hypervisor_hostname,
                                                                               key_pair))
            networks = [{"net-id": vm.network_id, "v4-fixed-ip": vm.ip_address}]
            server = virtual_machine.create_virtual_machine(vm.hostname, vm.image_id, flavor=vm.flavor.id,
                                                            security_groups=["default"],
                                                            key_pair=key_pair,
                                                            networks=networks, host=vm.hypervisor_hostname)
            print("Created Server: {}".format(server))

        virtual_machine.close_connection()
        """
        return {"vm-creation": "success"}


def main():
    # topology_builder = TopologyBuilder("hanif")
    # tosca_builder = TOSCABuilder("hanif")
    input_request: InputRequest = InputRequest("kn", "FOUR_G_LTE_CORE")
    execute = ServiceChain(input_request)
    # execute.create_service_chain()
    exit()


if __name__ == "__main__":
    main()
