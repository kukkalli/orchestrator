import logging
import time
from typing import Dict

import chronicler as chronicler
from gurobipy import GRB, Model, quicksum, GurobiError

from openstack_internal.nova.flavor import Flavor
from topology.topology import Topology
from tosca.tosca_input import TOSCAInput
import sys
import numpy as np

LOG = logging.getLogger(__name__)


class Optimizer:

    def __init__(self, topology: Topology, tosca: TOSCAInput):
        self.topology = topology
        self.links = topology.links
        self.nodes = topology.nodes
        self.compute_servers = topology.compute_servers
        self.switches = topology.switches
        self.vm_requirements = tosca.vm_requirements
        self.v_links = tosca.v_links
        self.problem_statement: Model = Model('Virtual Machine Placement & Routing Problem')
        self.flavor_id_map: Dict[str, Flavor] = tosca.service_template.flavor_id_map

    def build(self):
        LOG.info("In Optimize.build")

        len_nodes, len_links = len(self.nodes), len(self.links)
        len_switches, len_compute_servers = len(self.switches), len(self.compute_servers)
        len_vms, len_v_links = len(self.vm_requirements), len(self.v_links)

        # --- Primal variables ---#
        vm_placement = {}  # virtual machine placement variable

        for v in range(len_vms):
            for nth_element in range(len_compute_servers):
                vm_placement[v, nth_element] = self.problem_statement.addVar(
                    0., 1., vtype=GRB.INTEGER, name=f'x_{v}_{nth_element}')

        flow = {}  # directed flow

        for lvl in range(len_v_links):
            for ll in range(len_links):
                flow[lvl, ll] = self.problem_statement.addVar(0., 1., vtype=GRB.INTEGER, name=f'flow_{lvl}_{ll}')

        mu = self.problem_statement.addVar(0., 1., vtype=GRB.CONTINUOUS, name=f'mu')  # min max utilization
        request_status = self.problem_statement.addVar(0., 1., vtype=GRB.INTEGER, name=f'z')  # request accepted or not

        LOG.info(f"Update problem statement: min max utilization: {mu}")
        self.problem_statement.update()

        # --- Constraints ---#
        LOG.info(f"Adding constraints about VMs")
        for v in range(len_vms):
            self.problem_statement.addConstr(
                quicksum(vm_placement[v, n] for n in range(len_compute_servers)) == request_status)

        rho = 1.0  # parameter to balance utilization between nodes and edges
        for nth_element in range(len_compute_servers):
            flavor = self.flavor_id_map[self.vm_requirements[nth_element].flavor]
            self.problem_statement.addConstr(
                quicksum(flavor.vcpus * vm_placement[v, nth_element] for v in range(len_vms)) <= rho * mu
                * self.compute_servers[nth_element].cpu)
            self.problem_statement.addConstr(
                quicksum(flavor.disk * vm_placement[v, nth_element] for v in range(len_vms)) <= rho * mu
                * self.compute_servers[nth_element].hdd)
            self.problem_statement.addConstr(
                quicksum(flavor.ram * vm_placement[v, nth_element] for v in range(len_vms)) <= rho * mu
                * self.compute_servers[nth_element].ram)
            self.add_server_flow_constraint(vm_placement, nth_element, len_v_links, flow)

        for nth_element in range(len_switches):
            self.add_switch_flow_constraint(nth_element, len_v_links, flow)

        vau = 0.75
        for e in range(len_links):  # capacity constraint on link
            self.problem_statement.addConstr(
                quicksum(self.v_links[index].bandwidth * (flow[index, e]) for index in
                         range(len_v_links)) <= vau * mu * self.links[e].capacity)

        # --- Optional delay constraints between VM pairs ---#
        for count in range(len_v_links):  # delay constraint
            self.problem_statement.addConstr(
                quicksum(self.links[e].delay * (flow[count, e]) for e in
                         range(len_links)) <= self.v_links[count].max_link_delay)
            """
            for e in range(len_links):
                print("===============================================================================================")
                print(f"links.delay:{self.links[e].delay}, vLinks.max_link_delay: {self.v_links[count].max_link_delay}")
            """

        # --- Objective function ---#
        self.problem_statement.setObjective(request_status - mu, sense=GRB.MAXIMIZE)

        self.problem_statement.update()
        self.problem_statement.__data = vm_placement, flow, mu, request_status

    def add_server_flow_constraint(self, vm_placement, nth_element, len_v_links, flow):
        compute_server = self.compute_servers[nth_element]
        for count in range(len_v_links):
            self.problem_statement.addConstr(
                flow[count, compute_server.out_links.int_id] - flow[count, compute_server.in_links.int_id]
                == vm_placement[self.v_links[count].src_node_id, nth_element] - vm_placement[
                    self.v_links[count].dst_node_id, nth_element])

    def add_switch_flow_constraint(self, element, length, flow):
        for index in range(length):
            s = self.switches[element]
            self.problem_statement.addConstr(
                quicksum(flow[index, p.out_link.int_id] for p in s.get_ports())
                - quicksum(flow[index, p.in_link.int_id] for p in s.get_ports()) == 0)
            """
            for p in s.get_ports():
                LOG.debug("----------------------------------------------------")
                LOG.debug(f"s  id: {s.id}. name: {s.name}, int_id: {s.int_id}, port no: {p.port_number}")
                print("----------------------------------------------------")
                print(f"s  id: {s.id}. name: {s.name}, int_id: {s.int_id}, port no: {p.port_number}")
                print(f"p out: {p.out_link}")
                print(f"p  in: {p.in_link}")
                print(f"p out id: {p.out_link.int_id}")
                print(f"p  in id: {p.in_link.int_id}")
                LOG.debug(f"p out: {p.out_link.int_id}")
                LOG.debug(f"p  in: {p.in_link.int_id}")
            """

    def add_variables(self, problem_statement: Model):
        pass

    def add_constraint(self):
        pass

    def optimize(self):
        LOG.info(f"In Optimize.optimize going to build: Start Time: {time.time_ns()}")
        self.build()
        LOG.info(f"In Optimize.optimize build complete: End Time: {time.time_ns()}")
        LOG.info(f"In Optimize.optimize solve the model: Start Time: {time.time_ns()}")
        # --- Solve the model ---#
        try:
            #        chronicler.info(f'Solving ... ')
            self.problem_statement.optimize()
        except GurobiError as e:
            chronicler.error(f'Error code {e.errno}: {e}')
            return
        except AttributeError:
            chronicler.error(f'Encountered an attribute error')
            return
        LOG.info(f"In Optimize.optimize model solved: End Time: {time.time_ns()}")
        # --- Status check ---#
        print(f'Solution status: {self.problem_statement.status}')
        LOG.info(f'Solution status: {self.problem_statement.status}')
        if self.problem_statement.solCount < 1:
            #        chronicler.error(f'No solution found, stopping ... ')  # return None, None
            sys.exit()

        # ---Print the model stats ---#
        self.problem_statement.printAttr('X')

        len_nodes, len_links = len(self.nodes), len(self.links)
        len_switches, len_compute_servers = len(self.switches), len(self.compute_servers)
        len_vms, len_v_links = len(self.vm_requirements), len(self.v_links)

        z_output = self.problem_statement.getVarByName(f'z').X
        LOG.info("z_output: {}".format(z_output))
        print("z_output: {}".format(z_output))
        # for v in self.problem_statement.getVars():
        #     print('%s %g' % (v.VarName, v.X))
        # print('Obj: %g' % self.problem_statement.ObjVal)

        vm_mapping = np.zeros([len_vms, len_compute_servers], dtype=float)
        for n in range(len_compute_servers):
            for v in range(len_vms):
                vm_mapping[v, n] = self.problem_statement.getVarByName(f'x_{v}_{n}').X
                if self.problem_statement.getVarByName(f'x_{v}_{n}').X == 1:
                    print("Printing x_{}_{}:{}".format(v, n, vm_mapping[v, n]))
                    self.vm_requirements[v].hypervisor_hostname = self.compute_servers[n].hostname
                    print("VM Name: {}, Server Name: {}".format(self.vm_requirements[v].
                                                                hostname, self.compute_servers[n].name))

        flow_mapping = np.zeros([len_v_links, len_links])
        dict_switches = self.topology.switches_dict
        dict_servers = self.topology.compute_servers_dict
        for count in range(len_v_links):
            for e in range(len_links):
                flow_mapping = self.problem_statement.getVarByName(f'flow_{count}_{e}').X
                if self.problem_statement.getVarByName(f'flow_{count}_{e}').X == 1:
                    print("Printing x_{}_{}:{}".format(count, e, vm_mapping[v, n]))
                    self.v_links[count].implemented_links.append(self.links[e])

                    """
                    src_id, dst_id = "", ""
                    if self.links[e].src_node_id < len_switches:
                        src_id = dict_switches.get(self.links[e].src_node_id)
                    else:
                        src_id = dict_servers.get(self.links[e].src_node_id)

                    if self.links[e].dst_node_id < len_switches:
                        dst_id = dict_switches.get(self.links[e].dst_node_id)
                    else:
                        dst_id = dict_servers.get(self.links[e].dst_node_id)
                    print("Virtual Link Name: {}, Physical Link Name: {} : src->dst: {}->{}".
                          format(self.v_links[count].id, self.links[e].id, src_id.id, dst_id.id))
                    """

        mu_result = self.problem_statement.getVarByName(f'mu').X
        print(f"mu result: {mu_result}")
