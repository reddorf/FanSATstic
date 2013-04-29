#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import gsat
import wgsat
import gwsat
import wgwsat
import dimacs
import argparse

__version__='0.2'
__license__='GPL'
__authors__=['Marc Piñol Pueyo <mpp5@alumnes.udl.cat>',
            'Josep Pon Farreny <jpf2@alumnes.udl.cat>']

__description__='FanSATstic v%s - Local Search Sat Solver' % __version__

#
#
def Main(options):
    """
    Main(options): void
    """
    num_vars, clauses, litclauses = dimacs.ParseCNF(options.file, frozenset)
    
    comments = ''    

    # Chose and run algorithm    
    res = None
    if options.algorithm == 'gsat':
        if options.weighted:
            comments += 'Solved With: Weighted GSAT'
            res = wgsat.Solve(num_vars, clauses, litclauses, len(clauses)//2)
        else:
            comments += 'Solved With: GSAT'
            res = gsat.Solve(num_vars, clauses, litclauses, len(clauses)//2)
            
    elif options.algorithm == 'gwsat':
        if options.weighted:
            comments += 'Solved With: Weighted GWSAT'
            res = wgwsat.Solve(num_vars, clauses, litclauses, len(clauses)//2,
                              0.4)
        else:
            comments += 'Solved With: GWSAT'
            res = gwsat.Solve(num_vars, clauses, litclauses, len(clauses)//2,
                               0.35)
    else:
        sys.exit('Error: Unspecified algorithm')
   
    del res[0]
    print 's SATISFIABLE'
    PrintComments(comments)
    print FormatResult(res)
    

#
#
def FormatResult(bool_result):
    """
    Returns a textual representation of the result
    """
    s='v'
    for ind,b in enumerate(bool_result):
        if b:
            s += ' %d' % (ind+1)
        else:
            s += ' %d' % (-(ind+1) )
    return s

#
#
def PrintComments(comments):
    """
    Prints all the comment lines followed by the comment character
    """
    for comment in comments.splitlines():
        print 'c', comment

#
#
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument('-f', '--file', action='store', default="",
                    required=True, help='Path to a cnf file')
                    
    parser.add_argument('-a', '--algorithm', action='store', default="",
                    help='Specifies which algorithm use to solve the formula',
                    choices=['gsat', 'gwsat'], required=True)
                    
    parser.add_argument('-w', '--weighted', action='store_true',
                    default=False, 
                    help='Uses a weighted version of the algorithms')

    options = parser.parse_args()     
    
    Main(options)