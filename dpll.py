# -*- coding: utf-8 -*-

import satutil
import datautil

#
#
def solve(num_variables, clauses, selection_heuristic):
    """
    Uses the dpll algorithm to determine if the formula is satisfiable or 
    unsatisfiable
    
    Returns a tuple with the following formats:
        - If the formula is satisfiable
            (True, [None, truth_value1, truth_vaue2, ...] )
        - If the formula is unsatisfiable
            (False, frozenset() ) 
    """
    
    # Dictionary with clauses classified by literals
    litclauses = datautil.classifyClausesByLiteral(clauses)
    
    # Amount of times each clause appears in the formula. At the beginning only once
    ctimes = { c : 1 for c in clauses }

    # Generates list with variables to be assigned and initial interpretation
    variables = set()
    interpretation = [None]
    for v in xrange(1, num_variables+1):
        if litclauses.has_key(v) or litclauses.has_key(-v):
            variables.add(v)
            interpretation.append(None)
        else:
            interpretation.append(satutil.getRandomAssignation())
            
    return _solve(variables, clauses, ctimes, litclauses, interpretation, 
                  selection_heuristic)
    
    
#
#
def _solve(variables, clauses, ctimes, litclauses, interpretation, heuristic):
    """
    DPLL recursive implementation
    
    Performs the following steps:
        - Checks if a valid interpretation has been found
        - Unit Propagation
            - Restore data if empty clause was found
        - Checks if the formula has been solved by unit propagation
        - Pure Literal
        - Checks if the formula has been solved by pure literal
        
    """
    # Solved by previous assignation
    if not clauses:
        return (True, interpretation)
    
    # D.structures used to store unit propagation and pure literal changes
    used_vars = set()
    removed_clauses = set()
    modified_clauses = []
    
    # Performs unit propagation
    if unitPropagation(variables, clauses, ctimes, litclauses, interpretation, 
                       used_vars, removed_clauses, modified_clauses):        
    
        # Recover state of unitPropagation
        variables.update(used_vars)   
        undoClauseChanges(clauses, ctimes, litclauses, removed_clauses,
                          modified_clauses)
                          
        return (False, frozenset())
    
    # Solved by unitPropagation
    if not clauses:
        return (True, interpretation)
    
    # Propagate pure literals
    pureLiteral(variables, clauses, ctimes, litclauses, interpretation,
                used_vars, removed_clauses, modified_clauses)
                
    # Solved by pureLiteral
    if not clauses:
        return (True, interpretation)

    # select variable to explore
    var = heuristic(variables, litclauses)
    used_vars.add(var)
    variables.remove(var)
    
    # Recursive Call, internally recovers state between branches
    # if the return value of a branch is unsatisfiable
    res =  dpllBranch(var, variables, clauses, ctimes, litclauses,
                      interpretation, heuristic)
                     
    # Recover Unit Propagatin and Pure Literal changes
    if not res[0]:
        variables.update(used_vars)        
        undoClauseChanges(clauses, ctimes, litclauses, removed_clauses,
                          modified_clauses)
        
    return res   
    
                      
#
#
def unitPropagation(variables, clauses, ctimes, litclauses, interpretation,
                    used_vars, removed_clauses, modified_clauses):
    """
    Search for clauses with only one literal and then remove the unnecessary
    information
    
    This is an special version for DPLL that logs all the changes
    
    Returns True as soon as an emtpy clause is reached, False otherwise
    """
                        
    unit_lits = set([iter(c).next() for c in clauses if len(c) == 1])
    
    while unit_lits:
        lit = unit_lits.pop()
        
        removeClausesWithLiteral(lit, clauses, ctimes, litclauses,
                                 removed_clauses)
        
        # If removing the literal from the other clauses, appears an empty
        # clause then returns false
        if litclauses.has_key(-lit):
            if removeLiteralFromClauses(-lit, clauses, ctimes, litclauses,
                                        modified_clauses):
                return True
                
        # Remove te used variable
        var = abs(lit)
        variables.remove(var)
        used_vars.add(var)
        
        # Save interpretation
        interpretation[var] = lit > 0
        
        # Check if the last propagations generated more unit clauses        
        if not unit_lits:
            unit_lits = set([iter(c).next() for c in clauses if len(c) == 1])
            
    return False
    
#
#
def pureLiteral(variables, clauses, ctimes, litclauses, interpretation,
                used_vars, removed_clauses, modified_clauses):
    """
    Search for pure literals and then remove the unnecessary information and
    logs all the changes
    """
                    
    # Fill pure_lits with all the pure literals in the formula
    pure_lits = set()
    
    for v in variables:
        if litclauses.has_key(v) and not litclauses.has_key(-v):
            pure_lits.add(v)
        elif not litclauses.has_key(v) and litclauses.has_key(-v):
            pure_lits.add(-v)
            
    # Remove clauses with pure lits
    while pure_lits:
        pl = pure_lits.pop()
        var = abs(pl)
        variables.remove(var)
        used_vars.add(var)
        
        # Save interpretation
        interpretation[var] = pl > 0
        
        # This comprovation avoids an exception when a clause have more than
        # one pure literal (otherwise the algorithm tries to delete it twice)
        if litclauses.has_key(pl):
            removeClausesWithLiteral(pl, clauses, ctimes, litclauses,
                                     removed_clauses)
            
        # Check if the last propagations genereted more pure literals
        if not pure_lits:
            for v in variables:
                if litclauses.has_key(v) and not litclauses.has_key(-v):
                    pure_lits.add(v)
                elif not litclauses.has_key(v) and litclauses.has_key(-v):
                    pure_lits.add(-v)
            
