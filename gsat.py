# -*- coding: utf-8 -*-

from random import randint
import satutil

class GSAT(object):

	choice_values = (True, False) # Used in generate random interpretation

	#
	# Recomended value for max_flips = num_clauses / 10
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
		
		while True:
			rintp = satutil.RandomInterpretation(self.num_vars)
			if self.Satisfies(rintp):
				rintp.remove(None)
				return rintp

			# Flip some variables
			for j in xrange(self.max_flips):
				var_to_flip, num_sat_clauses = self.VariableToFlip(rintp)
				rintp[var_to_flip] = not rintp[var_to_flip]
				if(self.num_clauses == num_sat_clauses):
					rintp.remove(None)
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
		used_nums = set()

		for i in xrange(self.num_vars):
			i = randint(1, self.num_vars)
			if not i in used_nums:
				used_nums.add(i)

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
			if satutil.IsClauseSatisfied(clause, interpretation):
				satisfied_clauses += 1

		return satisfied_clauses

	#
	#
	def Satisfies(self, interpretation):
		"""
		Satisfies(interpretation: [boolean]): boolean

		Check if an interpretation satisfies this formula
		"""
		for clause in self.clauses:
			if not satutil.IsClauseSatisfied(clause, interpretation):
				return False

		return True