import logging

from odl.openflow import OpenFlow
from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.neutron.neutron_details import Neutron
from openstack_internal.openstack_constants import OpenStackConstants
from openstack_internal.virtual_machine import VirtualMachine
from optimization.optimizer import Optimize
from optimization.topology_builder import TopologyBuilder
from optimization.tosca_builder import TOSCABuilder
from templates.input_request import InputRequest
from topology.topology import Topology
from tosca.tosca_input import TOSCAInput
from tosca.vm_requirement import VMRequirement

LOG = logging.getLogger(__name__)


def get_vm_ip_address(network_ip_dict_list: dict[str, list], network_name: str, vm_requirement: VMRequirement) -> str:
    return network_ip_dict_list[network_name][vm_requirement.int_id]


class ServiceChain:

    def __init__(self, input_request: InputRequest):
        LOG.debug("Creating Topology Builder")
        self.topology: Topology = TopologyBuilder(input_request.name).build_topology()
        LOG.debug("Created  Topology Builder")
        LOG.debug("Creating Tosca Builder")
        self.tosca: TOSCAInput = TOSCABuilder(input_request).build_tosca()
        LOG.debug("Created  Tosca Builder")

    def create_service_chain(self) -> {}:
        provider_network_name = OpenStackConstants.PROVIDER_NETWORK_NAME
        LOG.debug("Creating Optimize object")
        optimize = Optimize(self.topology, self.tosca)
        LOG.debug("Created  Optimize object")
        LOG.debug("Calling  Optimize.optimize()")
        optimize.optimize()
        LOG.debug("Called   Optimize.optimize()")
        neutron = Neutron(AuthenticateConnection().get_connection())
        network_ip_dict_list = {}
        for network_name in OpenStackConstants.NETWORKS_LIST:
            LOG.info(f"Network ID: {neutron.networks_dict[network_name]}, Name: {network_name}")
            print(f"Network ID: {neutron.networks_dict[network_name]}, Name: {network_name}")
            ip_list = neutron.get_available_ip_list(network_name, len(self.tosca.vm_requirements))
            network_ip_dict_list[network_name] = ip_list
        neutron.connection.close()

        for vm_requirement in self.tosca.vm_requirements:
            networks = []
            int_id = vm_requirement.int_id
            print(f"VM int ID: {int_id}, VM name: {vm_requirement.hostname}")
            for network_name in OpenStackConstants.NETWORKS_LIST:
                ip_list = network_ip_dict_list[network_name]
                network_dict = {"net-id": neutron.networks_dict[network_name], "v4-fixed-ip": ip_list[int_id]}
                networks.append(network_dict)
            vm_requirement.networks = networks
            print(f"provider network name: {provider_network_name} \n"
                  f"Provider network ID  : {neutron.networks_dict[provider_network_name]} \n"
                  f"Provider IP of VM: {network_ip_dict_list[provider_network_name][vm_requirement.int_id]}\n"
                  f"get_vm_ip_address:"
                  f" {get_vm_ip_address(network_ip_dict_list, provider_network_name, vm_requirement)}")
            print(f"VM networks: {vm_requirement.networks}")

        of = OpenFlow()
        len_switches = len(self.topology.switches)
        len_compute_servers = len(self.topology.compute_servers)
        for v_link in self.tosca.v_links:
            dst_v_node = self.tosca.vm_requirements_dict[v_link.dst_node_id]
            src_v_node = self.tosca.vm_requirements_dict[v_link.src_node_id]
            for link in v_link.implemented_links:
                if link.src_node_id < len_switches:
                    src_node = self.topology.switches_dict.get(link.src_node_id)
                else:
                    src_node = self.topology.compute_servers_dict.get(link.src_node_id)

                if link.dst_node_id < len_switches:
                    dst_node = self.topology.switches_dict.get(link.dst_node_id)
                else:
                    dst_node = self.topology.compute_servers_dict.get(link.dst_node_id)

                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print(f"Virtual Link Name: {v_link.id}, Physical Link Name: {link.id},"
                      f"src->dst: {src_node.id}->{dst_node.id},\n"
                      f" src_ip: {get_vm_ip_address(network_ip_dict_list, provider_network_name, src_v_node)},\n"
                      f" dst_ip: {get_vm_ip_address(network_ip_dict_list, provider_network_name, dst_v_node)}")
                if src_node.is_switch:
                    of.create_arp_flow(src_node.id, src_node.ports_dict[link.src_port_id].port_number, 1)
                    of.create_traffic_forwarding(src_node.id, src_node.ports_dict[link.src_port_id].port_number,
                                                 get_vm_ip_address(network_ip_dict_list, provider_network_name,
                                                                   src_v_node),
                                                 get_vm_ip_address(network_ip_dict_list, provider_network_name,
                                                                   dst_v_node) + dst_v_node.subnet_mask)
                if dst_node.is_switch:
                    of.create_arp_flow(dst_node.id, dst_node.ports_dict[link.dst_port_id].port_number, 2)
                    of.create_traffic_forwarding(dst_node.id, dst_node.ports_dict[link.dst_port_id].port_number,
                                                 get_vm_ip_address(network_ip_dict_list, provider_network_name,
                                                                   src_v_node) + src_v_node.subnet_mask)

                print("--------------------------------------------------------------------------------------------")

        virtual_machine = VirtualMachine()
        for vm in self.tosca.vm_requirements:
            key_pair = "hanif-kukkalli"
            """
            if "compute01" in vm.hypervisor_hostname:
                key_pair = "compute01"
            elif "compute02" in vm.hypervisor_hostname:
                key_pair = "compute02"
            """

            print("Creating VM: {} on hypervisor: {} with key_pair: {}".format(vm.hostname, vm.hypervisor_hostname,
                                                                               key_pair))
            # networks = [{"net-id": vm.network_id, "v4-fixed-ip": vm.ip_address}]
            server = virtual_machine.create_virtual_machine(vm.hostname, vm.image_id, flavor=vm.flavor,
                                                            security_groups=["default"],
                                                            key_pair=key_pair,
                                                            networks=vm.networks, host=vm.hypervisor_hostname)
            print("Created Server: {}".format(server))
        virtual_machine.close_connection()

        return {"vm-creation": "success"}


def main():
    # topology_builder = TopologyBuilder("hanif")
    # tosca_builder = TOSCABuilder("hanif")
    input_request: InputRequest = InputRequest("KN 1st test", "FOUR_G_LTE_CORE_CASS_DB")
    execute = ServiceChain(input_request)
    execute.create_service_chain()
    exit()


if __name__ == "__main__":
    main()
