import numpy as np

class ResponseFunction:
	
	def __init__(self, params):
		self.params = params
		self.__configure()

	def __configure(self):
		if self.params["name"] == "watts":
			self.resp_func = lambda m: self.watts_threshold(m)
		elif self.params["name"] == "bond":
			self.resp_func = lambda m: self.bond_percolation(m)
		else:
			self.resp_func = lambda m:  0.0

	def watts_threshold(self, m):
		"""
		The watts threshold function.

		Input
		---------------
		m [number] :  Number of active neigbors

		Return
		---------------
		[float] : Probability of activation

		"""
		if m >= self.params["params"]["threshold"]:
			return np.float128(self.params["params"]["p"])
		else:
			return np.float128(0.0)
		return

	def bond_percolation(self, m):
		"""
		The bond percolation response function

		Input
		---------------
		m [number] :  Number of active neigbors

		Return
		---------------
		[float] : Probability of activation

		"""
		if m > 0:
			return (np.float128(1.0) - np.float128((1.0 - self.params["params"]["p"]) ** m)*(1.0-np.float128(self.params["params"]["p_spontaneous"])))
		else:
			return np.float128(self.params["params"]["p_spontaneous"])


