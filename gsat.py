# -*- coding: utf-8 -*-

import localsearch
import datautil

#
#
def solve(num_vars, clauses, maxflips):
    """
    Solve(num_vars, clauses, litclauses, maxflips, wprob) -> [None,bool,...]

    Try to find an interpretation that satisfies the given formula.

    The solution is composed by list of boolean values, but the first element
    (index 0) should be None. Otherwise an error has happened.

    Note: there can't be repeated clauses or literals into a clause in the 
    formula

    """    
    RndInterpretationGenerator = localsearch.randomInterpretation       
    InitializeClausesData = localsearch.initializeClausesData
    ChoseAndFlipVar = localsearch.choseAndFlipVar
    
    litclauses = datautil.classifyClausesByVariable(num_vars, clauses)
    num_clauses = len(clauses)
    var_range = xrange(1, num_vars+1)
    flip_range = xrange(maxflips)
    
    csatlits = { c: 0 for c in clauses }
       
    while True:
        rintp = RndInterpretationGenerator(num_vars)
        num_satclauses = InitializeClausesData(clauses, rintp, csatlits)
        
        if num_satclauses == num_clauses:
            return rintp
        
        for i in flip_range:
            num_satclauses = ChoseAndFlipVar(litclauses, rintp, csatlits, 
                                    num_satclauses, var_range)
                                    
            if num_satclauses == num_clauses:
                return rintp