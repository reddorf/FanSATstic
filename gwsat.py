# -*- coding: utf-8 -*-

from random import randint, random,randrange
import satutil
import functools

class GWSAT(object):

	choice_values = (True, False) # Used in generate random interpretation

	#
	# Recomended value for max_flips = num_clauses / 10
	def __init__(self, num_vars, clauses, max_flips, wprob):
		"""
		Builds a new instance of GSAT
		"""
		self.num_vars = num_vars
		self.clauses = clauses
		self.num_clauses = len(clauses)
		self.max_flips = max_flips
		self.wprob = wprob

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
				return rintp

			# Flip some variables
			old_sat_clauses = self.NumSatisfiedClauses(rintp)
			for j in xrange(self.max_flips):
				prob = random()
				if prob < self.wprob:
					num_sat_clauses = self.RndWalk(rintp)
				else:
					num_sat_clauses = self.FlipVar(rintp)
					if num_sat_clauses == old_sat_clauses:
						num_sat_clauses = self.RndWalk(rintp)

				if(self.num_clauses == num_sat_clauses):
					return rintp

	#
	#
	def FlipVar(self, interpretation):
		"""
		VariableToFlip(interpretation): num_sat_clauses:int

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
		
		interpretation[choosed_variable] = not interpretation[choosed_variable]
		return best_result

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

	#
	#
	def RndWalk(self, interpretation):
		for clause in self.clauses:
			if not satutil.IsClauseSatisfied(clause, interpretation):
				chosen_one = abs(clause[randrange(len(clause))])
				interpretation[chosen_one] = not interpretation[chosen_one]

		return self.NumSatisfiedClauses(interpretation)