#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
import numpy as np
import sys
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
from itertools import chain, combinations


# In[2]:


def solve(G):
    trees = []
    S_1 = nx.minimum_spanning_tree(G)
    trees += [network(G, S_1, "MST")]
    if average_pairwise_distance_fast(trees[0]) == 0:
        return S_1
    try:
        start_avgw = min(G.nodes, key=lambda n: G.degree(n, weight='weight') / G.degree(n))
        S_2 = generate_spt(G, start_avgw)
        trees += [network(G, S_2, "ASPT")]
    except ZeroDivisionError:
        pass
    high_degree = sorted(G.degree, key=lambda x: x[1], reverse=True)[0][0]
    S_3 = generate_spt(G, high_degree)
    trees += [network(G, S_3, "DSPT")]
    return min(trees, key=lambda t: average_pairwise_distance_fast(t))


# In[3]:


def generate_spt(G, start):
    sp_dict = nx.single_source_dijkstra(G, start)[1]
    edges = set()
    for path in sp_dict.values():
        for i in range(len(path)-1):
            edges.add((path[i], path[i+1]))
    spt = nx.edge_subgraph(G, edges)
    return spt


# In[4]:


def random_network(G):
    T = nx.Graph()
    if nx.number_of_edges(G) == 0:
        return G
    avg_edge_weight = G.size(weight='weight') / G.size()
    while True:
        for (u, v, w) in G.edges.data('weight'):
            potential_network = T.copy()
            potential_network.add_edge(u, v, weight=w)
            p = min(1, np.exp(-1 * w / avg_edge_weight))
            if np.random.rand() < p:
                try:
                    nx.find_cycle(potential_network, orientation='ignore')
                    continue
                except:
                    pass
                T.add_edge(u, v, weight=w)
            if nx.number_of_nodes(T) != 0 and is_valid_network(G, T):
                print("Random:", average_pairwise_distance_fast(T))  
                return T
    print("Random:", average_pairwise_distance_fast(T))            
    return T


# In[5]:


def network(G, T, name):
    """
    Args:
        G: networkx.Graph
    Returns:
        T: networkx.Graph
    """
    # TODO: your code here!
    current_best = T
    current_apd = average_pairwise_distance_fast(current_best)
    while nx.number_of_nodes(T) > 1:
        flag = False
        leaves = [n for n, d in T.degree() if d == 1]
        for leaf in leaves:
            subtree = T.copy()
            subtree.remove_node(leaf)
            new_apd = average_pairwise_distance_fast(subtree)
            if is_valid_network(G, subtree) and new_apd < current_apd:
                current_best = subtree
                current_apd = new_apd
                flag = True
        T = current_best
        # flag = False => no better tree available
        if not flag:
            print(name + ":", current_apd)
            return T
    print(name + ":", current_apd)
    return T


# In[ ]:




