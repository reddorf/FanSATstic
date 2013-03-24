# -*- coding: utf-8 -*-

from random import choice

#
#
def RandomInterpretation(num_vars):
	"""
	RandomInterpretation(num_vars:int): [boolean]

	Creates a random interpretation for this formula, starting with None to
	mach the range of values on the formula: [-num_vars, -1] U [1, num_vars]
	"""
	l = [None]
	l.extend([ choice( (True, False) ) for i in xrange(num_vars+1) ])
	return l

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
		if interpretation[lit] if lit > 0 else not interpretation[-lit]:
			return True
	return False