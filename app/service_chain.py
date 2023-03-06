import logging
import time
from typing import Dict

from odl.openflow import OpenFlow
from openstack_internal.authenticate.authenticate import AuthenticateConnection
from openstack_internal.neutron.neutron_details import Neutron
from openstack_internal.openstack_constants import OpenStackConstants
from openstack_internal.virtual_machine import VirtualMachine
from optimization.optimizer import Optimizer
from optimization.topology_builder import TopologyBuilder
from templates.input_request import InputRequest
from topology.topology import Topology
from tosca.tosca_input import TOSCAInput
from tosca.vm_requirement import VMRequirement

LOG = logging.getLogger(__name__)


class ServiceChain:

    def __init__(self, input_request: InputRequest):
        start_time = time.time_ns()
        LOG.info(f"Creating Topology Builder: Start Time: {start_time}")
        self.topology: Topology = TopologyBuilder(input_request.name).build_topology()
        end_time = time.time_ns()
        LOG.info(f"Created  Topology Builder: End Time: {end_time}")
        LOG.info(f"Topology creation time: {(end_time - start_time)/1000000000}s")

        start_time = time.time_ns()
        LOG.info(f"Creating ToscaInput: Start Time: {start_time}")
        self.tosca: TOSCAInput = TOSCAInput(input_request)
        self.tosca.build()
        end_time = time.time_ns()
        LOG.info(f"Created  ToscaInput: End Time: {end_time}")
        LOG.info(f"ToscaInput creation time: {(end_time - start_time)/1000000000}s")
        self.network_ip_dict_list: Dict[str, list] = {}
        self.nf_ip_dict: Dict[str, str] = {}
        self.neutron = None

    def create_service_chain(self) -> {}:
        provider_network_name = OpenStackConstants.MANAGEMENT_NETWORK_NAME
        start_time = time.time_ns()
        LOG.info(f"Creating Optimizer object: Start Time: {start_time}")
        optimizer = Optimizer(self.topology, self.tosca)
        LOG.info(f"Created  Optimizer object")
        LOG.info(f"Calling  Optimizer.optimize(): Start Time: {time.time_ns()}")
        optimizer.optimize()
        end_time = time.time_ns()
        LOG.info(f"Called   Optimizer.optimize(): End Time: {end_time}")
        LOG.info(f"Optimizer solution response time: {(end_time - start_time)/1000000000}s")

        start_time = time.time_ns()
        LOG.info(f"Deploying Optimizer solution: Start Time: {start_time}")
        self.create_network_dict()
        self.bind_ip_to_vm(provider_network_name)

        # self.create_vlinks_flows(provider_network_name)

        # self.create_vms()

        end_time = time.time_ns()
        LOG.info(f"Deploying Optimizer solution: End Time: {end_time}")
        LOG.info(f"Deploying Optimizer solution time: {(end_time - start_time)/1000000000}s")

        return {"vm-creation": "success"}

    def create_network_dict(self):
        self.network_ip_dict_list = {}
        self.neutron = Neutron(AuthenticateConnection().get_connection())
        for network_name in OpenStackConstants.NETWORKS_LIST:
            LOG.info(f"Network ID: {self.neutron.networks_dict[network_name]}, Name: {network_name}")
            print(f"Network ID: {self.neutron.networks_dict[network_name]}, Name: {network_name}")
            # ip_list = self.neutron.get_available_ip_list(network_name, len(self.tosca.vm_requirements))
            self.network_ip_dict_list[network_name] = self.neutron.get_available_ip_list(
                network_name, len(self.tosca.vm_requirements))
        self.neutron.connection.close()

    def get_vm_ip_address(self, network_name: str, vm_requirement: VMRequirement) -> str:
        return self.network_ip_dict_list[network_name][vm_requirement.int_id]

    def bind_ip_to_vm(self, provider_network_name: str):
        for vm_requirement in self.tosca.vm_requirements:
            networks = []
            int_id = vm_requirement.int_id
            print(f"VM int ID: {int_id}, VM name: {vm_requirement.hostname}")
            for network_name in OpenStackConstants.NETWORKS_LIST:
                ip_list = self.network_ip_dict_list[network_name]
                network_dict = {"net-id": self.neutron.networks_dict[network_name], "v4-fixed-ip": ip_list[int_id]}
                networks.append(network_dict)
            vm_requirement.networks = networks
            print(f"provider network name: {provider_network_name} \n"
                  f"Provider network ID  : {self.neutron.networks_dict[provider_network_name]} \n"
                  f"Provider IP of VM: {self.network_ip_dict_list[provider_network_name][vm_requirement.int_id]}\n"
                  f"get_vm_ip_address:"
                  f" {self.get_vm_ip_address(provider_network_name, vm_requirement)}")
            print(f"VM networks: {vm_requirement.networks}")
            self.nf_ip_dict[vm_requirement.name] = self.get_vm_ip_address(provider_network_name, vm_requirement)

    def create_vlinks_flows(self, provider_network_name: str):
        # of = OpenFlow()
        len_switches = len(self.topology.switches)
        # len_compute_servers = len(self.topology.compute_servers)
        print(f"Number of VLinks: {len(self.tosca.v_links)}")
        for v_link in self.tosca.v_links:
            dst_v_node = self.tosca.vm_requirements_dict[v_link.dst_node_id]
            src_v_node = self.tosca.vm_requirements_dict[v_link.src_node_id]
            print(f"Number of VLinks: {len(v_link.implemented_links)}")
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
                      f" src_ip: {self.get_vm_ip_address(provider_network_name, src_v_node)},\n"
                      f" dst_ip: {self.get_vm_ip_address(provider_network_name, dst_v_node)}")
                if src_node.is_switch:
                    self.create_flow(src_node, link, provider_network_name, src_v_node, dst_v_node, 1)
                    """
                    of.create_arp_flow(src_node.id, src_node.ports_dict[link.src_port_id].port_number, 1)
                    of.json_forwarding_flow_install(src_node.id, src_node.ports_dict[link.src_port_id].port_number,
                                                    self.get_vm_ip_address(provider_network_name, src_v_node)
                                                    + src_v_node.subnet_mask,
                                                    self.get_vm_ip_address(provider_network_name, dst_v_node)
                                                    + dst_v_node.subnet_mask)
                    """

                if dst_node.is_switch:
                    self.create_flow(dst_node, link, provider_network_name, src_v_node, dst_v_node, 2)
                    """
                    of.create_arp_flow(dst_node.id, dst_node.ports_dict[link.dst_port_id].port_number, 2)
                    of.json_forwarding_flow_install(dst_node.id, dst_node.ports_dict[link.dst_port_id].port_number,
                                                    self.get_vm_ip_address(provider_network_name, src_v_node)
                                                    + src_v_node.subnet_mask,
                                                    self.get_vm_ip_address(provider_network_name, dst_v_node)
                                                    + dst_v_node.subnet_mask)
                    """
                print("--------------------------------------------------------------------------------------------")

    def create_flow(self, node, link, provider_network_name, src_v_node, dst_v_node, arp_code):
        # of = OpenFlow()
        print(f"Src IP: {self.get_vm_ip_address(provider_network_name, src_v_node)}")
        print(f"Dst IP: {self.get_vm_ip_address(provider_network_name, dst_v_node)}")
        """
        of.create_arp_flow(node.id, node.ports_dict[link.dst_port_id].port_number, arp_code)
        of.json_forwarding_flow_install(node.id, node.ports_dict[link.dst_port_id].port_number,
                                        self.get_vm_ip_address(provider_network_name, src_v_node)
                                        + src_v_node.subnet_mask,
                                        self.get_vm_ip_address(provider_network_name, dst_v_node)
                                        + dst_v_node.subnet_mask)
        """

    def create_vms(self):
        vm_user_data_dict = self.tosca.service_template.populate_user_data(self.nf_ip_dict)
        """
        network_functions = self.tosca.service_template.get_network_functions()
        for network_function in network_functions:
            print(f"network function: name: {network_function.name}, {network_function.vm_name},\n"
                  f" {vm_user_data_dict[network_function.name]}")
        """

        virtual_machine = VirtualMachine()
        LOG.info("-----------------------------------------------------------------")
        for vm in self.tosca.vm_requirements:
            start_time = time.time_ns()
            LOG.info(f"Starting {vm.hostname} at: {start_time}")
            key_pair = "hanif-kukkalli"

            LOG.debug("Creating VM: {} on hypervisor: {} with key_pair: {}".format(vm.hostname, vm.hypervisor_hostname,
                                                                                   key_pair))
            server = virtual_machine.create_virtual_machine(vm.hostname, vm.image_id, flavor=vm.flavor,
                                                            security_groups=["default"],
                                                            userdata=vm_user_data_dict[vm.name],
                                                            key_pair=key_pair, networks=vm.networks,
                                                            host=vm.hypervisor_hostname)
            print(f"Created {vm.name} Server: {server}")
            end_time = time.time_ns()
            LOG.info(f"Started {vm.hostname} at: {end_time}")
            LOG.info(f"Creation of {vm.hostname} time: {(end_time - start_time) / 1000000000}s")
            LOG.info("-----------------------------------------------------------------")
        virtual_machine.close_connection()


def main():
    # topology_builder = TopologyBuilder("hanif")
    # tosca_builder = TOSCABuilder("hanif")
    input_request: InputRequest = InputRequest("KN-Core", "FOUR_G_VM_LTE_CORE", max_link_delay=0.5)
    execute = ServiceChain(input_request)
    execute.create_service_chain()
    exit()


if __name__ == "__main__":
    main()
