'''
SI model
This is a simple version used as the baseline for comparing the
performance of a Pandas implementation.

Modified from tnes.py by SV.
'''

import networkx as nx
import random from random
import argparse
import os
import numpy as np

##############################################
def init_states(G):
    #Setting the initial states of all nodes to susceptible, and time of infection to -1
    for v in G.nodes():
        G.node[v]['state'] = 'S'
        G.node[v]['time'] = -1

    #Setting node 0's state to Infected at time 0
    G.node['Spain']['state']='I'
    G.node['Spain']['time'] = 0
    return G

#############################################
def model_SI(G,k):
    #Implements one step of the SI process
    to_infect = []
    for v in G.nodes():
        if G.node[v]['state'] == 'I': #Nothing to do if node 'v' is already infected
            continue
        for u in G.predecessors(v):  #All in neighbors of node 'v'
            prob = random()
            if G.node[u]['state']=='I' and prob <= G.edge[u][v]['weight']: #If in-neighbor is infected, and edge flips to be true
                to_infect.append(v)
                continue
    for v in list(set(to_infect)):
        #Setting the newly infected node states and infection time
        G.node[v]['state']='I'
        G.node[v]['time'] = k
    return


if __name__ == "__main__":

    ap = argparse.ArgumentParser(description='Discrete time SI model simulator')
    ap.add_argument('network', help='Path to the network file')
    ap.add_argument('iterations', type=int,help='Number of replicates of the epidemic to be generated')
    ap.add_argument('time_steps', type=int,help='Number of timesteps per epidemic')
    ap.add_argument('-o','--output', help='Output file', default="sim_out.csv")
    args = parse_args()

    iterations = args.iterations
    T = args.time_steps

    G = nx.read_edgelist(network,create_using=nx.DiGraph())

    with open(args.output, 'wb') as f:
        for count in range(iterations):
            G = init_states(G)
            for t in range(T):
                model_SI(G,k)
            reports = []
            for v in G.nodes():
                if G.node[v]['time']==-1:
                    continue
                reports.append((v, G.node[v]['time']))

            reports.sort(key=lambda x: x[1])
            for i in range(len(reports)):
                f.write("{} {}\n".format(reports[i][0], reports[i][1]))

