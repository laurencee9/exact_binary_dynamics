# Dependencies
import sys
import numpy as np
sys.path.append('../src/')
from Solver import Solver
from ResponseFunction import ResponseFunction
import json
import networkx as nx


import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors

"""



"""
def make_colormap(seq):
	"""Return a LinearSegmentedColormap
	seq: a sequence of floats and RGB-tuples. The floats should be increasing
	and in the interval (0,1).
	"""
	seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
	cdict = {'red': [], 'green': [], 'blue': []}
	for i, item in enumerate(seq):
		if isinstance(item, float):
			r1, g1, b1 = seq[i - 1]
			r2, g2, b2 = seq[i + 1]
			cdict['red'].append([item, r1, r2])
			cdict['green'].append([item, g1, g2])
			cdict['blue'].append([item, b1, b2])
	return mcolors.LinearSegmentedColormap('CustomMap', cdict,5000)

def get_activation_probability(Q, N):
	Acti = [0.0]*N
	for key in Q:
		acti = [int(u) for u in list(key)]
		for i,ac in enumerate(acti):
			Acti[i] += ac*Q[key]


	
	return Acti

def get_Q(path):
	fileO = open(path, "r")
	Q = {}
	for line in fileO:
		a = line.split("\t")
		Q[a[0]]=float(a[1])
	return Q


Q = get_Q("large_network_solve.txt")
G = nx.read_edgelist("./edgelists/large_network.txt")
mapping = {}
for node in G:
	mapping[node] = int(node)
G = nx.relabel_nodes(G, mapping)

pos = {
	0 : [0,0],
	1 : [-0.5,0.5],
	2 : [-1.0,0.5],
	3 : [-1.3,0.0],
	4 : [-1.0,-0.5],
	5 : [-0.5,-0.5],
	6 : [0.5,0.0],
	7 : [1.0,0.25],
	8 : [1.0,-0.25],
	9 : [0.25,-0.5],
	10: [0.5,-1.0],
	11: [0.25,-1.4],
	12: [0.0,-1.0]
}


c = mcolors.ColorConverter().to_rgb
rvb = make_colormap([c('#4d74b5'),c('#96bfdb'), 0.2, c('#96bfdb') , c('#e2f3f8'), 0.4, c('#e2f3f8') , c('#fbe18f'), 0.6, c('#fbe18f') , c('#f88d59'), 0.8, c('#f88d59'),  c('#d0151d')])
node_color = get_activation_probability(Q,len(G.node))
fig = plt.figure(figsize=(5,3),frameon=False)


nodes = nx.draw_networkx_nodes(G, pos=pos,width=1, 
							 node_size=700,
							 linewidths=4,
							 edge_color="black",
							 node_color=node_color,
							 with_labels=False,
							 cmap=rvb)


nodes.set_edgecolor('black')
nx.draw_networkx_edges(G,pos=pos,width=4,edge_color="black")


plt.xlim([-1.5,1.2])
plt.ylim([-1.7,0.9])
ax = plt.gca()

# fig.patch.set_visible(False)
ax.axis('off')

# plt.colorbar(nodes)
plt.savefig("./full_graph.pdf", bbox_inches='tight', pad_inches=0.0,dpi=300)

