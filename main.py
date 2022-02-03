from odl.odl_helper import ODLHelperFunctions
# from graph import Graph
# from optimization import topology_builder
from odl.openflow import OpenFlow
# from requests.auth import HTTPBasicAuth

flow = OpenFlow()
# body = flow.flow_attr(0, 1, 11, 76)
flow_list = [[[0, 1, 76, 77], [0, 2, 77, 76]], [[0, 1, 11, 76], [0, 2, 76, 11]], [[0, 1, 77, 10], [0, 2, 10, 77]]]
topo = ODLHelperFunctions()
switches = topo.get_topology_switches()
sw_list = []
for sw in switches:
    sw_list.append(sw.id)
sw_list.remove('openflow:1')

for i, item in enumerate(flow_list):
    # print(flow.put_flow_url_creator(sw_list[i],0,1))
    # print(flow.flow_attr(*item[0]))
    # print(flow.http_put_request_xml((flow.put_flow_url_creator(sw_list[i], 0, 1)), (flow.flow_attr(*item[0]))))
    # print(flow.put_flow_url_creator(sw_list[i],0,2))
    # print(flow.http_put_request_xml((flow.put_flow_url_creator(sw_list[i], 0, 2)), (flow.flow_attr(*item[1]))))
    # print(flow.flow_attr(*item[1]))
    pass

# url = 'http://10.10.0.10:8181/restconf/operational/network-topology:network-topology' #main addresses
# url='http://10.10.0.10:8181/restconf/operational/network-topology:network-topology/topology/flow:1'
# url='http://10.10.0.10:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:3/node-connector/openflow:3:10'
# url= 'http://10.10.0.10:8181/restconf/operations/path-computation:get-constrained-path'
# p=ODLHelper()
# graph=Graph()
#
# topo= ODLHelper()
# switches= topo.get_topology_switches()
# print(topo.get_node_by_id('openflow:2'))
# for sw in switches:
#      print(sw.get_ports()[0])


# print(p.topology_node_port('openflow:1985587783700'))
# print(p.get_topology_switches())
# print(p.get_topology_links())

# print('Show Switch Ports: ',p.topology_node_port('openflow:3'))
# print('------------------------------')
# print('show port detail stat:')
# p.show_node_port_stat('openflow:3','76')
# print(p.topology_list())
# print(p.topology_link())
'''
#pars json and return node list
edges=p.topology_link()



#create edges with random values between 1 and 10(as cost)
for item in range(len(edges)):
    edges[item].append((random.randint(1,10)))
for edge in edges:
    graph.add_edge(*edge)


#define GUI object based on edges
gui=GUI(edges)

#fucntion return g as info about nodes/edges in graph and position of each node for draw
g,pos=gui.create_topology_graph()

# show original topology with node and edge label
gui.show_graph(g,pos)

#take src and dst node from input
path_nodes=[]
path_nodes.extend([item for item in input("Enter the source and destination  nodes: ").split()])
src_node='openflow:'+path_nodes[0]
dst_node='openflow:'+path_nodes[1]
result=graph.dijkstra(src_node,dst_node)

gui.show_graph_shortest_path(g,result,pos)

'''
