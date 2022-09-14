#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import logging
import sys

import numpy as np

from gurobipy import GRB, Model, quicksum, GurobiError

from optimization import vm_prp_io

LOG = logging.getLogger(__name__)


def build_ILP(nodes, edges, VMs, vLinks):
    """
    Builds a MIP model of the VM placement
    and routing problem and returns the model
        """

    # --- Optimisation model ---#

    VMPRP = Model('VM Placement & Routing Problem')

    # --- Cardinality of objects ---#

    N, E = len(nodes), len(edges)
    V, L = len(VMs), len(vLinks)

    # --- Primal variables ---#

    x = {}
    for n in range(N):
        for v in range(V):
            x[v, n] = VMPRP.addVar(0., 1., vtype=GRB.INTEGER, name=f'x_{v}_{n}')

    fI, fO = {}, {}
    for e in range(E):
        for l in range(L):
            fI[l, e] = VMPRP.addVar(0., 1., vtype=GRB.INTEGER, name=f'fI_{l}_{e}')
            fO[l, e] = VMPRP.addVar(0., 1., vtype=GRB.INTEGER, name=f'fO_{l}_{e}')

    mu = VMPRP.addVar(0., 1., vtype=GRB.CONTINUOUS, name=f'mu')

    z = VMPRP.addVar(0., 1., vtype=GRB.INTEGER, name=f'z')

    VMPRP.update()

    # --- Constraints ---#

    for v in range(V):
        VMPRP.addConstr(quicksum(nodes[n].cFlag * x[v, n] for n in range(N)) == z)

    for n in range(N):
        VMPRP.addConstr(quicksum(VMs[v].CPU * x[v, n] for v in range(V)) <= mu * nodes[n].CPU)
        VMPRP.addConstr(quicksum(VMs[v].HDD * x[v, n] for v in range(V)) <= mu * nodes[n].HDD)
        VMPRP.addConstr(quicksum(VMs[v].RAM * x[v, n] for v in range(V)) <= mu * nodes[n].RAM)
        for l in range(L):
            VMPRP.addConstr(quicksum(fI[l, e.ID] - fO[l, e.ID] for e in nodes[n].outEdges)
                            - quicksum(fI[l, e.ID] - fO[l, e.ID] for e in nodes[n].inEdges)
                            == x[vLinks[l].tailID, n] - x[vLinks[l].headID, n])

    for e in range(E):
        VMPRP.addConstr(quicksum(vLinks[l].traffic * (fI[l, e] + fO[l, e]) for l in range(L)) <= mu * edges[e].capacity)

    # --- Optional delay constraints between VM pairs ---#

    for l in range(L):
        VMPRP.addConstr(quicksum(edges[e].delay * (fI[l, e] + fO[l, e]) for e in range(E)) <= vLinks[l].delay)

    # --- Objective function ---#

    VMPRP.setObjective(z - mu, sense=GRB.MAXIMIZE)

    VMPRP.update()
    VMPRP.__data = x, fI, fO, mu, z

    return VMPRP


