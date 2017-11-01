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
	rvb = make_colormap([c('#d0151d'), c('#f88d59'), 0.2, c('#f88d59') , c('#fbe18f'), 0.4, c('#fbe18f') , c('#e2f3f8'), 0.6,c('#e2f3f8') , c('#96bfdb'), 0.8, c('#96bfdb'), c('#4d74b5')])
	node_color = get_activation_probability(Q,len(G.node))



	fig = plt.figure(figsize=(7,2.5),frameon=False)
	
	edges = nx.draw_networkx_nodes(G,pos=pos,width=6, node_size=1000, linewidths=4,edge_color="#BFBFBF",node_color=node_color,with_labels=False,cmap=rvb)
	nx.draw_networkx_edges(G,pos=pos,width=4,linewidths=20,edge_color="black")

	# 


	# plt.xlim([-0.5,0.6])
	# plt.ylim([-0.3,0.3])
	ax = plt.gca()

	ax.axis('off')
	plt.savefig("./test.png")
	plt.colorbar(edges)
	plt.savefig("./test_withcolorbar.png")
	# plt.savefig("./plot/network_activation_3.pdf")
	# plt.show()

	return



params = {
	"edgelist_path" : "./edgelists/triade.txt",
	"response_function": [
		{	
			"name": "bond",
			"nodes": [0],
			"params": {
				"p": 0.1,
				"p_spontaneous": 0.99999999
			}

		},

		{	
			"name": "bond",
			"nodes": [1,2],
			"params": {
				"p": 0.4,
				"p_spontaneous": 0.2
			}
		},

	]
}


solver = Solver(params)
Q = solver.get_probabilities_Q()

norm = 0.0
for key in Q:
	norm += Q[key]
print(norm)

output_path = "./triade_solve.txt"
write_Q(output_path, Q)

# #########################################
# # Plot the probability of activation
# #########################################
# pos = {
# 	0: [1,1],
# 	1: [0.5,0.5],
# 	2: [0,0],
# 	3: [1,0],
# 	4: [1.5,0.5],
# 	5: [2.5,0.5]
# }


# G = nx.read_edgelist(params["edgelist_path"])
# G = nx.convert_node_labels_to_integers(G, first_label=0,ordering="sorted")
# plot_probability_of_activation(G, pos, Q)
















