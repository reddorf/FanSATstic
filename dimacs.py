# -*- coding: utf-8 -*-

import sys

#
#
def ParseCNF(fname, outformat=list):

    num_vars = 0
    #num_clauses = 0
    litclauses = None
    clauses = []

    cnf_file = open(fname, 'r')    
    
    try:
        for nline, line in enumerate(cnf_file):
            lvalues = line.strip().split()
            
            if not lvalues or lvalues[0] == 'c':
                continue
            
            elif    lvalues[0] == 'p':
                if lvalues[1] != 'cnf':
                    raise Exception('Invalid format identifier "%s".'
                                % (lvalues[1]) )
                            
                num_vars = int(lvalues[2])
                #num_clauses = int(lvalues[3])                
                litclauses = [[] for i in xrange(num_vars+1)] #range [1, num_vars]
                
            else:
                values = map(int, lvalues)                    
                clause = []
                
                for lit in values:
                    if lit == 0:
                        if outformat != list:
                            clause = outformat(clause)
                        clauses.append( clause )
                                                    
                        for l in clause:
                            alit = abs(l)
                            litclauses[alit].append(clause)
                            
                        clause = None # Check line ends with 0
                        
                    else:
                        clause.append(lit)

                        if lit < -num_vars or lit > num_vars:
                            raise Exception('Invalid literal %d '
                                ', it must be in range [1, %d].'
                                % (lit, num_vars) )

                if clause:
                    raise Exception('Error not found the trailing 0')
                
    except Exception, e:
        sys.stderr.write('Error parsing file "%s" (%d): %s\n' % 
                                    (fname, nline, str(e)) )
        raise e
        
    if outformat != list:
        clauses = outformat(clauses)
        litclauses = tuple(litclauses)
    
    return num_vars, clauses, litclauses

    