#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO Solver Logic

from sys import argv, exit
from dimacs import ParseCNF

import random
import wgsat
import gwsat
import gsat


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

    num_vars, clauses, litclauses = ParseCNF(argv[1], frozenset)
    
#    print 'Num Vars:', num_vars
#    print 'Num Clauses:', len(clauses)
#    print 'Clauses:'
#    for c in clauses:
#        print c
#    print 'Clauses in literal "i":'
#    for i, c in enumerate(litclauses):
#        print '%d:' % (i), c
    
    #res = gsat.Solve(num_vars, clauses, litclauses, len(clauses)//2)
    #res = wgsat.Solve(num_vars, clauses, litclauses, len(clauses)//2)
    res = gwsat.Solve(num_vars, clauses, litclauses, len(clauses)//2, 0.4)
    del res[0]
    
    print 's SATISFIABLE'
    print FormatResult(res)
    
    
#
#
def FormatResult(bool_result):
    s='v'
    for ind,b in enumerate(bool_result):
        if b:
            s += ' %d' % (ind+1)
        else:
            s += ' %d' % (-(ind+1) )
    return s

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
    random.seed(15254354355)
    Main()