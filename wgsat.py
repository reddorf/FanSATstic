# -*- coding: utf-8 -*-

import localsearch
import datautil

#
#
def solve(num_vars, clauses, maxflips):
    
    UpdateUnsatWeights = localsearch.incrementUnsatWeights
    RndInterpretationGenerator = localsearch.randomInterpretation    
    InitializeClausesData = localsearch.initializeWeightedClausesData
    ChoseAndFlipVar = localsearch.weightedChoseAndFlipVar
    
    num_clauses = len(clauses)
    var_range = xrange(1, num_vars+1)
    flip_range = xrange(maxflips)
    litclauses = datautil.classifyClausesByVariable(num_vars, clauses)
    
    csatlits = { c: 0 for c in clauses }
    cweight = { c : 1 for c in clauses }
    
    
    while True:
        rintp = RndInterpretationGenerator(num_vars)
        num_satclauses = InitializeClausesData(clauses, rintp, csatlits,
                                               cweight)
        
        if num_satclauses == num_clauses:
            return rintp
        
        for i in flip_range:
            num_satclauses = ChoseAndFlipVar(litclauses, rintp, csatlits,
                                             cweight, num_satclauses,
                                             var_range)
                                    
            if num_satclauses == num_clauses:
                return rintp
                
            UpdateUnsatWeights(clauses, rintp, cweight)    