#!/usr/bin/env python
# -*- coding: utf-8 -*-

# WARNING: Converted to python3 but it should run in python 2.7

# TODO Optimize DIMACS Parser. Object + Encapsulation?
# TODO Solver Logic

from sys import argv, exit
from dimacs import ParseCNF
from solver import Solver

import random

__program__='FanSATstic - Local Search Sat Solver'
__authors__=['Marc Piñol Pueyo <mpp5@alumnes.udl.cat>',
			'Josep Pon Farreny <jpf2@alumnes.udl.cat>']
__copyright__='Copyright 2013, Marc Piñol Pueyo & Josep Pon Farreny'

__version__='0.1a'
__license__='GPL'

#
#
def Main():
	"""
	Main(): void
	"""
	if len(argv) < 2:
		PrintHelp()
		exit(-1)

	dimacs_file = OpenFileOrDie(argv[1], 'r')
	num_vars, num_clauses, clauses = ParseCNF(dimacs_file)
	dimacs_file.close()
	
	# print 'Num Variables:', num_vars
	# print 'Num Clauses:', num_clauses
	# print 'Clauses:'
	# for c in clauses:
	# 	print c

	solver = Solver(num_vars, num_clauses, clauses, num_clauses//2)
	#res = solver.Solve()
	print(res)
	print(FormatResult(res))

#
#
def FormatResult(bool_result):
	s = 'v'
	for ind,b in enumerate(bool_result):
		if b:
			s = s + ' %d' % (ind+1)
		else:
			s = s + ' %d' % (-(ind+1) )
	return s
#
#
def OpenFileOrDie(fname, mode):
	"""
	OpenFileOrDie(fname:string, mode:string): void
	Tries to open the specified file with the specified mode.
	Abort on failure.
	"""
	try:
		return open(fname, mode)
	except Exception:
		exit('Error opening file: %s' % fname)

#
#	
def PrintHelp():
	"""
	PrintHelp(): void
	Prints a help message on stdout
	"""
	print(__program__)
	print('Version:', __version__, '\n')

	print('Authors:\n') 
	for i in __authors__:
		print('\t%s' % (i))
	
	print('Usage:\n%s <input-file>' % (argv[0]))
	print('\tinput-file must be in dimacs cnf format')

#
#
if __name__ == '__main__':
	random.seed(15254354355)
	Main()