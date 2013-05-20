# -*- coding: utf-8 -*-

import datautil
import satutil

#
#
def solve(num_variables, clauses, selection_heuristic):
    """
    Uses the dp algorithm to determine if the formula is satisfiable or 
    unsatisfiable
    
    Returns a tuple with the following formats:
        - If the formula is satisfiable
            (True, frozenset() )
        - If the formula is unsatisfiable
            (False, frozenset(<core_clause1>, <core_clause2>, ...) ) 
    """
    
    litclauses = datautil.classifyClausesByLiteral(clauses)
    variables = range(1, num_variables+1)
    reason = {} # Clause "parents"
        
    while variables:
        
        if unitPropagation(variables, clauses, litclauses, reason):
            return (False, generateCoreFromEmtpyClause(reason))

        # All clauses and variables wasted without finding the emtpy clause
        if not clauses or not variables:
            return (True, frozenset())
        
        # Select variable
        var = selection_heuristic(variables, litclauses)
        variables.remove(var)
        
        # Ignore variables that don't belong to any clause
        if not litclauses.has_key(var) and not litclauses.has_key(var):
            continue
        
        if resolution(var, clauses, litclauses, reason):
            return (False, generateCoreFromEmtpyClause(reason))
            
    return (True, frozenset())


#
#
def unitPropagation(variables, clauses, litclauses, reason):
    """
    Search for clauses with only one literal and then remove the unnecessary
    information
    
    This is an special version for DP that does not save the interpretation
    
    Returns True as soon as an emtpy clause is reached, False otherwise
    """
    # set of literals that belongs to a unit clause
    unit_lits = set([iter(c).next() for c in clauses if len(c) == 1])
    
    while unit_lits:
        lit = unit_lits.pop()
                        
        removeClausesWithLiteral(lit, clauses, litclauses)
        
        # If removing the literal appears an empty clause return false
        if litclauses.has_key(-lit):
            if removeUnitClause(-lit, clauses, litclauses, reason):
                return True
                
        # Variables are represented as possitive numbers
        alit = abs(lit)
        variables.remove(alit)
        
        # If all the previous unit literals have been removed check for possible
        # new unit lits
        if not unit_lits:
            unit_lits = set([iter(c).next() for c in clauses if len(c) == 1])
                
    return False    

#
#
def resolution(var, clauses, litclauses, reason):
    """
    Checks if the specified variable 'var' is a pure literal, if it is not
    then performs resolution and add to reason the 'parents' of the new
    clases

    Returns True if the empty clause is found, False otherwise
    """
    nvar = -var # Variable values are always possiive
    
    # Variable x only appears with one polarity (Pure literal)    
    if litclauses.has_key(var) and not litclauses.has_key(nvar):
        removeClausesWithLiteral(var, clauses, litclauses)
        
    elif not litclauses.has_key(var) and litclauses.has_key(nvar):
        removeClausesWithLiteral(nvar, clauses, litclauses)

    # Perform resolution with variable 'var'        
    else:
        for c in litclauses[var]:
            for n in litclauses[nvar]:
                resolvent = resolve(c, n, var)

                # Ignore tautologies
                if not satutil.isTautology(resolvent):

                    # Check if resolvent's reason has been initialized
                    if not reason.has_key(resolvent):
                        reason[resolvent] = set()
                    parents = reason[resolvent]
                    parents.add(c)
                    parents.add(n)
                
                    # If resolvent is the empty clause
                    if not resolvent:
                        return True


                    clauses.add(resolvent)
                    
                    # KeyError should not be raised otherwise there is an error
                    # in some part of the code
                    for lit in resolvent:
                        litclauses[lit].add(resolvent)
                    
        # Remove all the clauses with the literals x and -x
        removeClausesWithLiteral(var, clauses, litclauses)
        removeClausesWithLiteral(nvar, clauses, litclauses)
        
    return False
    
#
#
def resolve(c1, c2, var):
    """
    Resolution method with clauses c1 and c2 using the variable var
    """
    nl = [x for x in c1 if x != var]
    nl.extend( (x for x in c2 if x != -var) ) # Use a generator to save memory
    return frozenset(nl)
    
#
#
def removeClausesWithLiteral(lit, clauses, litclauses):
    """
    removeClausesWithLiteral(lit, clauses, litclauses)

    - lit: The literal to remove

    - clauses: A set filled with clauses (as a frozensets)

    - litclauses: A dictionary with a set of clauses for each literal    
    
    Removes all the clauses which contain the specified literal
    """
    # The exception KeyError should never happen, as long as the literal 
    # exists in the formula    
    for clause in litclauses[lit]:
        # The clause could have been removed previously, 
        # because it can be associated to another literal
        try:
            clauses.remove(clause)
        except KeyError:
            pass
        
        # Remove the clause from the literal's local sets
        for l in clause:
            if l != lit:
                lset = litclauses[l]
                lset.remove(clause)
                # If empty set for literal l remove its local set
                if not lset:
                    del litclauses[l]
    
    del litclauses[lit]
    
#
#
def removeUnitClause(lit, clauses, litclauses, reason):
    """
    removeUnitClause(lit, clauses, litclauses, reason)
    
    - lit: The literal to remove

    - clauses: A set filled with clauses (as frozensets)

    - litclauses: A dictionary with a set of clauses for each literal     
    
    - reason: Dictionary that will be filled with the parent clauses of
                                
    Removes the literal from the clauses to which it belongs
    
    Returns True if some of the reductions is the empty clause, False otherwise
    """
    parent_unit_caluse = frozenset([-lit])
      
    for clause in litclauses[lit]:
        # New clause without the literal
        nc = frozenset([x for x in clause if x != lit])
        
        # Check if nc's reason has been initialized
        if not reason.has_key(nc):
            reason[nc] = set()
        reason[nc].add(parent_unit_caluse)
        reason[nc].add(clause)
        
        # Empty clause found
        if not nc:
            return True

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
    
    return False

#
#
def generateCoreFromEmtpyClause(reason):
    """
    generateCoreFromEmptyClause(reason)

    Generates the core prove traversing the reason implication graph
    from the empty clause to the first clauses

    Returns a frozenset filled with the core clauses
    """
    empty_clause = frozenset()
    core = set()
    stack = list(reason[empty_clause])
    
    while stack:
        clause = stack.pop()

        try:
            for c in reason[clause]:
                stack.append(c)

        except KeyError:
            core.add(clause)

    return frozenset(core)




