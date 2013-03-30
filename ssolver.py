# -*- coding: utf-8 -*- 

import satutil
import random
import sys

def Solve(num_vars, clauses):

	incrementUnsatWeights = satutil.IncrementUnsatWeights

	num_clauses = len(clauses)
	rintp = satutil.RandomInterpretation(num_vars)
	best_num_sat = satutil.NumSatisfiedClauses(clauses, rintp)	
	var_range = xrange(num_vars)

	if best_num_sat == num_clauses:
		return rintp

	# Weight structure
	weights = { c: 1 for c in clauses }

	while True:
		num_sat = FlipVar(clauses, rintp, var_range, best_num_sat, weights)
		incrementUnsatWeights(clauses, rintp, weights)
		if num_sat == num_clauses:
			return rintp
		elif num_sat == best_num_sat:
			best_num_sat = FlipUnsat(rintp, clauses, num_vars)
			if best_num_sat == num_clauses:
				return rintp
		else:
			best_num_sat = num_sat

#
#
def FlipUnsat(interpretation, clauses, num_vars):
	satCheck = satutil.IsClauseSatisfied
	tabu = set()

	#print '----FlipUnsat----'
	for clause in clauses:

		if not satCheck(clause, interpretation):
			for i in xrange(len(clause)):
				chosen = abs(clause[random.randrange(len(clause))])
				if chosen not in tabu:
					break

			if chosen not in tabu:
				tabu.add(chosen)		
			else:
				chosen = random.randrange(len(interpretation))

			interpretation[chosen] = not interpretation[chosen]
			
	return satutil.NumSatisfiedClauses(clauses, interpretation)

#
#
def FlipVar(clauses, interpretation, var_range, best_result, weights):
	chosed_variable = 0
	checkNumWSat = satutil.NumSatisfiedWeightedClauses

	for i in var_range:
		interpretation[i] = not interpretation[i]
		result = checkNumWSat(clauses, interpretation, weights)
		interpretation[i] = not interpretation[i]

		if result > best_result:
			best_result = result
			chosed_variable = i

	if chosed_variable != 0:
		interpretation[chosed_variable] = not interpretation[chosed_variable]
		return satutil.NumSatisfiedClauses(clauses, interpretation)
	return best_result