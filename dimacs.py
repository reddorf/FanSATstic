# -*- coding: utf-8 -*-

from sys import stderr
from itertools import groupby

#
#
def ParseCNF(cnf_file, outformat=list):
	"""
	parseCNF(f:file): (num_vars:int, clauses:outformat(int) )

	- outformat must be an iterable such as tuple or list

	Parse a file in DIMACS CNF format and returns a tuple with three components,
	the amount of variables, the amount of clauses and a list with the clauses.

	Raise an exception if there are format errors in the file
	"""
	num_vars = 0
	num_clauses = 0
	cnf_formula = []
	try:
		for num_line, line in enumerate(cnf_file):
			lvalues = line.strip().split()
			if not lvalues: continue

			if lvalues[0] == 'c':
				continue

			elif lvalues[0] == 'p':
				if lvalues[1] != 'cnf':
					raise Exception("Invalid file type after 'p'")
				num_vars = int(lvalues[2])
				num_clauses = int(lvalues[3])

			else:
				lvalues = list(map(int, lvalues))
				
				l = []
				for val in lvalues:
					if val == 0 and l:
						if outformat == list:
							cnf_formula.append( l )
						else:
							cnf_formula.append( outformat(l) )
						l = []
					else:
						l.append(val)
						if val < -num_vars or val > num_vars:
							raise Exception('Invalid variable %d. '
											'Variables must be in range [1, %d]'
											% (val, num_vars))
							
				# The same as above in a different way, without checks
				# cnf_formula.extend(SplitByValue(lvalues, (None, 0)))
				# [list(g) for k,g in itertools.groupby(iterable,lambda x:x in splitters) if not k]

	except Exception as e:
		stderr.write('Error parsing file "%s" (%d): %s' % 
						(cnf_file.name, num_line, str(e)) )
		raise e

	if outformat != list:
		cnf_formula = outformat(cnf_formula)
	return (num_vars, cnf_formula)