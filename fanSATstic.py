#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

__description__='FanSATstic v%s' % __version__

# List of possible algorithms
local_search_algs = ['gsat', 'gwsat']
systematic_search_algs = ['dp']

#
#
def main(options):
    """
    Main(options): void
    """
    if isLocalSearch(options.algorithm):
        executeLocalSearchAlgorithm(options)
        
    #elif isSystematicSearch(options.algorithm):
                
        
    else:
        print 'Unknown algorithm'   # This should never be printed if the argparser works well
        
#
#
def isSystematicSearch(alg):
    """
    Returns true if the algorithm is one of the local search list
    """
    return alg.lower() in systematic_search_algs

#
#
def isLocalSearch(alg):
    """
    Returns true if the algorithm is one of the local search list
    """
    return alg.lower() in local_search_algs


#
#
def executeLocalSearchAlgorithm(options):
    """
    Execute the specified algorithm and prints the result
    """
    
    try:
        num_vars, clauses, litclauses=dimacs.parseCNFLocalSearch(options.file)
        
        comments = ''    
    
        # Chose and run algorithm    
        res = None
        if options.algorithm.lower() == 'gsat':
            
            if options.weighted:
                comments += 'Solved With: Weighted GSAT'
                res = wgsat.solve(num_vars, clauses, litclauses,
                                  len(clauses)//2)
            else:
                comments += 'Solved With: GSAT'
                res = gsat.solve(num_vars, clauses, litclauses,
                                 len(clauses)//2)
                
        elif options.algorithm.lower() == 'gwsat':
            
            if options.weighted:
                comments += 'Solved With: Weighted GWSAT'
                res = wgwsat.solve(num_vars, clauses, litclauses,
                                   len(clauses)//2, 0.4)
            else:
                comments += 'Solved With: GWSAT'
                res = gwsat.solve(num_vars, clauses, litclauses,
                                  len(clauses)//2, 0.35)
        else:
            raise Exception('Unspecified algorithm')
       
        del res[0]
        print 's SATISFIABLE'
        printComments(comments)
        print formatResult(res)
        
    except Exception, e:
        print 'Error:', str(e)

#
#
def formatResult(bool_result):
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
def printComments(comments):
    """
    Prints all the comment lines followed by the comment character
    """
    for comment in comments.splitlines():
        print 'c', comment

#
# Program entry point
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument('-f', '--file', action='store', default="",
                    required=True, help='Path to a cnf file')
                    
    parser.add_argument('-a', '--algorithm', action='store', default="",
                    help='Specifies which algorithm use to solve the formula',
                    choices=local_search_algs + systematic_search_algs,
                    required=True)
                    
    parser.add_argument('-w', '--weighted', action='store_true',
                    default=False, 
                    help='Uses a weighted version of the algorithms (If exists)')

    options = parser.parse_args()     
    
    main(options)