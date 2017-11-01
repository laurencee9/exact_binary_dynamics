# Dependencies
import sys
import numpy as np
sys.path.append('../src/')
from Solver import Solver
from ResponseFunction import ResponseFunction
import json
import networkx as nx

def write_Q(output_path, Q):
	"""
		Write in a file the probabilities.

		Params
		-------------------------
		output_path [String]
		Q [dict]: Dictionnary where key is configuration and value is a float.
	"""
	with open(output_path, 'w') as outfile:
		for key in Q:
			if Q[key]>1e-18:
				outfile.write(key+"\t"+str(Q[key])+"\n")
	return

def plot_probability_of_activation(G, pos, Q):
	import matplotlib.pyplot as plt
	from matplotlib.colors import LinearSegmentedColormap
	import matplotlib.colors as mcolors

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




	c = mcolors.ColorConverter().to_rgb
	rvb = make_colormap([c('#4d74b5'),c('#96bfdb'), 0.2, c('#96bfdb') , c('#e2f3f8'), 0.4, c('#e2f3f8') , c('#fbe18f'), 0.6, c('#fbe18f') , c('#f88d59'), 0.8, c('#f88d59'),  c('#d0151d')])
	node_color = get_activation_probability(Q,len(G.node))



	fig = plt.figure(figsize=(5,3),frameon=False)
	
	nodes = nx.draw_networkx_nodes(G,pos=pos,width=1, node_size=1200, linewidths=4, edge_color="black",node_color=node_color,with_labels=False,cmap=rvb)
	nodes.set_edgecolor('black')
	nx.draw_networkx_edges(G,pos=pos,width=4,edge_color="black")


	plt.xlim([-0.3,3])
	plt.ylim([-0.3,1.2])
	ax = plt.gca()

	ax.axis('off')
	plt.savefig("./test.png")
	plt.colorbar(nodes)
	plt.savefig("./test_withcolorbar.png", bbox_inches='tight', pad_inches=0.1,dpi=200)
	# plt.savefig("./plot/network_activation_3.pdf")
	# plt.show()

	return



params = {
	"edgelist_path" : "./edgelists/large_network.txt",
	"response_function": [
		{	
			"name": "bond",
			"nodes": [0,6,9],
			"params": {
				"p": 0.9,
				"p_spontaneous": 0.6
			}

		},
		{	
			"name": "bond",
			"nodes": [1,5,11],
			"params": {
				"p": 0.7,
				"p_spontaneous": 0.4
			}
		},
		{	
			"name": "watts",
			"nodes": [3,7,10],
			"params": {
				"p": 0.7,
				"threshold": 1
			}
		},
		{	
			"name": "watts",
			"nodes": [2,4,8,12],
			"params": {
				"p": 0.6,
				"threshold": 2
			}
		},

	]
}


solver = Solver(params)
Q = solver.get_probabilities_Q()
write_Q("large_network_solve.txt", Q)











