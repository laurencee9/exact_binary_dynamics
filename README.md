# Exact analytical solution of irreversible binary dynamics on networks

A python implementation of the exact solution of irreversible binary dynamics on networks.

## Table of content

1. [Usage](#usage)
	1. [Solver](#solver)
	2. [Parameters](#parameters)
2. [Companion article](#companion-article)


## Usage

### Solver

After having declared your paramters, you must initiate an instance and run the algorithm:

	solver = Solver(params)
	Q = solver.get_probabilities_Q()

The output of `solver.get_probabilities_Q()` is a dictionnary where keys are the configurations as strings (e.g. "101011011") and value are the probability of getting the key configuration. For example, the output could look like:

```
{
 '01110': -3.5575383784680611984e-21,
 '01111': 1.8973538018496326391e-20,
 '11001': -5.4887734982078661633e-20,
 '11000': 0.027000000000000005414,
 '10000': 0.081000000000000003455,
 '11011': 9.1479558303464436055e-20,
 '01101': -1.4230153513872244794e-20,
 '01100': 0.021000000000000002999,
 '01011': 0.0,
 '11100': 0.0090000000000000029588,
 '11101': 1.1604351377383914645e-19,
 '11010': -4.8789097761847699229e-20,
 '01010': 0.0,
 '01000': 0.062999999999999999075,
 '01001': 0.0,
 '00000': 0.72899999999999998655,
 '11110': 6.1833405149563924752e-20,
 '00100': 0.062999999999999999075,
 '10100': 0.0070000000000000004227
 }
```

### Parameters

The algorithm needs some parameters to run. We use a dictionnary to feed the parameters. 
```
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
```

 - `edgelist_path` : The path to the edgelist
 - `response_function` : A list of response functions to use.

In each element of `params["response_function"]`, you must declare the name of the response function and the nodes that apply to. 


