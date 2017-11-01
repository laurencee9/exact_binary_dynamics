import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors

plt.rcParams['text.usetex']=True
plt.rcParams['text.latex.preamble']=[r'\usepackage{amsmath}']
plt.rc('font',**{'family':'serif','serif':['Computer Modern']})
plt.rcParams['text.latex.unicode']=True
params = {'legend.fontsize': 20, 'legend.markersize': 18, 'axes.labelsize': 20, 'figure.autolayout': True}
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.size'] = 4
plt.rcParams['xtick.major.width'] = 1
plt.rcParams['xtick.minor.size'] = 2
plt.rcParams['xtick.minor.width'] = 1
plt.rcParams['ytick.major.size'] = 4
plt.rcParams['ytick.major.width'] = 1
plt.rcParams['ytick.minor.size'] = 2
plt.rcParams['ytick.minor.width'] = 1

plt.rc('xtick', labelsize=20) 
plt.rc('ytick', labelsize=20) 


def get_Q(path):
	fileO = open(path, "r")
	Q = {}
	for line in fileO:
		a = line.split("\t")
		Q[a[0]]=float(a[1])
	return Q


def order_by_size(Dict):
	Size_dict = {}

	for key in Dict:
		size = np.sum([int(u) for u in list(key)])
		if Dict[key]>1e-17:
			try:
				Size_dict[size].append(Dict[key])
			except:
				Size_dict[size] = [Dict[key]]

	return Size_dict



Q = get_Q("./large_network_solve.txt")
Size_dict = order_by_size(Q)



case = 3

a = 0
plt.figure(figsize=(7.9,3.5))
bbox = {'fc': '1.0', 'pad': 0}
colors = ['#a50026','#d73027', '#D73827','#f46d43','#fdae61','#fee090','#ffffbf','#CDE5FF', '#e0f3f8','#abd9e9','#74add1','#4575b4','#313695']
# colors= ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99']
for size in Size_dict:
	
	X = range(a,a+len(Size_dict[size]))
	Y = sorted(Size_dict[size])
	plt.plot(X,Y,"-o",linewidth=3,color=colors[size], markersize=6,markeredgecolor="black")
	if size<12:
		plt.plot([a+len(Size_dict[size])+2,a+len(Size_dict[size])+2],[0.0,1.0],"--",linewidth=1,color="#b3b3b3")
		# plt.text(a+len(Size_dict[size])+2, 0.2, "size :"+str(size), rotation=90)
	a += len(Size_dict[size]) + 4

plt.yscale('log')
# plt.
plt.ylabel("probability",fontsize=20)
plt.xlabel("configurations",fontsize=20)
plt.yticks([1e-6,1e-4,1e-2,1e-0])
plt.xticks([])
plt.xlim(-5,a+5)
plt.savefig("./configurations.pdf",bbox_inches='tight')
# plt.savefig("./plot/confi_"+str(case)+".pdf",bbox_inches='tight')


# plt.plot(X,Y,"-s",color="#226598",linewidth=1.5,markeredgewidth=0.0, markersize=6, label="Exact")
