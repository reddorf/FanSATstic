# -*- coding: utf-8 -*-

from random import choice

#
#
def randomInterpretation(num_vars):
    """
    RandomInterpretation(num_vars:int): [boolean]

    Creates a random interpretation for this formula, starting with None to
    mach the range of values on the formula: [-num_vars, -1] U [1, num_vars]
    """
    l = [None]
    l.extend([ choice( (True, False) ) for i in xrange(num_vars) ])
    return l

#
#
def isClauseSatisfied(clause, interpretation):
    """
    IsClauseSatisfied(clause:iterable(int),
                      interpretation:iterable(boolean)): boolean

    Returns true if the given clause is satisfied by the specified
    interpretation
    """
    for lit in clause:
        if interpretation[lit] if lit > 0 else not interpretation[-lit]:
            return True
    return False

#
#
def satisfies(clauses, interpretation):
    """
    Satisfies(interpretation: [boolean]): boolean

    Check if an interpretation satisfies this formula
    """
    for clause in clauses:
        if not isClauseSatisfied(clause, interpretation):
            return False
    return True

#
#
def numSatisfiedClauses(clauses, interpretation):
    """
    NumSatisfiedClauses(clauses: [], interpretation: [boolean]): int

    Count all the satisfied clauses with the given interpretation
    """
    return sum(1 for c in clauses if isClauseSatisfied(c, interpretation))

#
#
def numSatisfiedWeightedClauses(clauses, interpretation, weights):
    """
    NumSatisfiedClauses(clauses: [], interpretation: [boolean],
                                                     weights: {clause:int}): int

    When a clause is satisfied increments the weight of that clause
    """
    return sum(weights[c] for c in clauses \
                                        if isClauseSatisfied(c, interpretation))

#
#
def incrementUnsatWeights(clauses, interpretation, weights):
    """
    Increments the amount of times that a clause was found unsatisfied
    """
    for c in clauses:
        if not isClauseSatisfied(c, interpretation):
            weights[c] += 1
            
#
#
def numSatisfiedLiterals(clause, interpretation):
    """
    Counts the number of satisfied literals with the given interpretation
    """
    satlits = 0
    
    for lit in clause:
        var = abs(lit)
        if (interpretation[var] and lit > 0) or \
            (not interpretation[var] and lit < 0):
            satlits += 1
            
    return satlits
    
#
#
def initializeClausesData(clauses, intp, csatlits):
    """
    InitializeClausesData(clauses, intp, csatlits) -> num_sat_clauses

    Initialize the number of sat literals per clause and counts the number of
    satisified clauses
    """
    num_sat_clauses = 0    
    
    for c in clauses:
        num_sat_lits = 0        
        
        for lit in c:
            if intp[lit] if lit > 0 else not intp[-lit]:
                num_sat_lits += 1
                
        csatlits[c] = num_sat_lits
                    
        # If it is different from zero
        if num_sat_lits:
            num_sat_clauses += 1    
            
    return num_sat_clauses
            
#
#
def choseAndFlipVar(litclauses, rintp, csatlits, old_num_satclauses,
                    var_range):
    """
    Chooses and flips the variable that improves or worsens less possible the
    amount of satisfied clauses
    """
    best_result = -1
    chosed_var = 0
    
    for i in var_range:
        num_sat_change = satClausesOnIntpChange(litclauses[i], rintp,
                                                csatlits, old_num_satclauses,
                                                i)
        if num_sat_change > best_result:
            best_result = num_sat_change
            chosed_var = i
    
    flipVar(litclauses[chosed_var], rintp, csatlits, chosed_var)
    
    return best_result            

#
#
def satClausesOnIntpChange(varclauses, rintp, csatlits, num_satclauses, var):
    """
    Counts the number of satisfied clauses after flipping the value of 'var'
    """
    rintp[var] = not rintp[var]
    
    for c in varclauses:
        satlits = csatlits[c]
        
        # If num sat lits was 0 with the flip it must be 1
        # so the clause is satisfied with the change
        if satlits == 0:
            num_satclauses += 1
        
        # If the var is falsified it meas it was the only satisfied literal
        # with the previous interpretation
        elif satlits == 1:
            lit = var if rintp[var] else -var
            if not lit in c:
                num_satclauses -= 1    
    
    rintp[var] = not rintp[var]
    
    return num_satclauses
    
#
#
def flipVar(varclauses, rintp, csatlits, chosed_var):
    """
    Flips the specified variable and updates the amount of satisfied literals
    in all the clauses that it appears
    """    
    rintp[chosed_var] = not rintp[chosed_var]
    lit = chosed_var if rintp[chosed_var] else -chosed_var    
    
    for c in varclauses:
        if lit in c:
            csatlits[c] += 1
        else:
            csatlits[c] -= 1
            
#
#
def initializeWeightedClausesData(clauses, intp, csatlits, cweight):
    """    
    InitializeWeightedClausesData(clauses, intp, csatlits, cweight) 
                                                        -> num_sat_clauses

    Initialize the number of sat literals per clause, counts the number of
    satisified clauses and initialize clauses's weights
    """
    num_sat_clauses = 0    
    
    for c in clauses:
        num_sat_lits = 0        
        
        for lit in c:
            if intp[lit] if lit > 0 else not intp[-lit]:
                num_sat_lits += 1
                
        csatlits[c] = num_sat_lits
                    
        # If it is different from zero
        if num_sat_lits:
            num_sat_clauses += 1
        else:
            cweight[c] += 1

    return num_sat_clauses
    
#
#
def weightedChoseAndFlipVar(litclauses, rintp, csatlits, cweight,
                            old_num_satclauses, var_range):
    """
    Chooses and flips the variable that improves or worsens less possible the
    amount of satisfied (weight) clauses
    """
    best_wsat_clauses = -1
    best_sat_clauses = -1
    chosed_var = 0
    
    for i in var_range:
        num_sat_change, num_wsat_change = weightedSatClausesOnIntpChange(
                                                        litclauses[i],
                                                        rintp, csatlits,
                                                        cweight,
                                                        old_num_satclauses,
                                                        i)
        if num_wsat_change > best_wsat_clauses:
            best_wsat_clauses = num_wsat_change
            best_sat_clauses = num_sat_change
            chosed_var = i
    
    flipVar(litclauses[chosed_var], rintp, csatlits, chosed_var)
    
    return best_sat_clauses
    
#
#
def weightedSatClausesOnIntpChange(varclauses, rintp, csatlits, cweight,
                                   num_satclauses, var):
    """
    Counts the number of satisfied clauses and it's weight after flipping 
    the value of 'var'
    """ 
    num_wsatclauses = num_satclauses

    rintp[var] = not rintp[var]
    
    for c in varclauses:
        satlits = csatlits[c]
        
        # If num sat lits was 0 with the flip it must be 1
        # so the clause is satisfied with the change
        if satlits == 0:
            num_satclauses += 1
            num_wsatclauses += cweight[c]
        
        # If the var is falsified it meas it was the only satisfied literal
        # with the previous interpretation
        elif satlits == 1:
            lit = var if rintp[var] else -var
            if not lit in c:
                num_satclauses -= 1
                num_wsatclauses -= cweight[c]
    
    rintp[var] = not rintp[var]
    
    return num_satclauses, num_wsatclauses