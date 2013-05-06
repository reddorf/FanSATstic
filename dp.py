# -*- coding: utf-8 -*-

import datautil
import satutil

#
#
def solve(num_variables, clauses):
    """
    Solve the given formula using the DP algorithm
    
    --- TEMPORAL ---
    Returns None if the formula is Unsatisfiable and a fake representation
    if it is Satisfiable
    """
    
    #satutil.removeTautologies(clauses)
    litclauses = datautil.classifyClausesPerLiteral(clauses)
    variables = range(1, num_variables+1)
    interpretation = [None for _ in xrange(num_variables+1)]
    
    while variables:
        
        if not unitPropagation(variables, clauses, litclauses, interpretation):
            return None
            
        if not variables:
            return interpretation
            
        var = variables.pop()
        
        if not resolution(var, clauses, litclauses, interpretation):
            return None
            
    return interpretation
        
#
#
def unitPropagation(variables, clauses, litclauses, interpretation):
    """
    Search for clauses with only one literal and then remove the unnecessary
    information
    """
    # set of literals that belongs to a unit clause
    unit_lits = set([iter(c).next() for c in clauses if len(c) == 1])
    
    for lit in unit_lits:
                        
        removeClausesWithLiteral(lit, clauses, litclauses)
        if litclauses.has_key(-lit):
            if not removeLiteralFromClauses(-lit, clauses, litclauses):
                return False
                
        # Variables are represented as possitive numbers
        alit = abs(lit)
        variables.remove(alit)
        interpretation[alit] = lit > 0        
                
    return True        

#
#
def removeClausesWithLiteral(lit, clauses, litclauses):
    """
    Removes all the clauses which contain the specified literal
    """
    # The exception KeyError should never happen, as long as the literal 
    # exists in the formula    
    for clause in litclauses[lit]:
        # The clause could be removed previously because it is associated 
        # to another literal
        try:
            clauses.remove(clause)
        except KeyError:
            pass
        
        # Remove the clause from the literal's local sets
        for l in clause:
            if l != lit:
                litclauses[l].remove(clause)
    
    del litclauses[lit]
    
#
#
def removeLiteralFromClauses(lit, clauses, litclauses):
    """
    Removes the literal from the clauses to which it belongs
    
    Returns: False if some of the reductions is the empty clause, True otherwise
    """
    for clause in litclauses[lit]:
        nc = removeLiteralFromClause(lit, clause)
        # Empty clause found
        if not nc:
            return False
        
        # Update clause on the global clauses set
        clauses.add(nc)
        clauses.remove(clause)
        
        # Update clause in all the literal's local sets
        for l in clause:
            if l != lit:
                lset = litclauses[l]
                lset.remove(clause)
                lset.add(nc)
    
    # Delete the loca set for the specified literal
    del litclauses[lit]    
    
    return True
    
#
#
def removeLiteralFromClause(lit, clause):
    """
    Creates a new clause without the specified literal
    """
    nc = frozenset([x for x in clause if x != lit])
    return nc
    
#
#
def resolution(var, clauses, litclauses, interpretation):
    """
    Checks if the specified variable 'var' is a pure literal, if it is not
    then performs resolution
    """
    nvar = -var # Variable values are always possiive
    
    # Variable x only appears with one polarity (Pure literal)    
    if litclauses.has_key(var) and not litclauses.has_key(nvar):
        interpretation[var] = True
        removeClausesWithLiteral(var, clauses, litclauses)
        
    elif not litclauses.has_key(var) and litclauses.has_key(nvar):
        interpretation[var] = False
        removeClausesWithLiteral(nvar, clauses, litclauses)

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
        removeClausesWithLiteral(var, clauses, litclauses)
        removeClausesWithLiteral(nvar, clauses, litclauses)
        
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