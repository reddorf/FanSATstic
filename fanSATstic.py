#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO Solver Logic

from sys import argv, exit
from dimacs import ParseCNF

import gsat
import gwsat
import wgsat
import wgwsat
import ssolver

import random

__program__='FanSATstic - Local Search Sat Solver'
__authors__=['Marc Piñol Pueyo <mpp5@alumnes.udl.cat>',
			'Josep Pon Farreny <jpf2@alumnes.udl.cat>']
__copyright__='Copyright 2013, Marc Piñol Pueyo & Josep Pon Farreny'

__version__='0.3a'
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
	num_vars, clauses = ParseCNF(dimacs_file, tuple)
	dimacs_file.close()
	
	# print 'Num Variables:', num_vars
	# print 'Num Clauses:', len(clauses)
	# print 'Clauses:'
	# for c in clauses:
	# 	print c

	max_flips = len(clauses)//2

	#res = gsat.Solve(num_vars, clauses, max_flips)
	#res = wgsat.Solve(num_vars,clauses, max_flips)
	#res = gwsat.Solve(num_vars, clauses, max_flips, 0.4)
	res = wgwsat.Solve(num_vars, clauses, max_flips, 0.4)

	#res = ssolver.Solve(num_vars, clauses)
	del res[0]	# Solution starts with None. Variable zero doesn't exists
	
	print 'c Max Flips:', max_flips
	print 's SATISFIABLE'
	print 'v', FormatResult(res)

#
#
def FormatResult(bool_result):
	s=''
	for ind,b in enumerate(bool_result):
		if b:
			s += ' %d' % (ind+1)
		else:
			s += ' %d' % (-(ind+1) )
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
	print 'Version:', __version__

	print('Authors:') 
	for i in __authors__:
		print('\t%s' % (i))
	
	print('\nUsage:\n%s <input-file>' % (argv[0]))
	print('\tinput-file must be in dimacs cnf format')

#
#
if __name__ == '__main__':
	#random.seed(15254354355)
	Main()