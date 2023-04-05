"""
Implimentation of Trustrank using pregel framework
"""

from pregel import Vertex, Pregel

from numpy import mat, eye, zeros, ones, linalg
import random
import numpy as np

import matplotlib.pyplot as plt


num_workers = 4                                 # No of threads to assign vertices

""" Vertex class for Trustrank algorithm
    Can add instance varibles and methods according to algorithm
"""
class TrustRankVertex(Vertex):
    def __init__(self,id,value,out_vertices,flag,damping_factor=0.85,iterations=50):
        Vertex.__init__(self,id,value,out_vertices)
        self.num_supersteps = iterations
        self.damping_factor = damping_factor
        self.flag = flag

    def update(self):
        # This routine has a bug when there are Trusts with no outgoing
        # links (never the case for our tests).  This problem can be
        # solved by introducing Aggregators into the Pregel framework,
        # but as an initial demonstration this works fine.

        #print(f"{self.id} Vertex Superstep : {self.superstep}" )
        if self.superstep < self.num_supersteps:
            messages_sum = 0
            dino_sum = 0
            for (vertex,message) in self.incoming_messages:
                #print(vertex.flag)
                if vertex.flag:
                    messages_sum = messages_sum+message
                    dino_sum += 1/len(vertex.out_vertices)
            #self.value = (1-self.dampingFactor) / num_vertices + self.dampingFactor*messages_sum
            if len(self.incoming_messages) > 0 and dino_sum >0:
                self.value = (1-self.damping_factor) + self.damping_factor*(messages_sum/dino_sum)

            outgoing_message = 0
            if len(self.outgoing_messages) > 0:
                outgoing_message = self.value / len(self.out_vertices)
            self.outgoing_messages = [(vertex,outgoing_message) for vertex in self.out_vertices]
        else:
            self.active = False


""" Get the list of graph nodes from file"""
def getNodes(filenm):
    with open(filenm,'r') as file:
        return [int(nd)for nd in file.readlines()]

""" Intialiaze value for each node
    For Trustrank it is same of all nodes : 1 / No of nodes
"""
def intialTrustRank(nodes, bad_nodes_file):
    # create a set of bad nodes
    bad_node = set(getNodes(bad_nodes_file))
    
    #return [1.0/len(nodes) for n in nodes]

    rank = []
    for n in nodes:
        if n in bad_node:
            rank.append(1/len(nodes))
        else:
            rank.append(0)
    return rank

""" Updating out going vertices for each vertex using edges """
def updateOutGoingVertices(vertices,edge_file):
    out_vertces_dict = {}
    with open(edge_file,'r') as file:
        for edge in file.readlines():
            #print(edge)
            frm,to = map(int,edge.strip('\n').split(','))
            for v in vertices:
                for u in vertices:
                    if v.id == frm and u.id == to:
                        v.out_vertices.append(u)

'''def Trustrank_test(vertices):
    """Computes the Trustrank vector associated to vertices, using a
    standard matrix-theoretic approach to computing Trustrank.  This is
    used as a basis for comparison."""
    I = mat(eye(num_vertices))
    G = zeros((num_vertices,num_vertices))
    for vertex in vertices:
        num_out_vertices = len(vertex.out_vertices)
        for out_vertex in vertex.out_vertices:
            G[out_vertex.id,vertex.id] = 1.0/num_out_vertices
    P = (1.0/num_vertices)*mat(ones((num_vertices,1)))
    return 0.15*((I-0.85*G).I)*P'''

""" Compute Trustrank using pregel by assing set of vertices to thread """
def pregelTrustrank(vertices):
    p = Pregel(vertices,num_workers)
    p.run()
    return mat([vertex.value for vertex in p.vertices]).transpose()



def printSorted(mat):
    l = mat.tolist()
    flat_list = []
    for i in l:
        for k in i:
            flat_list.append(k)
    
    flat_list.sort()
    
    #print(len(flat_list))
    x = list(range(len(flat_list)))
    plt.plot(x,flat_list)
    plt.show()

    







nodes_file = "data/nodes_unique.txt"
bad_nodes_file = "data/nodes_unique_bad.txt"
nodes = getNodes(nodes_file)                   # Nodes of graph
num_vertices = len(nodes)
nodes_intial_ranks = intialTrustRank(nodes,bad_nodes_file)     # Intial ranks of nodes in the order of nodes


#Intialize the vertices with modified Vertex class
vertices = []
for i in range(len(nodes)):
    if(nodes_intial_ranks[i] == 0):

        vertices.append(TrustRankVertex(nodes[i],nodes_intial_ranks[i],[],False,0.85,50))
    else:
        vertices.append(TrustRankVertex(nodes[i],nodes_intial_ranks[i],[],True,0.85,50))

#Updating vertex out vertices to send the messages
edge_file="data/edge_unique_reverse_to_propagate_mistrust.txt"
updateOutGoingVertices(vertices,edge_file)

#Trustrank computation
node_ranks = pregelTrustrank(vertices)
'''node_r = []
for e in node_ranks:
    node_r.append(str(e[0]))'''
#node_r.sort()
print("Pregel Trustrank result : \n", node_ranks)
#print(type(node_ranks))
printSorted(node_ranks)
'''
flat_list = []
for sublist in node_ranks:
    for item in sublist:
        flat_list.append(item)
print("Pregel Trustrank result : \n", flat_list)
'''
#Trustrank computation using matrix theory
#node_ranks_ = Trustrank_test(vertices)

#print("Matrix Theory Trustrank result : \n",node_ranks_)
