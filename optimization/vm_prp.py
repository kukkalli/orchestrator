#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import datetime
import logging
import sys

import numpy as np
import pandas as pd

from gurobipy import tuplelist, GRB, Model, quicksum, Env
from itertools import product

from optimization import vm_prp_io


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
    #           (S3)        (S4)
    #            / \          \
    #          /     \          \
    #        /         \          \
    #      (OS)       (C1)       (C2)

    names = ['OS', 'C_1', 'C_2', 'S_1', 'S_2', 'S_3', 'S_4']
    conn = [('OS', 'S_3'), ('C_1', 'S_3'), ('C_2', 'S_4'), ('S_3', 'S_1'), ('S_3', 'S_2'), ('S_4', 'S_1'),
            ('S_4', 'S_2')]

    nodes = []
    for n in range(len(names)):

        if names[n] in ['C_1', 'C_2']:
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

    #         (VM_1) ---- (VM_2)
    #                      /
    #                     /
    #                    /
    #                   /
    #              (VM_3)

    V = 3
    VMs, vLinks = [], []
    for v in range(V):
        CPU, HDD, RAM = 5, 5, 5
        VMs.append(vm_prp_io.VM(v, f'VM_{v}', CPU, HDD, RAM))

    # conn = [('VM_0', 'VM_1'), ('VM_1', 'VM_2')]
    # vLinks.append(VMPRP_IO.vLink(v, f'VM_{v % V}', v % V, f'VM_{(v + 1) % V}', (v + 1) % V, traffic, delay))

    vLinks.append(vm_prp_io.vLink(1, f'VM_{0}', 0, f'VM_{1}', 1, 5, 20))
    vLinks.append(vm_prp_io.vLink(2, f'VM_{1}', 1, f'VM_{2}', 2, 5, 20))

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
