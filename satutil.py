# -*- coding: utf-8 -*-

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
    
