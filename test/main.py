# Dependencies
import unittest
import sys
from types import *
import numpy as np

sys.path.append('../src/')
from Solver import Solver
from ResponseFunction import ResponseFunction

class SolverTestCaseWatts(unittest.TestCase):
	def setUp(self):
		params = {
			"edgelist_path" : "./edgelist.txt",
			"response_function": [
				{	
					"name": "bond",
					"nodes": [0,1,2],
					"params": {
						"p": 0.3,
						"p_spontaneous": 0.1
					}

				},
				{	
					"name": "watts",
					"nodes": [3,4],
					"params": {
						"threshold": 3.0,
						"p": 0.4
					}
				},

			]
		}
		self.params = params
		self.solver = Solver(params)
		self.Q = self.solver.get_probabilities_Q()


	def test_response_function(self):

		"""
		Verify the response functions
		"""
		for node in self.solver.G.nodes():

			self.assertIn("rf", self.solver.G.node[node])
			self.assertIsInstance(self.solver.G.node[node]["rf"], ResponseFunction )
			self.assertIs(type(self.solver.G.node[node]["rf"].resp_func(0.0)), np.float128)
			self.assertIs(type(self.solver.G.node[node]["rf"].resp_func(20.0)), np.float128)


	def test_possible_configuration(self):
		possible_config = self.solver.get_possible_configurations()
		for config in possible_config:
			self.assertIs(type(config), str)
			self.assertIs(type(possible_config[config]), set)


	def test_probability_normalized(self):
		prob_sum = 0.0
		for config in self.Q:
			prob_sum += self.Q[config]

		# Must add a margin of error
		self.assertTrue(np.abs(prob_sum-1.0)<1e-8)











if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(SolverTestCaseWatts)
	unittest.TextTestRunner(verbosity=2).run(suite)



