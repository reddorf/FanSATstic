# -*- coding: utf-8 -*-

import datautil
import satutil
import systematicsearch


#
#
def solve(num_variables, clauses, selection_heuristic):
    """
    Uses the dp algorithm to determine if the formula is satisfiable or 
    unsatisfiable
    
    Returns False if the formula is Unsatisfiable and True if it is
    Satisfiable
    """
    
    litclauses = datautil.classifyClausesPerLiteral(clauses)
    variables = range(1, num_variables+1)
        
    while variables:
        
        if not unitPropagation(variables, clauses, litclauses):
            return False
            
        if not variables:
            return True
        
        # Select variable
        var = selection_heuristic(variables, litclauses)
        variables.remove(var)
        
        if not litclauses.has_key(var) and not litclauses.has_key(var):
            continue
        
        if not resolution(var, clauses, litclauses):
            return False
            
    return True


#
#
def unitPropagation(variables, clauses, litclauses):
    """
    Search for clauses with only one literal and then remove the unnecessary
    information
    
    This is an special version for DP that does not save the interpretation
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
        
        # If all the previous unit lits have been removed check for possible
        # new unit lits
        if not unit_lits:
            unit_lits = set([iter(c).next() for c in clauses if len(c) == 1])
                
    return True    

#
#
def resolution(var, clauses, litclauses):
    """
    Checks if the specified variable 'var' is a pure literal, if it is not
    then performs resolution
    """
    nvar = -var # Variable values are always possiive
    
    # Variable x only appears with one polarity (Pure literal)    
    if litclauses.has_key(var) and not litclauses.has_key(nvar):
        systematicsearch.removeClausesWithLiteral(var, clauses, litclauses)
        
    elif not litclauses.has_key(var) and litclauses.has_key(nvar):
        systematicsearch.removeClausesWithLiteral(nvar, clauses, litclauses)

    # Perform resolution with variable 'var'        
    else:
        for c in litclauses[var]:
            for n in litclauses[nvar]:
                resolvent = resolve(c, n, var)
                
                # If resolvent is the empty clause
                if not resolvent:
                    return False
                
                if not satutil.isTautology(resolvent):
                    clauses.add(resolvent)
                    
                    # KeyError should not be raised otherwise there is an error
                    # in some part of the code
                    for lit in resolvent:
                        litclauses[lit].add(resolvent)
                    
        # Remove all the clauses with the literals x and -x
        systematicsearch.removeClausesWithLiteral(var, clauses, litclauses)
        systematicsearch.removeClausesWithLiteral(nvar, clauses, litclauses)
        
    return True
    
#
#
def resolve(c1, c2, var):
    """
    Resolution method with clauses c1 and c2 using the variable var
    """
    nl = [x for x in c1 if x != var]
    nl.extend( (x for x in c2 if x != -var) ) # Use a generator to save memory
    return frozenset(nl)