# -*- coding: utf-8 -*-

from random import choice

#
#
def RandomInterpretation(num_vars):
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
def IsClauseSatisfied(clause, interpretation):
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
def Satisfies(clauses, interpretation):
    """
    Satisfies(interpretation: [boolean]): boolean

    Check if an interpretation satisfies this formula
    """
    for clause in clauses:
        if not IsClauseSatisfied(clause, interpretation):
            return False
    return True

#
#
def NumSatisfiedClauses(clauses, interpretation):
    """
    NumSatisfiedClauses(clauses: [], interpretation: [boolean]): int

    Count all the satisfied clauses with the given interpretation
    """
    return sum(1 for c in clauses if IsClauseSatisfied(c, interpretation))

#
#
def NumSatisfiedWeightedClauses(clauses, interpretation, weights):
    """
    NumSatisfiedClauses(clauses: [], interpretation: [boolean],
                                                     weights: {clause:int}): int

    When a clause is satisfied increments the weight of that clause
    """
    return sum(weights[c] for c in clauses \
                                        if IsClauseSatisfied(c, interpretation))

#
#
def IncrementUnsatWeights(clauses, interpretation, weights):
    for c in clauses:
        if not IsClauseSatisfied(c, interpretation):
            weights[c] += 1
            
#
#
def NumSatisfiedLiterals(clause, interpretation):
    
    satlits = 0
    
    for lit in clause:
        var = abs(lit)
        if (interpretation[var] and lit > 0) or \
            (not interpretation[var] and lit < 0):
            satlits += 1
            
    return satlits
            
        