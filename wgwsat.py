# -*- coding: utf-8 -*-

import localsearch
import datautil
import random

#
#
def solve(num_vars, clauses, maxflips, wprob):
    """
    Solve(num_vars, clauses, litclauses, maxflips, wprob) -> [None,bool,...]

    Try to find an interpretation that satisfies the given formula.

    The solution is composed by list of boolean values, but the first element
    (index 0) should be None. Otherwise an error has happened.

    Note: there can't be repeated clauses or literals into a clause in the 
    formula

    """

    UpdateUnsatWeights = localsearch.incrementUnsatWeights
    RndInterpretationGenerator = localsearch.randomInterpretation    
    InitializeClausesData = localsearch.initializeWeightedClausesData
    ChoseAndFlipVar = localsearch.weightedChoseAndFlipVar
    
    num_clauses = len(clauses)
    var_range = xrange(1, num_vars+1)
    flip_range = xrange(maxflips)
    litclauses = datautil.classifyClausesPerVariable(num_vars, clauses)    
    
    csatlits = { c: 0 for c in clauses }
    cweight = { c : 1 for c in clauses }
      
    while True:
        rintp = RndInterpretationGenerator(num_vars)
        num_satclauses = InitializeClausesData(clauses, rintp, csatlits, 
                                               cweight)     
        
        if num_satclauses == num_clauses:
            return rintp
        
        for i in flip_range:
            prob = random.random()
                        
            if prob < wprob:
                num_satclauses = randomWalk(clauses, litclauses, rintp,
                                            csatlits, num_satclauses)
                                            
            else:
                num_satclauses = ChoseAndFlipVar(litclauses, rintp, csatlits,
                                                 cweight, num_satclauses,
                                                 var_range)

            if num_satclauses == num_clauses:
                return rintp

            UpdateUnsatWeights(clauses, rintp, cweight)
    
#
#
def randomWalk(clauses, litclauses, rintp, csatlits, num_satclauses):
    
    var = 0    
    
    for c in clauses:
        if csatlits[c] == 0:
            var = abs(random.sample(c,1)[0])
            break
            
    rintp[var] = not rintp[var]

    for c in litclauses[var]:
        satlits = csatlits[c]
        
        # If num sat lits was 0 with the flip it must be 1
        # so the clause is satisfied with the change
        if not satlits:
            num_satclauses += 1
            satlits = 1
        
        # If the var is falsified it meas it was the only satisfied literal
        # with the previous interpretation
        elif satlits == 1:
            lit = var if rintp[var] else -var
            if lit in c:
                satlits = 2
            else:
                satlits = 0
                num_satclauses -= 1                
        
        # If the var is falsified discount it but the clause remains staified
        # If the var is staisfied count it but the clause was already satisfied
        else:
            lit = var if rintp[var] else -var
            if lit in c:
                satlits += 1
            else:
                satlits -= 1
        
        csatlits[c] = satlits

    return num_satclauses