#
#
def dpllBranch(var, variables, clauses, ctimes, litclauses, interpretation,
               heuristic):
    
    """
    Explore all the search space with var = True and var = False until
    a solution or empty clause are found
    """
    nvar = -var    
    br_removed_clauses = set()
    br_modified_clauses = []
        
    # Truth value for var = True
    interpretation[var] = True
    if not removeLiteralFromClauses(nvar, clauses, ctimes, litclauses,
                                    br_modified_clauses):
        removeClausesWithLiteral(var, clauses, ctimes, litclauses,
                                 br_removed_clauses)
        res = _solve(variables, clauses, ctimes, litclauses, interpretation,
                     heuristic)
                     
        # Solution found. Do not undo changes 
        if res[0]:
            return res
            
    undoClauseChanges(clauses, ctimes, litclauses, br_removed_clauses,
                      br_modified_clauses)
    
    br_modified_clauses = []
    br_removed_clauses.clear()
    
    # Truth value for var = False
    interpretation[var] = False
    if not removeLiteralFromClauses(var, clauses, ctimes, litclauses,
                                    br_modified_clauses):
        removeClausesWithLiteral(nvar, clauses, ctimes, litclauses,
                                 br_removed_clauses)
        res = _solve(variables, clauses, ctimes, litclauses, interpretation,
                     heuristic)
                     
        # Solution found. Do not undo changes
        if res[0]:
            return res
            
    undoClauseChanges(clauses, ctimes, litclauses, br_removed_clauses,
                      br_modified_clauses)
    
    # Both assignations have failed
    return (False, frozenset())
         
#
#
def removeClausesWithLiteral(lit, clauses, ctimes, litclauses,
                             removed_clauses):
    """
    Remove all the clauses with the specified literal and logs the changes
    """
    
    for clause in litclauses[lit]:
        # Record clause deletion
        removed_clauses.add( (clause, ctimes[clause]) )
        
        clauses.remove(clause)
        ctimes[clause] = 0
        
        # Remove the clause from literal's local sets
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
def removeLiteralFromClauses(lit, clauses, ctimes, litclauses,
                             modified_clauses):
    """
    Remove the specified literal from all the clauses it belongs to and
    logs the changes
    """
    for clause in litclauses[lit]:                
        nc = frozenset([x for x in clause if x != lit])
        
        if not nc:
            return True

        # Record clause modification
        modified_clauses.append( (nc, clause, ctimes[clause]) )

        # Delete clause
        clauses.remove(clause)        
        clauses.add(nc)
        
        # Update times
        ctimes[clause] = 0
        try:
            ctimes[nc] += 1
        except KeyError:
            ctimes[nc] = 1
        
        # Update clause on literal's local sets
        for l in nc:
            lset = litclauses[l]
            lset.remove(clause)
            lset.add(nc)
                
    del litclauses[lit]                
        
    return False  

#
#
def undoClauseChanges(clauses, ctimes, litclauses, removed_clauses, 
                modified_clauses):
    readdRemovedClauses(clauses, ctimes, litclauses, removed_clauses)
    undoModifiedClauses(clauses, ctimes, litclauses, modified_clauses)
    
#
#
def readdRemovedClauses(clauses, ctimes, litclauses, removed_clauses):
    """
    Add all the clauses removed on a previous call to removeClausesWithLiteral
    """
    for clause, t in removed_clauses:
        clauses.add(clause)
        ctimes[clause] = t
        
        for l in clause:
            if not litclauses.has_key(l):
                litclauses[l] = set()
            litclauses[l].add(clause)
            
#
#
def undoModifiedClauses(clauses, ctimes, litclauses, modified_clauses):
    """
    Undo all the modifications performed by removeLiteralFromClauses
    """
    for nclause, clause, t in reversed(modified_clauses):
        
        # Remove the current clause if only appears once
        ctimes[nclause] -= 1
        if ctimes[nclause] == 0:
            clauses.remove(nclause)
          
        # Add the old clause
        clauses.add(clause)
        ctimes[clause] = t
        
        for l in clause:
            # Add literal set of clauses and the old clause
            if not litclauses.has_key(l):
                litclauses[l] = set()
                litclauses[l].add(clause)
                
            # Remove the newest clause if necessary and add the old one
            else:
                lset = litclauses[l]
                if ctimes[nclause] == 0 and nclause in lset:
                    lset.remove(nclause)
                lset.add(clause)                   