# -*- coding: utf-8 -*-

from random import randint, random, randrange
import satutil

def Solve(num_vars, clauses, max_flips, wprob):
	"""
	Solve(): [boolean, boolean, ...]

	Tries to find a solution to the given formula using GSAT algorithm
	"""	
	num_clauses = len(clauses)

	while True:
		rintp = satutil.RandomInterpretation(num_vars)
		if satutil.Satisfies(clauses, rintp):
			return rintp

		# Flip some variables
		old_sat_clauses = satutil.NumSatisfiedClauses(clauses, rintp)
		for j in xrange(max_flips):
			prob = random()
			if prob < wprob:
				num_sat_clauses = RndWalk(clauses, rintp)
			else:
				num_sat_clauses = FlipVar(rintp, clauses, num_vars)
				if num_sat_clauses == old_sat_clauses:
					num_sat_clauses = RndWalk(rintp, clauses)

			if num_clauses == num_sat_clauses:
				return rintp

#
#
def FlipVar(interpretation, clauses, num_vars):
	"""
	VariableToFlip(interpretation): num_sat_clauses:int

	Search the best variable to flip and return the index of this variable
	and the number of satisfied clauses due to this modification
	"""
	choosed_variable = 0
	best_result = -1

	for i in xrange(num_vars):
		interpretation[i] = not interpretation[i]
		result = satutil.NumSatisfiedClauses(clauses, interpretation)
		interpretation[i] = not interpretation[i]

		if result > best_result:
			best_result = result
			choosed_variable = i
	
	interpretation[choosed_variable] = not interpretation[choosed_variable]
	return best_result

#
#
def RndWalk(clauses, interpretation):
	satCheck = satutil.IsClauseSatisfied

	for clause in clauses:
		if not satCheck(clause, interpretation):
			chosen_one = abs(clause[randrange(len(clause))])
			interpretation[chosen_one] = not interpretation[chosen_one]

	return satutil.NumSatisfiedClauses(clauses, interpretation)
