# -*- coding: utf-8 -*-


def resolve(c1, c2, var):
    """
    Resolution method with clauses c1 and c2 using the variable var
    """
    new = frozenset([x for x in c1 if x != var])
    new = new.union(set([x for x in c2 if x != -var]))
    return new
    
    
def solve(num_variables, litclauses):
    """
    Solve the given formula using the DP algorithm
    
    --- TEMPORAL ---
    Returns False if the formula is Unsatisfiable and True if it is Satisfiable
    """
    
    visited = set()    
    
    for x in xrange(1, num_variables + 1):
        # Avoid reading clausules that only contains visited literals
        visited.add(x)
        visited.add(-x)
        
        try:
            for c in litclauses[x]:
                try:
                    for n in litclauses[-x]:
                        resolvent = resolve(c, n, x)
                    
                        if not resolvent:
                            return False
                        
                        for lit in resolvent:
                            if lit not in visited:
                                if not litclauses.has_key(lit):
                                    litclauses[lit] = set()
                                
                                litclauses[lit].add(resolvent)
                
                except KeyError:
                    pass
                
            # Delete track record of clauses with the variable x
            del litclauses[x]
            
        except KeyError:
            pass
        
        # The -x variable is deleted here in case the acces to the x variable
        # raises an exception
        try:
            # Delete track record of clauses with the variable -x
            del litclauses[-x]
        except KeyError:
            pass
        
        return True