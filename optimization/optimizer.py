import chronicler as chronicler
from gurobipy import GRB, Model, quicksum, GurobiError
from topology.topology import Topology
from tosca.tosca_input import TOSCAInput
import sys
import numpy as np


class Optimize:

    def __init__(self, topology: Topology, tosca: TOSCAInput):
        self.topology = topology
        self.links = topology.links
        self.nodes = topology.nodes
        self.servers = topology.servers
        self.switches = topology.switches
        self.vm_requirements = tosca.vm_requirements
        self.v_links = tosca.v_links
        self.problem_statement: Model = Model('Virtual Machine Placement & Routing Problem')

    def build(self):

        len_nodes, len_links = len(self.nodes), len(self.links)
        len_switches, len_servers = len(self.switches), len(self.servers)
        len_vms, len_v_links = len(self.vm_requirements), len(self.v_links)

        # --- Primal variables ---#
        vm_placement = {}  # virtual machine placement variable

        for n in range(len_servers):
            for v in range(len_vms):
                vm_placement[v, n] = self.problem_statement.addVar(0., 1., vtype=GRB.INTEGER, name=f'x_{v}_{n}')

        flow = {}  # directed flow

        for ll in range(len_links):
            for lvl in range(len_v_links):
                flow[lvl, ll] = self.problem_statement.addVar(0., 1., vtype=GRB.INTEGER, name=f'flow_{lvl}_{ll}')

        mu = self.problem_statement.addVar(0., 1., vtype=GRB.CONTINUOUS, name=f'mu')  # min max utilization
        request_status = self.problem_statement.addVar(0., 1., vtype=GRB.INTEGER, name=f'z')  # request accepted or not

        self.problem_statement.update()

        # --- Constraints ---#
        for v in range(len_vms):
            self.problem_statement.addConstr(quicksum(vm_placement[v, n] for n in range(len_servers)) == request_status)

        rho = 1.0  # parameter to balance utilization between nodes and edges
        for n in range(len_servers):
            self.problem_statement.addConstr(
                quicksum(self.vm_requirements[v].flavor.vcpus * vm_placement[v, n] for v in range(len_vms)) <= rho
                * mu * self.servers[n].cpu)
            self.problem_statement.addConstr(
                quicksum(self.vm_requirements[v].flavor.disk * vm_placement[v, n] for v in range(len_vms)) <= rho
                * mu * self.servers[n].hdd)
            self.problem_statement.addConstr(
                quicksum(self.vm_requirements[v].flavor.ram * vm_placement[v, n] for v in range(len_vms)) <= rho
                * mu * self.servers[n].ram)
            self.add_server_flow_constraint(vm_placement, n, len_v_links, flow)

        for n in range(len_switches):
            self.add_switch_flow_constraint(n, len_v_links, flow)

        vau = 1.0
        for e in range(len_links):  # capacity constraint on link
            self.problem_statement.addConstr(
                quicksum(self.v_links[index].bandwidth * (flow[index, e]) for index in
                         range(len_v_links)) <= vau * mu * self.links[e].capacity)

        # --- Optional delay constraints between VM pairs ---#
        for count in range(len_v_links):  # delay constraint
            self.problem_statement.addConstr(
                quicksum(self.links[e].delay * (flow[count, e]) for e in
                         range(len_links)) <= self.v_links[count].max_link_delay)

        # --- Objective function ---#
        self.problem_statement.setObjective(request_status - mu, sense=GRB.MAXIMIZE)

        self.problem_statement.update()
        self.problem_statement.__data = vm_placement, flow, mu, request_status

    def add_server_flow_constraint(self, vm_placement, element, length, flow):
        serv = self.servers[element]
        for count in range(length):
            self.problem_statement.addConstr(
                flow[count, serv.out_links.int_id] - flow[count, serv.in_links.int_id]
                == vm_placement[self.v_links[count].src_node_id, element] - vm_placement[
                    self.v_links[count].dst_node_id, element])

    def add_switch_flow_constraint(self, element, length, flow):
        for index in range(length):
            s = self.switches[element]
            self.problem_statement.addConstr(
                quicksum(flow[index, p.out_link.int_id] for p in s.get_ports())
                - quicksum(flow[index, p.in_link.int_id] for p in s.get_ports()) == 0)

    def add_variables(self, problem_statement: Model):
        pass

    def add_constraint(self):
        pass

    def optimize(self):
        self.build()
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
        # --- Status check ---#
        print(f'Solution status: {self.problem_statement.status}')
        if self.problem_statement.solCount < 1:
            #        chronicler.error(f'No solution found, stopping ... ')  # return None, None
            sys.exit()

        # ---Print the model stats ---#
        self.problem_statement.printAttr('X')
        """
            Variable            X 
        -------------------------
               x_0_0            1 
               x_1_0            1 
               x_2_1            1 
            flow_3_0            1 
            flow_2_2            1 
            flow_2_5            1 
            flow_3_6            1 
            flow_2_8            1 
            flow_3_9            1 
           flow_3_10            1 
           flow_2_11            1 
                  mu     0.131291 
                   z            1 
        """

        len_nodes, len_links = len(self.nodes), len(self.links)
        len_switches, len_servers = len(self.switches), len(self.servers)
        len_vms, len_v_links = len(self.vm_requirements), len(self.v_links)

        z_output = self.problem_statement.getVarByName(f'z').X
        # print("z_output: {}".format(z_output))

        vm_mapping = np.zeros([len_vms, len_nodes], dtype=float)
        for n in range(len_servers):
            for v in range(len_vms):
                vm_mapping[v, n] = self.problem_statement.getVarByName(f'x_{v}_{n}').X
                if self.problem_statement.getVarByName(f'x_{v}_{n}').X == 1:
                    # print("Printing x_{}_{}:{}".format(v, n, vm_mapping[v, n]))
                    self.vm_requirements[v].hypervisor_hostname = self.servers[n].name
                    # print("VM Name: {}, Server Name: {}".format(self.vm_requirements[v].
                    #                                             hostname, self.servers[n].name))

        flow_mapping = np.zeros([len_v_links, len_links])
        dict_switches = self.topology.switches_dict
        dict_servers = self.topology.servers_dict
        for count in range(len_v_links):
            for e in range(len_links):
                flow_mapping = self.problem_statement.getVarByName(f'flow_{count}_{e}').X
                if self.problem_statement.getVarByName(f'flow_{count}_{e}').X == 1:
                    # print("Printing x_{}_{}:{}".format(count, e, vm_mapping[v, n]))
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
