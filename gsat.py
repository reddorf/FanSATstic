# -*- coding: utf-8 -*-

import satutil

#
#
def Solve(num_vars, clauses, litclauses, maxflips):
    
    num_clauses = len(clauses)
    var_range = xrange(1, num_vars+1)
    flip_range = xrange(maxflips)
    
    csatlits = { c: 0 for c in clauses }
       
    while True:
        rintp = satutil.RandomInterpretation(num_vars)
        num_satclauses = InitializeClausesData(clauses, rintp, csatlits)
        
        if num_satclauses == num_clauses:
            return rintp
        
        for i in flip_range:
            num_satclauses = ChoseAndFlipVar(litclauses, rintp, csatlits, 
                                    num_satclauses, var_range)
                                    
            if num_satclauses == num_clauses:
                return rintp

#
#
def InitializeClausesData(clauses, intp, csatlits):
    
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
def ChoseAndFlipVar(litclauses, rintp, csatlits, old_num_satclauses,
                    var_range):
    best_result = -1
    chosed_var = 0
    
    for i in var_range:
        num_sat_change = SatClausesOnIntpChange(litclauses[i], rintp,
                                                csatlits, old_num_satclauses,
                                                i)
        if num_sat_change > best_result:
            best_result = num_sat_change
            chosed_var = i
    
    FlipVar(litclauses[chosed_var], rintp, csatlits, chosed_var)
    
    return best_result
    
#
#
def SatClausesOnIntpChange(varclauses, rintp, csatlits, num_satclauses, var):
        
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
def FlipVar(varclauses, rintp, csatlits, chosed_var):
    
    rintp[chosed_var] = not rintp[chosed_var]
    lit = chosed_var if rintp[chosed_var] else -chosed_var    
    
    for c in varclauses:
        if lit in c:
            csatlits[c] += 1
        else:
            csatlits[c] -= 1  