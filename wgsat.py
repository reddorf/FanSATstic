# -*- coding: utf-8 -*-

import satutil
import sys
#
#
def Solve(num_vars, clauses, litclauses, maxflips):
    
    UpdateUnsatWeights = satutil.IncrementUnsatWeights
    RndInterpretationGenerator = satutil.RandomInterpretation    
    
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

#
#
def InitializeClausesData(clauses, intp, csatlits, cweight):
    
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
def ChoseAndFlipVar(litclauses, rintp, csatlits, cweight, old_num_satclauses,
                    var_range):
    best_wsat_clauses = -1
    best_sat_clauses = -1
    chosed_var = 0
    
    for i in var_range:
        num_sat_change, num_wsat_change = SatClausesOnIntpChange(litclauses[i],
                                                                rintp, csatlits,
                                                                cweight,
                                                        old_num_satclauses, i)
        if num_wsat_change > best_wsat_clauses:
            best_wsat_clauses = num_wsat_change
            best_sat_clauses = num_sat_change
            chosed_var = i
    
    FlipVar(litclauses[chosed_var], rintp, csatlits, chosed_var)
    
    return best_sat_clauses
    
#
#
def SatClausesOnIntpChange(varclauses, rintp, csatlits, cweight,
                           num_satclauses, var):
        
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
    
#
#
def FlipVar(varclauses, rintp, csatlits, chosed_var):
    
    rintp[chosed_var] = not rintp[chosed_var]
    lit = chosed_var if rintp[chosed_var] else -chosed_var    
    
    for c in varclauses:
        if lit in c:
            csatlits[c] += 1
        else:
            csatlits[c] -= 1
    