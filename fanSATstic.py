#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dp
import gsat
import wgsat
import gwsat
import wgwsat
import argparse
import datautil
import heuristics

__version__='0.3'
__license__='GPL'
__authors__=['Marc Piñol Pueyo <mpp5@alumnes.udl.cat>',
            'Josep Pon Farreny <jpf2@alumnes.udl.cat>']

__description__='FanSATstic v%s' % __version__

# List of possible algorithms
GSAT = 'gsat'
GWSAT = 'gwsat'
local_search_algs = [GSAT, GSAT]

DAVIS_PUTNAM = 'dp'
systematic_search_algs = [DAVIS_PUTNAM]

# Variable selection heuristics
MOST_OFTEN = 'most_often'
MOST_EQUILIBRATED = 'most_equilibrated'
var_selection_heuristics = { 
                    MOST_OFTEN : heuristics.mostOftenVariable,
                    MOST_EQUILIBRATED : heuristics.mostEqulibratedVariable
                                }

#
#
def main(options):
    """
    Main(options): void
    """
    if isLocalSearch(options.algorithm):
        executeLocalSearchAlgorithm(options)

    elif isSystematicSearch(options.algorithm):
        executeSystematicSearchAlgorithm(options)

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
        num_vars, clauses = datautil.parseCNF(options.file)
        comments = ''

        # Chose and run algorithm
        res = None
        if GSAT == options.algorithm.lower():

            if options.weighted:
                comments += 'Solved With: Weighted GSAT'
                res = wgsat.solve(num_vars, clauses, len(clauses)//2)
            else:
                comments += 'Solved With: GSAT'
                res = gsat.solve(num_vars, clauses, len(clauses)//2)

        elif GWSAT == options.algorithm.lower():

            if options.weighted:
                comments += 'Solved With: Weighted GWSAT'
                res = wgwsat.solve(num_vars, clauses, len(clauses)//2, 0.4)
            else:
                comments += 'Solved With: GWSAT'
                res = gwsat.solve(num_vars, clauses, len(clauses)//2, 0.35)
        else:
            raise Exception('Unspecified algorithm')

        # If the formula it is not satisfiable this lines are never executed
        del res[0]
        print 's SATISFIABLE'
        printComments(comments)
        print formatResult(res)

    except Exception, e:
        print type(e), ':', str(e)

#
#
def executeSystematicSearchAlgorithm(options):
    """
    Execute the specified algorthim and prints the result
    """

#    try:
    num_vars, clauses = datautil.parseCNF(options.file)
    comments = ''

    if DAVIS_PUTNAM == options.algorithm.lower():
        comments += 'Using DP algorithm (The orignal DP not DPLL)\n'
        comments += 'The DP algorithm do not give a model, only answer if ' \
                    'the foruma is satisfiable or unsatisfiable'

        res = dp.solve(num_vars, clauses,
                       var_selection_heuristics[options.vselection])
                       
        printComments(comments)
        if res:
            print 's SATISIFIABLE'
        else:
            print 's UNSATISFIABLE'
                    
#    except Exception, e:
#       print '%s: %s' % (e.__class__.__name__, str(e))

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
                    choices=local_search_algs + systematic_search_algs,
                    required=True, help='Specifies which algorithm use to '
                                        'solve the formula')

    parser.add_argument('-vsh', '--vselection', action='store',
                        default=MOST_OFTEN,
                        choices=var_selection_heuristics.keys(),
                        help='Specfies the variable selection heuristic.'
                        'These heuristics are used only in the systematic '
                        'search algorithms. DEFAULT = %s' % MOST_OFTEN)

    parser.add_argument('-w', '--weighted', action='store_true',
                    default=False,
                    help='Uses a weighted version of the algorithms (If exists)')

    options = parser.parse_args()

    main(options)