def main(argv):
    parser = argparse.ArgumentParser(description='VM Placement & Routing Problem')

    #    parser.add_argument('-v', '--VMs',
    #                        type=int,
    #                        action='store',
    #                        dest='VMs',
    #                        default=None,
    #                        required=False,
    #                        help='Flag to indicate number of VMs')

    global args
    args = parser.parse_args()

    # --- Create the physical network infrastructure ---#

    #           (S1)        (S2)
    #             | \      / |
    #             |   \  /   |
    #             |   /  \   |
    #             | /      \ |
    #    (OS)---(S3)        (S4)
    #            / \        / \
    #          /    \      /   \
    #        /       \    |     \
    #      (C3)     (C1) (RRH)  (C2)

    names = ['C_1', 'C_2', 'C_3', 'OS', 'RRH', 'S_1', 'S_2', 'S_3', 'S_4']
    conn = [('OS', 'S_3'), ('C_1', 'S_3'), ('C_2', 'S_4'), ('C_3', 'S_3'), ('RRH', 'S_4'), ('S_3', 'S_1'),
            ('S_3', 'S_2'), ('S_4', 'S_1'), ('S_4', 'S_2')]

    nodes = []
    for n in range(len(names)):

        if names[n] in ['C_1', 'C_2', 'C_3']:
            nodes.append(vm_prp_io.Node(n, names[n], 20, 20, 20, 1))
        else:
            nodes.append(vm_prp_io.Node(n, names[n], 0, 0, 0, 0))

    for n in range(len(names)):
        print(nodes[n].cFlag)

    edges = []
    for e in range(len(conn)):
        tailname, headname = conn[e]
        tailID, headID = names.index(tailname), names.index(headname)
        edges.append(vm_prp_io.Edge(e, tailname, tailID, headname, headID, 20, 3))

        nodes[edges[-1].headID].addInEdge(edges[-1])
        nodes[edges[-1].tailID].addOutEdge(edges[-1])

    # --- Create the virtual network request ---#

    #         (VM_0) ---- (VM_1)
    #                      / \
    #                     /   \
    #                    /     \
    #                   /       \
    #               (VM_2) ---- (VM_3)

    V = 4
    VMs, vLinks = [], []
    for v in range(V):
        CPU, HDD, RAM = 5, 5, 5
        VMs.append(vm_prp_io.VM(v, f'VM_{v}', CPU, HDD, RAM))

    # conn = [('VM_0', 'VM_1'), ('VM_1', 'VM_2')]
    # vLinks.append(VMPRP_IO.vLink(v, f'VM_{v % V}', v % V, f'VM_{(v + 1) % V}', (v + 1) % V, traffic, delay))
    vLinks.append(vm_prp_io.vLink(0, f'VM_{0}', 0, f'VM_{1}', 1, 5, 20))
    vLinks.append(vm_prp_io.vLink(1, f'VM_{1}', 1, f'VM_{2}', 2, 5, 20))
    vLinks.append(vm_prp_io.vLink(2, f'VM_{1}', 1, f'VM_{3}', 3, 5, 20))
    vLinks.append(vm_prp_io.vLink(3, f'VM_{2}', 2, f'VM_{3}', 3, 5, 20))

    """
    vLinks.append(vm_prp_io.vLink(0, f'VM_{0}', 0, f'VM_{1}', 1, 5, 20))
    vLinks.append(vm_prp_io.vLink(1, f'VM_{1}', 1, f'VM_{0}', 0, 5, 20))
    vLinks.append(vm_prp_io.vLink(2, f'VM_{1}', 1, f'VM_{2}', 2, 5, 20))
    vLinks.append(vm_prp_io.vLink(3, f'VM_{2}', 2, f'VM_{1}', 1, 5, 20))
    vLinks.append(vm_prp_io.vLink(4, f'VM_{1}', 1, f'VM_{3}', 3, 5, 20))
    vLinks.append(vm_prp_io.vLink(5, f'VM_{3}', 3, f'VM_{1}', 1, 5, 20))
    vLinks.append(vm_prp_io.vLink(6, f'VM_{2}', 2, f'VM_{3}', 3, 5, 20))
    vLinks.append(vm_prp_io.vLink(7, f'VM_{3}', 3, f'VM_{2}', 2, 5, 20))
    """

    # --- Build the model ---#
    VMPRP = build_ILP(nodes, edges, VMs, vLinks)
    x, fI, fO, mu, z = VMPRP.__data

    # --- Read in the solver parameters ---#
    #    VMPRP.read(args.gurobi)
    #    VMPRP.setParam('LogFile', f'{args.logPath}/gurobi/{fileIO}.log')
    #    VMPRP.update()

    # --- Solve the model ---#
    try:
        #        chronicler.info(f'Solving ... ')
        VMPRP.optimize()

    except GurobiError as e:
        #        chronicler.error(f'Error code {e.errno}: {e}')
        return

    except AttributeError:
        #        chronicler.error(f'Encountered an attribute error')
        return

    # --- Status check ---#

    print(f'Solution status: {VMPRP.status}')
    if VMPRP.solCount < 1:
        #        chronicler.error(f'No solution found, stopping ... ')  # return None, None
        sys.exit()

    # ---Print the model stats ---#

    #    chronicler.info(f'Solution value:	{VMPRP.ObjVal}')
    #    chronicler.info(f'Objective bound:	{VMPRP.ObjBound}')
    #    chronicler.info(f'Relative gap:	{VMPRP.MIPGap}')
    #    chronicler.info(f'Resolution time:	{VMPRP.Runtime}')
    #    chronicler.info(f'Nodes progressed:	{VMPRP.Nodecount}')

    #    class Node:
    #        def __init__(self, ID, name):
    #            self.ID = ID
    #            self.name = name
    #            self.inEdges = []
    #            self.outEdges = []

    #        def __str__(self):
    #            return "Node ID: %4d, Name: " % (self.ID) + self.name

    #        def addInEdge(self, edge):
    #            self.inEdges.append(edge)
    #            self.totalEdgeCapacity += edge.capacity

    #        def addOutEdge(self, edge):
    #            self.outEdges.append(edge)
    #            self.totalEdgeCapacity += edge.capacity

    #    class Compute(Node):
    #        def __init__(self, ID, name, CPU, HDD, RAM):
    #    	super(Compute, self).__init__(ID, name)
    #            self.CPU = CPU
    #    	self.HDD = HDD
    #    	self.RAM = RAM

    #    class Switch(Node):
    #        def __init__(self, ID, name):
    #    	super(Switch, self).__init__(ID, name)

    VMPRP.printAttr('X')
    """
Restricted license - for non-production use only - expires 2023-10-25
Gurobi Optimizer version 9.5.2 build v9.5.2rc0 (linux64)
Thread count: 4 physical cores, 4 logical processors, using up to 4 threads
Optimize a model with 80 rows, 110 columns and 502 nonzeros
Model fingerprint: 0xd186cb59
Variable types: 1 continuous, 109 integer (0 binary)
Coefficient statistics:
  Matrix range     [1e+00, 2e+01]
  Objective range  [1e+00, 1e+00]
  Bounds range     [1e+00, 1e+00]
  RHS range        [2e+01, 2e+01]
Found heuristic solution: objective -0.0000000
Presolve removed 34 rows and 40 columns
Presolve time: 0.00s
Presolved: 46 rows, 70 columns, 286 nonzeros
Variable types: 0 continuous, 70 integer (69 binary)

Root relaxation: objective 6.666667e-01, 20 iterations, 0.00 seconds (0.00 work units)

    Nodes    |    Current Node    |     Objective Bounds      |     Work
 Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time

     0     0    0.66667    0   16   -0.00000    0.66667      -     -    0s
H    0     0                       0.2500000    0.66667   167%     -    0s
H    0     0                       0.5000000    0.66667  33.3%     -    0s
     0     0    0.66667    0   16    0.50000    0.66667  33.3%     -    0s

Explored 1 nodes (50 simplex iterations) in 0.00 seconds (0.00 work units)
Thread count was 4 (of 4 available processors)

Solution count 3: 0.5 0.25 -0 
No other solutions better than 0.5

Optimal solution found (tolerance 1.00e-04)
Best objective 5.000000000000e-01, best bound 5.000000000000e-01, gap 0.0000%
Solution status: 2

    Variable            X 
-------------------------
       x_0_1            1 
       x_1_1            1 
       x_2_2            1 
       x_3_3            1 
      fI_1_1            1 
      fI_2_1            1 
      fO_1_2            1 
      fI_3_2            1 
      fO_2_3            1 
      fO_3_3            1 
      fI_1_6            1 
      fO_3_6            1 
      fO_1_8            1 
      fI_3_8            1 
          mu          0.5 
           z            1 

Process finished with exit code 0

    """
    # --- Access the variables ---#

    N, E = len(nodes), len(edges)
    V, L = len(VMs), len(vLinks)

    xX = np.zeros([V, N], dtype=float)
    for n in range(N):
        for v in range(V):
            xX[v, n] = VMPRP.getVarByName(f'x_{v}_{n}').X

    fFI, fFO = np.zeros([L, E]), np.zeros([L, E])
    for e in range(E):
        for l in range(L):
            fFI = VMPRP.getVarByName(f'fI_{l}_{e}').X
            fFO = VMPRP.getVarByName(f'fO_{l}_{e}').X

    Mu = VMPRP.getVarByName(f'mu').X

    zZ = VMPRP.getVarByName(f'z').X

    # If this (VMPRP.x[v, n].x) doesn't work, we may have to try VMPRP.getVarByName('x_{}_{}'.format(v, n))


if __name__ == '__main__':
    main(sys.argv[1:])
