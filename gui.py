import networkx as nx
import matplotlib.pyplot as plt
class GUI():
    def __init__(self,edge_node):
        self.edges=edge_node

    def topology_graph_without_label(self):
        g=nx.DiGraph()
        for edge in self.edges:
            g.add_edges_from([(edge[0:2][0],edge[0:2][1])],weight=(edge[2:3][0]))
        nx.draw(g)
        plt.show()

    def create_topology_graph(self):
        g = nx.DiGraph()
        for edge in self.edges:
            g.add_node(edge[0:2][0])
            g.add_node(edge[0:2][1])
            g.add_edge((edge[0:2][0]),(edge[0:2][1]),weight=(edge[2:3][0]))
        pos = nx.spring_layout(g)
        return(g ,pos)

    def show_graph(self,g,pos):
        #pos = nx.spring_layout(g) #pos change each time but for fix we can use  pos = nx.planar_layout(g)
        nx.draw(g, pos,with_labels=True,font_size=7)
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
        plt.show()

    def show_graph_shortest_path(self,g,shortest_path_node,pos):

        #the shortest path nodes passed to this function are seperated like(1,2,3)
        #but it should be like this ((1,2)(2,3))
        #the following code makes edgs for shortest path nodes
        shortest_path_edges=[]
        for i in range(len(shortest_path_node)-1):
            shortest_path_edge = []
            shortest_path_edge.append(shortest_path_node[i])
            shortest_path_edge.append(shortest_path_node[i+1])
            shortest_path_edges.append(shortest_path_edge)

        #we make the return of g.edges like a list to do further steps
        list_edge = []
        for item in g.edges:
            list_edge.append(list(item))

        #list_edge is a list made of g.edges
        #it has two way communication for nodes like (5,7) (7,5)
        #one of them is sufficient for drawing graph hence we remove one of them
        #first we make t contratry to item then we remove it from list_edge
        for item in list_edge:
            t = []
            t.append(item[1])
            t.append(item[0])
            if t in list_edge:
                list_edge.remove(t)
        #we need to make a list of edges which are not in shortestpath edges
        #this should be tuple as nx.draw_networkx requires tule
        fix_edges=[]
        for item in list_edge:
            if item not in shortest_path_edges:
                fix_edges.append(tuple(item))

        fix_node = g.nodes - shortest_path_node
        labels = nx.get_edge_attributes(g, 'weight')

        #to print node name we need to make a dic which the key is the name of node and each key has node name
        node_labels = {}
        for node in g.nodes:
            node_labels[node] = node
        #we draw the graph via two approaches
        # one time the nodes and edges which are in shortest path with its own attributes
        #othe one which has the fix nodes and edges with another attributes

        nx.draw_networkx_nodes(g, pos, nodelist=shortest_path_node)
        nx.draw_networkx_edges(g, pos, edgelist=shortest_path_edges,arrows=False ,label=labels,width=8, alpha=0.5, edge_color="r")
        nx.draw_networkx_nodes(g, pos, nodelist=fix_node)
        nx.draw_networkx_edges(g, pos, edgelist=fix_edges,arrows=False,label=labels, edge_color="black")
        nx.draw_networkx_edge_labels(g, pos,edge_labels=labels)
        nx.draw_networkx_labels(g,pos,labels=node_labels,font_size=7)
        plt.show()
