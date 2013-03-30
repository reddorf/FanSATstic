# -*- coding: utf-8 -*-

from random import random, randrange
import satutil
import copy

def Solve(num_vars, clauses, max_flips, wprob):
	"""
	Solve(): [boolean, boolean, ...]

	Tries to find a solution to the given formula using GSAT algorithm
	"""
	checkSat = satutil.Satisfies
	incrementUnsatWeights = satutil.IncrementUnsatWeights
	var_range = xrange(1, num_vars + 1)
	num_clauses = len(clauses)

	# Weight structure
	weights = { c: 1 for c in clauses }

	while True:
		rintp = satutil.RandomInterpretation(num_vars)
		if checkSat(clauses, rintp):
			return rintp

		# Flip some variables
		for j in xrange(max_flips):
			prob = random()

			if prob < wprob:
				num_sat_clauses = RndWalk(clauses, rintp)
			else:
				num_sat_clauses = FlipVar(rintp, clauses, var_range, weights)

			if(num_clauses == num_sat_clauses):
				return rintp

			incrementUnsatWeights(clauses, rintp, weights)

#
#
def FlipVar(interpretation, clauses, var_range, weights):
	chosed_variable = 0
	best_result = -1
	checkNumWSat = satutil.NumSatisfiedWeightedClauses

	for i in var_range:
		interpretation[i] = not interpretation[i]
		result = checkNumWSat(clauses, interpretation, weights)
		interpretation[i] = not interpretation[i]

		if result > best_result:
			best_result = result
			chosed_variable = i

	interpretation[chosed_variable] = not interpretation[chosed_variable]

	return satutil.NumSatisfiedClauses(clauses, interpretation)

#
#
def RndWalk(clauses, interpretation):
	satCheck = satutil.IsClauseSatisfied

	for clause in clauses:
		if not satCheck(clause, interpretation):
			chosen_one = abs(clause[randrange(len(clause))])
			interpretation[chosen_one] = not interpretation[chosen_one]

	return satutil.NumSatisfiedClauses(clauses, interpretation)