# Dependencies
import unittest
import sys
from types import *
import numpy as np

sys.path.append('src/')
from Solver import Solver
from ResponseFunction import ResponseFunction

class SolverTestCaseWatts(unittest.TestCase):
	
	def setUp(self):
		params = {
			"edgelist_path" : "./test/edgelist.txt",
			"symbolic": True
		}
		self.params = params
		self.solver = Solver(params)
		

	def test_probability_normalized(self):
		self.Q = self.solver.get_probabilities_Q()


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(SolverTestCaseWatts)
	unittest.TextTestRunner(verbosity=2).run(suite)



