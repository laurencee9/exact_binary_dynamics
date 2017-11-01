import networkx as nx
import numpy as np
import itertools as it
from ResponseFunction import ResponseFunction as RF



class Solver:

	def __init__(self, params):
		
		self.params = params
		self.__configure()

	##########################################################
	# CONFIGURATION
	##########################################################
	def __configure(self):

		if "symbolic" in self.params:
			self.symbolic_ = self.params["symbolic"]
		else:
			self.symbolic_ = False
		
		self.__load_edgelist()
		self.__configure_response_function()
		return
		
	def __load_edgelist(self):
		"""
		Load the graph
		"""	
		self.G = nx.read_edgelist(self.params["edgelist_path"],create_using=nx.DiGraph())
		# self.G = nx.convert_node_labels_to_integers(self.G, first_label=0,ordering="sorted")
		return

	def __configure_response_function(self):
		"""
		Configure the response function
		"""	
		if self.symbolic_:
			return
		rf = self.params["response_function"]
		F = {}
		for rf_case in rf:
			for node in rf_case["nodes"]:
				F[str(node)] = RF(rf_case)

		nx.set_node_attributes(self.G,"rf",F)
		return 

	##########################################################
	# HELPER
	##########################################################

	def does_edge_exist(self, u, v):
		"""
		Indicate if an edge exist from node u to node v.

		Return 
		--------------
		1 : The edge exits
		0 : The edge does not exist

		"""
		return 1 if (u in G.neighbors(v)) else 0


	def list_to_string(self, config):
		"""
		Convert a list of elements ot a string. No separetor between elements.

		Example
		---------------
		print(list_to_string([1,2,31,2])) -> "12312"


		Return
		---------------
		[str] : The string
		"""
		a = ""
		for i in config:
			a += str(i)
		return a

	##########################################################
	# COMPUTATION
	##########################################################

	def get_probabilities_Q(self):
		"""
		Give the probability Q for each possible configuration.

		Return
		---------------------
		Dictionnary of probabilities where the key is the configuration as a string (e.g. "10101110") and the value is Q(l;n)


		"""
		possible_configs = self.get_possible_configurations()
		Q = self.get_probabilities_Q_possible(possible_configs)
		return Q

	def get_possible_configurations(self):
		"""
		Get all the possible configurations of the graph.
		In a possible configuration, it must exist a path between each node and a source or a spontaneous active node.
		
		Return
		--------------------------
		Dictionnary where keys are the config as a string (i.e. "0101011011") and value are sets of the parent configurations.
	
		"""

		#Dict of all possible configurations
		dict_configurations = {}
		N = len(self.G.nodes())

		#Get the seed nodes
		seed_nodes = set()
		for node in self.G.nodes():
			if self.symbolic_ == True:
				seed_nodes.add(node)
			else:
				if self.G.node[node]["rf"].resp_func(0)>0.0:
					seed_nodes.add(node)

		#Initial configuration : All nodes are inactive
		initial_config = [0]*N
		config_str = self.list_to_string(initial_config)
		dict_configurations[config_str] = {"adjacent_nodes" :seed_nodes, "parent_configs":set()}
		list_config_size1 = [config_str]

		for size in range(1,N):
			
			#List of the new config
			list_config_size_str2 = set()
			list_config_size_2 = []

			for config in list_config_size1:

				#Adjacent Nodes
				for node in dict_configurations[config]["adjacent_nodes"]:

					#Update the config
					new_config = config
					list_new = list(new_config)
					list_new[int(node)]= "1"
					new_config = "".join(list_new)

					#Adjacent
					adjacent_nodes =  dict_configurations[config]["adjacent_nodes"].copy()
					adjacent_nodes.remove(node)
					for neighbors in self.G.neighbors(node):
						#Check that adjacent_nodes are not already active
						if list_new[int(neighbors)] != "1":
							adjacent_nodes.add(neighbors)

					#Update dict and lists
					new_config_str = self.list_to_string(new_config)
					if new_config_str in list_config_size_str2:
						dict_configurations[new_config_str]["parent_configs"].add(config)
					else:
						dict_configurations[new_config_str]={"adjacent_nodes":adjacent_nodes, "parent_configs" : set([config]) }
						list_config_size_str2.add(new_config_str)
						list_config_size_2.append(new_config)

			list_config_size1 = list_config_size_2

		all_configs_with_parent = {}
		for config in dict_configurations:
			all_configs_with_parent[config] = dict_configurations[config]["parent_configs"]

		return all_configs_with_parent

	def get_probabilities_Q_possible(self, possible_configs):
		"""
		Get the probability Q(l;n) for each configuration in the possible_configs dictionnary.
		The implementation is based on the recursive equation of the paper.
		
		Input
		----------------------
		possible_configs: Dictionnary where keys are the config as a string (i.e. "0101011011") and value are sets of the parent configurations.
	
		Return 
		----------------------
		Dictionnary of probabilities where the key is the configuration as a string (e.g. "10101110") and the value is Q(l;n)

		"""
		#the master dictionnary
		dict_config = {}
		prob_tot = 1.0
		#order by size to simplify the calculation
		possible_config_ordered_by_size = self.regroup_config_by_size(possible_configs)

		N = len(self.G.nodes())

		#Initial configuration
		initial_config = [0]*N
		if self.symbolic_:
			dict_config[self.list_to_string(initial_config)] = "<prod>"+";".join(["G("+str(node)+","+str(0)+")" for node in self.G.nodes()])+"</prod>"
		else:
			dict_config[self.list_to_string(initial_config)] = np.float128(np.product([(1.0-self.G.node[node]["rf"].resp_func(0)) for node in self.G.nodes()]))
			prob_tot -= dict_config[self.list_to_string(initial_config)]

		for size in range(1,N+1):
			if size in possible_config_ordered_by_size:
				for config_str in possible_config_ordered_by_size[size]:

					Q_ln = self.solve_specific_configuration(config_str, dict_config, possible_configs)
					dict_config[config_str] = Q_ln
					prob_tot -= Q_ln

		dict_config["1"*N] = prob_tot
		return dict_config

	def regroup_config_by_size(self, possible_configs):
		"""
		Regroup the possible configuration by their sizes. 
		
		Input
		----------------------
		possible_configs: Dictionnary where keys are the config as a string (i.e. "0101011011") and value are sets of the parent configurations.
	
		Return 
		--------------------
		Dictionnary where the key is the size of the configurations (Int) and the value is a list of configurations (Configuration are strings)

		"""
		dict_config = {}
		for config in possible_configs:

			size = np.sum([int(i) for i in list(config)])
		
			try:
				dict_config[size].append(config)
			except:
				dict_config[size] = [config]

		return dict_config

	def solve_specific_configuration(self, config_str, dict_config, possible_configs ):
		"""
		Solve Q(l;n) for a specific configuration

		Input
		----------------------
		config_str: The configuration to solve as String

		dict_config: The dictionnary containing all the previously solved configuration (i.e. dict_config[config]->Q(l;n) )

		possible_configs: Dictionnary where keys are the config as a string (i.e. "0101011011") and value are sets of the parent configurations.
		

		Return
		----------------------
		float : Q(l;n) for the desired configuration 

		"""
		N = len(self.G.nodes())
		config = list(config_str)
		size_of_config = np.sum([int(i) for i in config])
		if self.symbolic_:
			cst = "<prod>"
		else:
			cst = 1.0


		for node in self.G.nodes():
			if config[int(node)] == "0" :
				m = np.sum([int(config[int(neigh)]) for neigh in self.G.neighbors(node)])
				if self.symbolic_:
					cst += "G("+str(node)+","+str(m)+");"  
				else:
					cst *= (1.0-self.G.node[node]["rf"].resp_func(m))

		#Get Q(l|l)
		if self.symbolic_:
			cst += "</prod>"
			Q_ll = "<add>1;"
		else:
			Q_ll = 1.0

		allU_str = self.get_all_smaller_permutations(config_str, possible_configs)


		allU_list_str = [list(a) for a in allU_str]
		allU = [0]*len(allU_list_str)

		for i,item in enumerate(allU_list_str):
			allU[i] = [int(a) for a in item]


		for u in allU:
			if self.symbolic_:
				cst2 = "<prod>"
			else:
				cst2 = 1.0
			for node in self.G.nodes():
				if config[int(node)] == "0" :
					m = np.sum([int(u[int(neigh)]) for neigh in self.G.neighbors(node)])
					# print("node :",node,"  m,",m, "G(m)-",self.G.node[node]["rf"].resp_func(m))
					if self.symbolic_:
						cst2 += "G("+str(node)+","+str(m)+");"  
					else:
						cst2 *= (1.0-self.G.node[node]["rf"].resp_func(m))

			if self.symbolic_:
				cst2 += "</prod>"
				Q_ll += "-<div>"+dict_config[self.list_to_string(u)]+";"+cst2+"</div>;"
			else:
				if cst2!=0.0:
					Q_ll -= dict_config[self.list_to_string(u)]/cst2

		if self.symbolic_:
			return "<prod>"+Q_ll+"</add>"+";"+cst+"</prod>"
		else:
			if cst2==0:
				return 0.0
			else:
				return Q_ll*cst
	

	def get_all_smaller_permutations(self, config_str, possible_configs):
		"""
		Get all the smaller configuration which are contained in the desired configuration.

		Input
		----------------
		config_str: The configuration to solve as String

		possible_configs: Dictionnary where keys are the config as a string (i.e. "0101011011") and value are sets of the parent configurations.
		

		Return 
		----------------
		list : List of all the configurations

		"""

		#For all parents (smaller configurations)

		#first level
		parents = possible_configs[config_str]

		complete_parents = set(parents)
		old_parents = set(parents)
		partial_parents = set(parents)

		while len(partial_parents) > 0 :
			# print(partial_parents)
			partial_parents = set()
			for parent in old_parents:
				partial_parents.update(possible_configs[parent])

			old_parents = partial_parents.copy()
			complete_parents.update(partial_parents)
		
		return list(complete_parents)


