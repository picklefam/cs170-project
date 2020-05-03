#!/usr/bin/env python
# coding: utf-8

# In[28]:


import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
import sys
from itertools import chain, combinations


# In[24]:


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        T: networkx.Graph
    """
    # TODO: your code here!
    T = nx.minimum_spanning_tree(G)
    apd = average_pairwise_distance_fast(T)
    while not T.is_empty():
        flag = False
        leaves = [n for n, d in T.degree() if d == 1]
        for leaf in leaves:
            subtree = T.copy()
            subtree.remove_node(leaf)
            new_apd = average_pairwise_distance_fast(subtree)
            if is_valid_network(subtree) and new_apd < apd:
                T = subtree
                apd = new_apd
                flag = True
        # flag = False => no better tree available
    if not flag:
        return T


# In[25]:


# def powerset(iterable):
#     "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
#     s = list(iterable)
#     return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


# Here's an example of how to run your solver.
# Usage: python3 solver.py test.in

# In[10]:


if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    T = solve(G)
    assert is_valid_network(G, T)
    print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
    write_output_file(T, 'out/test.out')

