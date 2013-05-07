FanSATstic
==========

This project is the solution given to a university's assignment.

First it was created for a local search SAT solvers competition.
But as we are seeing more algorithms these ones are being integrated to the original solver.



********************************
Algorithms and Program Arguments

                                 |
+ To specify the path to the cnf formula file
	
	-f/--file {FILE}

+ To specify the algorithm to solve the formula

	-a/--algorithm {gsat, gwsat, dp}

	The possible algorithms are:

		- gsat      [GSAT]
		- gwsat     [GWSAT]
		- dp        [Davis-Putnam]

+ To specify the variable selection heuristic

	-vsh/--vselection {most_often, most_equilibrated}

	This argument is only used by the following algorithms:

		- dp

+ To use a weighted version of the algorithms

	-w/--weighted

	This argument is only used by the following algorithms:

		- gsat
		- gwsat
