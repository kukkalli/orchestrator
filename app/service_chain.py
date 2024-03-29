import logging
import time
from datetime import datetime
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
        start_time = time.time()
        print(f"Creating Topology Builder: Start Time: {start_time}")
        self.topology: Topology = TopologyBuilder(input_request.name).build_topology()
        end_time = time.time()
        print(f"Created  Topology Builder: End Time: {end_time}")
        print(f"Topology creation time: {(end_time - start_time)}s")

        start_time = time.time()
        print(f"Creating ToscaInput: Start Time: {start_time}")
        self.tosca: TOSCAInput = TOSCAInput(input_request)
        self.tosca.build()
        end_time = time.time()
        print(f"Created  ToscaInput: End Time: {end_time}")
        print(f"ToscaInput creation time: {(end_time - start_time)}s")
        self.network_ip_dict_list: Dict[str, list] = {}
        self.nf_ip_dict: Dict[str, str] = {}
        self.neutron = None

    def create_service_chain(self) -> {}:
        provider_network_name = OpenStackConstants.PROVIDER_NETWORK_NAME
        start_time = time.time()
        print(f"Creating Optimizer object: Start Time: {start_time}")
        optimizer = Optimizer(self.topology, self.tosca)
        print(f"Created  Optimizer object")
        print(f"Calling  Optimizer.optimize(): Start Time: {time.time()}")
        optimizer.optimize()
        end_time = time.time()
        print(f"Called   Optimizer.optimize(): End Time: {end_time}")
        print(f"Optimizer solution response time: {(end_time - start_time)}s")

        start_time = time.time()
        print(f"Deploying Optimizer solution: Start Time: {start_time}")
        self.create_network_dict()
        self.bind_ip_to_vm(provider_network_name)

        # self.create_vlinks_flows(provider_network_name)

        self.create_vms()

        end_time = time.time()
        print(f"Deploying Optimizer solution: End Time: {end_time}")
        print(f"Deploying Optimizer solution time: {(end_time - start_time)}s")

        return {"vm-creation": "success"}

    def create_network_dict(self):
        self.network_ip_dict_list = {}
        self.neutron = Neutron(AuthenticateConnection().get_connection())
        for network_name in OpenStackConstants.NETWORKS_LIST:
            print(f"Network ID: {self.neutron.networks_dict[network_name]}, Name: {network_name}")
            self.network_ip_dict_list[network_name] = self.neutron.get_available_ip_list(
                network_name, len(self.tosca.vm_requirements))
        self.neutron.connection.close()

    def get_vm_ip_address(self, network_name: str, vm_requirement: VMRequirement) -> str:
        return self.network_ip_dict_list[network_name][vm_requirement.int_id]

    def bind_ip_to_vm(self, provider_network_name: str):
        for vm_requirement in self.tosca.vm_requirements:
            networks = []
            int_id = vm_requirement.int_id
            for network_name in OpenStackConstants.NETWORKS_LIST:
                ip_list = self.network_ip_dict_list[network_name]
                network_dict = {"net-id": self.neutron.networks_dict[network_name], "v4-fixed-ip": ip_list[int_id]}
                networks.append(network_dict)
            vm_requirement.networks = networks
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

                if src_node.is_switch:
                    self.create_flow(src_node, link, provider_network_name, src_v_node, dst_v_node, 1)

                if dst_node.is_switch:
                    self.create_flow(dst_node, link, provider_network_name, src_v_node, dst_v_node, 2)

    def create_flow(self, node, link, provider_network_name, src_v_node, dst_v_node, arp_code):
        of = OpenFlow()
        print(f"Src IP: {self.get_vm_ip_address(provider_network_name, src_v_node)}")
        print(f"Dst IP: {self.get_vm_ip_address(provider_network_name, dst_v_node)}")
        of.create_arp_flow(node.id, node.ports_dict[link.dst_port_id].port_number, arp_code)
        of.json_forwarding_flow_install(node.id, node.ports_dict[link.dst_port_id].port_number,
                                        self.get_vm_ip_address(provider_network_name, src_v_node)
                                        + src_v_node.subnet_mask,
                                        self.get_vm_ip_address(provider_network_name, dst_v_node)
                                        + dst_v_node.subnet_mask)

    def create_vms(self):
        vm_user_data_dict = self.tosca.service_template.populate_user_data(self.nf_ip_dict)
        """
        network_functions = self.tosca.service_template.get_network_functions()
        for network_function in network_functions:
            print(f"network function: name: {network_function.name}, {network_function.vm_name},\n"
                  f" {vm_user_data_dict[network_function.name]}")
        """

        virtual_machine = VirtualMachine()
        print("-----------------------------------------------------------------")
        print("-----------------------------------------------------------------")
        for vm in self.tosca.vm_requirements:
            start_time = time.time()
            LOG.info(f"Starting {vm.hostname} at: {start_time}")
            print(f"Starting {vm.hostname} at: {start_time}")
            date_time = datetime.fromtimestamp(start_time)
            LOG.info(f"Started {vm.hostname} at: {date_time.strftime('%Y-%m-%d, %H:%M:%S.%f')}")
            print(f"Started {vm.hostname} at: {date_time.strftime('%Y-%m-%d, %H:%M:%S.%f')}")
            key_pair = "hanif-kukkalli"

            LOG.debug("Creating VM: {} on hypervisor: {}".format(vm.hostname, vm.hypervisor_hostname))
            print("Creating VM: {} on hypervisor: {}".format(vm.hostname, vm.hypervisor_hostname))
            print(f"Networks:\n{vm.networks}")
            # print(f"userdata:\n{vm_user_data_dict[vm.name]}")
            server = virtual_machine.create_virtual_machine(vm.hostname, vm.image_id, flavor=vm.flavor,
                                                            security_groups=["default"],
                                                            userdata=vm_user_data_dict[vm.name],
                                                            key_pair=key_pair, networks=vm.networks,
                                                            host=vm.hypervisor_hostname)
            LOG.debug(f"Created {vm.name} Server: {server}")
            print(f"Created {vm.name} Server: {server}")
            end_time = time.time()
            date_time = datetime.fromtimestamp(end_time)
            LOG.info(f"Started {vm.hostname} at: {date_time.strftime('%Y-%m-%d, %H:%M:%S.%f')}")
            print(f"Started {vm.hostname} at: {date_time.strftime('%Y-%m-%d, %H:%M:%S.%f')}")
            LOG.info(f"Started {vm.hostname} at: {end_time}")
            print(f"Started {vm.hostname} at: {end_time}")
            LOG.info(f"Creation of {vm.hostname} time: {(end_time - start_time)}s")
            print(f"Creation of {vm.hostname} time: {(end_time - start_time)}s")
            LOG.info("-----------------------------------------------------------------")
            print("-----------------------------------------------------------------")
        virtual_machine.close_connection()


def main():
    input_request: InputRequest = InputRequest("OAI 5G 001 1ms", "OAI_5GCN_DC", max_link_delay=1)
    execute = ServiceChain(input_request)
    execute.create_service_chain()
    exit()


if __name__ == "__main__":
    main()
