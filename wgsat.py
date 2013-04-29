# -*- coding: utf-8 -*-

import satutil

#
#
def Solve(num_vars, clauses, litclauses, maxflips):
    
    UpdateUnsatWeights = satutil.IncrementUnsatWeights
    RndInterpretationGenerator = satutil.RandomInterpretation    
    InitializeClausesData = satutil.InitializeWeightedClausesData
    ChoseAndFlipVar = satutil.WeightedChoseAndFlipVar
    
    num_clauses = len(clauses)
    var_range = xrange(1, num_vars+1)
    flip_range = xrange(maxflips)
    
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