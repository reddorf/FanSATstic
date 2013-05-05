# -*- coding: utf-8 -*

import sys

#
#
def parseCNFLocalSearch(fname):
    """
    Parses the specified dimacs cnf file
    
    Returns: 
        - num_variables: Number of variables
        
        - clauses: All the clauses into a set of frozensets
        
        - litclauses: A tuple that contains all the clauses  where appears the
                      variable x and it's negate -x sorted by the variable 'name'.
                      The clauses are stored into frozensets
          
          For example to traverse all the clauses where appears the variable 
          2 and -2, simply do:
              
              for clause in litclauses[2]:
                  ... Lots of good code ...
          
    """
    num_vars = 0
    litclauses = None
    clauses = set()

    cnf_file = open(fname, 'r')    
    
    try:
        for nline, line in enumerate(cnf_file):
            lvalues = line.strip().split()
            
            if not lvalues or lvalues[0] == 'c':
                continue
            
            elif    lvalues[0] == 'p':
                if lvalues[1] != 'cnf':
                    raise SyntaxError('Invalid format identifier "%s".'
                                % (lvalues[1]) )
                            
                num_vars = int(lvalues[2])
                #num_clauses = int(lvalues[3])                
                litclauses = [[] for i in xrange(num_vars+1)] #range [1, num_vars]
                
            else:
                values = map(int, lvalues)                    
                clause = set()
                
                for lit in values:
                    if lit == 0:
                        if clause not in clauses:                        
                        
                            clause = frozenset(clause)
                            clauses.add( clause )
                                                        
                            for l in clause:
                                alit = abs(l)
                                litclauses[alit].append(clause)
                        else:
                            print 'Repeated'
                        clause = None # Check line ends with 0
                        
                    else:
                        clause.add(lit)

                        if lit < -num_vars or lit > num_vars:
                            raise SyntaxError('Invalid literal %d '
                                ', it must be in range [1, %d].'
                                % (lit, num_vars) )

                if clause:
                    raise SyntaxError('Not found the trailing 0')
                
    except SyntaxError, e:
        sys.stderr.write('Error parsing file "%s" (%d): %s\n' % 
                                    (fname, nline, str(e)) )
        raise e
        
    #clauses = set(clauses)
    litclauses = tuple(litclauses)
    
    return num_vars, clauses, litclauses


#
#
def parseCNFSystematicSearch(fname):
    """
    Parses the specified dimacs cnf file
    
    Returns: 
        - num_variables: Number of variables
                
        - litclauses: A dictionary that contains all the clauses where
                      appears the variable x (not -x)
                      
          For example to traverse all the clauses where appears the variable 
          2, simply do:
              
              for clause in litclauses[2]:
                  ... Lots of good code ...
                  
          And for traverse all the clauses where appears the variable -2, do:
              
              for clause in litclauses[-2]:
                  ... Lots of good code ...
          
    """
    num_vars = 0
    litclauses = {}

    cnf_file = open(fname, 'r')    
    
    try:
        for nline, line in enumerate(cnf_file):
            lvalues = line.strip().split()
            
            if not lvalues or lvalues[0] == 'c':
                continue
            
            elif    lvalues[0] == 'p':
                if lvalues[1] != 'cnf':
                    raise SyntaxError('Invalid format identifier "%s".'
                                % (lvalues[1]) )
                            
                num_vars = int(lvalues[2])
                #num_clauses = int(lvalues[3])                

            # Parse clause
            else:
                values = map(int, lvalues)
                clause = set()

                for lit in values:
                    
                    if lit == 0:           
                        
                        clause = frozenset(clause)                        
                        
                        for l in clause:
                           if not litclauses.has_key(l):
                               litclauses[l] = set()
                           
                           litclauses[l].add(clause)                       
                        
                        clause = None # Check line ends with 0

                    else:
                        clause.add(lit)

                        if lit < -num_vars or lit > num_vars:
                            raise SyntaxError('Invalid literal %d '
                                ', it must be in range [1, %d].'
                                % (lit, num_vars) )

                if clause:
                    raise SyntaxError('Error not found the trailing 0')

    except SyntaxError, e:
        sys.stderr.write('Error parsing file "%s" (%d): %s\n' % 
                                    (fname, nline, str(e)) )

        raise e
        
    return num_vars, litclauses