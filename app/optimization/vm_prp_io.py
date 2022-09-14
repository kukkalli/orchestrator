#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)


class Node:
    def __init__(self, ID, name, CPU, HDD, RAM, cFlag):
        self.ID = ID
        self.name = name
        self.CPU = CPU
        self.HDD = HDD
        self.RAM = RAM
        self.cFlag = cFlag
        self.inEdges = []
        self.outEdges = []

    def addInEdge(self, edge):
        self.inEdges.append(edge)

    def addOutEdge(self, edge):
        self.outEdges.append(edge)


class Edge:
    def __init__(self, ID, tailname, tailID, headname, headID, capacity, delay):
        self.ID = ID
        self.tailname = tailname
        self.tailID = tailID
        self.headname = headname
        self.headID = headID
        self.capacity = capacity
        self.delay = delay


class Network:
    def __init__(self, ID, nodes, edges):
        self.ID = ID
        self.nodes = nodes
        self.edges = edges

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)
        self.nodes[edge.headID].addInEdge(edge)
        self.nodes[edge.tailID].addOutEdge(edge)


class Request:
    def __init__(self, ID, delay, VMs, vLinks):
        self.ID = ID
        self.delay = delay
        self.VMs = VMs
        self.vLinks = vLinks

    def addVM(self, VM):
        self.VMs.append(VM)

    def addvLink(self, vLink):
        self.vLinks.append(vLink)


class VM:
    def __init__(self, ID, name, CPU, HDD, RAM):
        self.ID = ID
        self.name = name
        self.CPU = CPU
        self.HDD = HDD
        self.RAM = RAM


class vLink:
    def __init__(self, ID, tailname, tailID, headname, headID, traffic, delay):
        self.ID = ID
        self.tailname = tailname
        self.tailID = tailID
        self.headname = headname
        self.headID = headID
        self.traffic = traffic
        self.delay = delay
