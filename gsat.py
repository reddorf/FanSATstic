# -*- coding: utf-8 -*-

# TODO Test random selection in variable to flip
# TODO Check satisify operations
# TODO Check performans with a set to avoid repeated random interpretations

from random import choice

class GSAT(object):

	choice_values = (True, False) # Used in generate random interpretation

	def __init__(self, num_vars, num_clauses, clauses, max_flips):
		"""
		Builds a new instance of GSAT
		"""
		self.num_vars = num_vars
		self.num_clauses = num_clauses
		self.clauses = clauses
		self.max_flips = max_flips

	#
	#
	def Solve(self):
		"""
		Solve(): [boolean, boolean, ...]

		Tries to find a solution to the given formula using GSAT algorithm
		"""
		num_clauses = len(self.clauses)
		while True:
			rintp = self.RandomInterpretation()
			if self.Satisfies(rintp):
				return rintp

			# Flip some variables
			for j in xrange(self.max_flips):
				var_to_flip, num_sat_clauses = self.VariableToFlip(rintp)
				rintp[var_to_flip] = not rintp[var_to_flip]
				if(num_clauses == num_sat_clauses):
					return rintp

	#
	#
	def VariableToFlip(self, interpretation):
		"""
		VariableToFlip(interpretation): (choosed_var:int, num_sat_clauses:int)

		Search the best variable to flip and return the index of this variable
		and the number of satisfied clauses due to this modification
		"""
		choosed_variable = 0
		best_result = -1

		for i in xrange(self.num_vars):
			interpretation[i] = not interpretation[i]
			result = self.NumSatisfiedClauses(interpretation)
			interpretation[i] = not interpretation[i]

			if result > best_result:
				best_result = result
				choosed_variable = i

		return (choosed_variable, best_result)

	#
	#
	def NumSatisfiedClauses(self, interpretation):
		"""
		NumSatisfiedClauses(interpretation: [boolean]): int

		Count all the satisfied clauses with the given interpretation
		"""
		satisfied_clauses = 0

		for clause in self.clauses:
			satc = False
			for v in (v for v in clause if not satc):
				satc |= interpretation[v-1] if v > 0 else \
						not interpretation[-v-1]

			if satc: satisfied_clauses += 1

		return satisfied_clauses

	#
	#
	def Satisfies(self, interpretation):
		"""
		Satisfies(interpretation: [boolean]): boolean

		Check if an interpretation satisfies this formula
		"""
		for clause in self.clauses:
			satc = False
			for v in (v for v in clause if not satc):
				satc |= interpretation[v-1] if v > 0 else \
						not interpretation[-v-1]
			if not satc:
				return False

		return True

	#
	#
	def RandomInterpretation(self):
		"""
		RandomInterpretation(): [boolean]

		Creates a random interpretation for this formula
		"""
		return [ choice( GSAT.choice_values ) 
						for i in xrange(self.num_vars) ]