# -*- coding: utf-8 -*-
#
# This file contains functions used by some systematic search algorithms
#

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
def removeLiteralFromClauses(lit, clauses, litclauses):
    """
    removeLiteralFromClauses(lit, clauses, litclauses)
    
    - lit: The literal to remove

    - clauses: A set filled with clauses (as a frozensets)

    - litclauses: A dictionary with a set of clauses for each literal     
    
    Removes the literal from the clauses to which it belongs
    
    Returns False if some of the reductions is the empty clause, True otherwise
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