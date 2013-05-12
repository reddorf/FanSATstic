# -*- coding: utf-8 -*-

import copy
import satutil
import datautil
import systematicsearch


#
#
def solve(num_variables, clauses, selection_heuristic):
    """
    Uses the dpll algorithm to determine if the formula is satisifiable
    or unsatisfiable
    
    Returns an interpretation if the formula is satisfiable or None
    if it is unsatisfiable
    """
    
    litclauses = datautil.classifyClausesPerLiteral(clauses)
    variables = range(1,num_variables+1)
    interpretation = [None for _ in xrange(num_variables+1)]
    
    # Remove the used variables and its associated clauses and literals
    # and saves the assignation to interpretation
    # As this call is the first one, every variable deleted here it is not
    # necessary to put it back to check it with other combinations
    if not unitPropagation(variables, clauses, litclauses, interpretation):
        return None    

    return _solve(variables, clauses, litclauses, interpretation, 
                  selection_heuristic)
       
#
#
def _solve(variables, clauses, litclauses, interpretation, heuristic):

    # All the variables were used the interpretation is now a solution    
    if not variables:
        return interpretation 
    
    # All the clauses were eliminated without the assignation of some variables
    # That means that these variables are meaningless
    if not clauses:
        for v in variables:
            interpretation[v] = satutil.getRandomAssignation()     
        return interpretation
            
    c_variables = copy.deepcopy(variables)    
    c_clauses = copy.deepcopy(clauses)
    c_litclauses = copy.deepcopy(litclauses)    

    var = heuristic(variables, litclauses)
    c_variables.remove(var)    
    
    # Pure literal
    nvar = -var
    if litclauses.has_key(var) and not litclauses.has_key(nvar):
        interpretation[var] = True
        systematicsearch.removeClausesWithLiteral(var, c_clauses, c_litclauses)
        
        return _solve(c_variables, c_clauses, c_litclauses, interpretation,
                      heuristic)
                      
    elif not litclauses.has_key(var) and litclauses.has_key(nvar):
        interpretation[var] = False
        systematicsearch.removeClausesWithLiteral(nvar, c_clauses, c_litclauses)
        
        return _solve(c_variables, c_clauses, c_litclauses, interpretation,
                      heuristic)
                      
    # Positive variable
    interpretation[var] = True       
    
    if systematicsearch.removeLiteralFromClauses(nvar, c_clauses, c_litclauses):
        
        systematicsearch.removeClausesWithLiteral(var, c_clauses,c_litclauses)
        if _solve(c_variables, c_clauses, c_litclauses, interpretation,
                  heuristic):
            return interpretation          
       
    # Create the copy of the clauses and litclauses again to explore the -var branch
    c_clauses = copy.deepcopy(clauses)
    c_litclauses = copy.deepcopy(litclauses)       
      
    # Negative variable
    interpretation[var] = False
    
    if systematicsearch.removeLiteralFromClauses(var, c_clauses, c_litclauses):
        
        systematicsearch.removeClausesWithLiteral(nvar, c_clauses,c_litclauses)
        if _solve(c_variables, c_clauses, c_litclauses, interpretation,
                  heuristic):
            return interpretation  
    
    return None
    
    
#
#
def unitPropagation(variables, clauses, litclauses, interpretation):
    """
    Search for clauses with only one literal and then remove the unnecessary
    information
    """
    # set of literals that belongs to a unit clause
    unit_lits = set([iter(c).next() for c in clauses if len(c) == 1])
    
    while unit_lits:
        lit = unit_lits.pop()
                        
        systematicsearch.removeClausesWithLiteral(lit, clauses, litclauses)
        
        # If removing the literal appears an empty clause return false
        if litclauses.has_key(-lit):
            if not systematicsearch.removeLiteralFromClauses(-lit, clauses,
                                                             litclauses):
                return False
                
        # Variables are represented as possitive numbers
        alit = abs(lit)
        variables.remove(alit)
        
        # Save the interpretation for var
        interpretation[alit] = lit > 0
        
        # If all the previous unit lits have been removed check for possible
        # new unit lits
        if not unit_lits:
            unit_lits = set([iter(c).next() for c in clauses if len(c) == 1])
                
    return True