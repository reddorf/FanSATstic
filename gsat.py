# -*- coding: utf-8 -*-

from random import randint
import satutil

#
#
def Solve(num_vars, clauses, max_flips):
	"""
	Solve(): [boolean, boolean, ...]

	Tries to find a solution to the given formula using GSAT algorithm
	"""	
	checkNumSat = satutil.NumSatisfiedClauses
	num_clauses = len(clauses)
	var_range = xrange(1, num_vars+1)

	while True:
		rintp = satutil.RandomInterpretation(num_vars)
		if satutil.Satisfies(clauses, rintp):
			return rintp

		# Flip some variables
		for j in xrange(max_flips):
			num_sat_clauses = FlipVar(var_range, clauses, rintp)
			if num_clauses == num_sat_clauses:
				return rintp

#
#
def FlipVar(var_range, clauses, interpretation):
	"""
	VariableToFlip(interpretation): (choosed_var:int, num_sat_clauses:int)

	Search the best variable to flip and return the index of this variable
	and the number of satisfied clauses due to this modification
	"""
	chosed_variable = 0
	best_result = -1
	checkNumSat = satutil.NumSatisfiedClauses

	for i in var_range:
		interpretation[i] = not interpretation[i]
		result = checkNumSat(clauses, interpretation)
		interpretation[i] = not interpretation[i]

		if result > best_result:
			best_result = result
			chosed_variable = i

	interpretation[chosed_variable] = not interpretation[chosed_variable]

	return best_result