# -*- coding: utf-8 -*-

from random import choice

#
#
def RandomInterpretation(num_vars):
	"""
	RandomInterpretation(num_vars:int): [boolean]

	Creates a random interpretation for this formula
	"""
	return [ choice( (True, False) ) for i in xrange(num_vars) ]

#
#
def IsClauseSatisfied(clause, interpretation):
	"""
	IsClauseSatisfied(clause:iterable(int),
					  interpretation:iterable(boolean)): boolean

	Returns true if the given clause is satisfied by the specified
	interpretation
	"""
	for lit in clause:
		if interpretation[lit-1] if lit > 0 else not interpretation[-lit-1]:
			return True
	return False
