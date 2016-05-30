# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 13:56:26 2016

@author: Mark
"""

import pprint
import scipy
import numpy
import scipy.linalg   # SciPy Linear Algebra Library

AS = scipy.array([ [7, 3, -1, 2], [3, 8, 1, -4], [-1, 1, 4, -1], [2, -4, -1, 6] ])
AN = numpy.array([ [7, 3, -1, 2], [3, 8, 1, -4], [-1, 1, 4, -1], [2, -4, -1, 6] ])

## function
def LU_Decomp( matrix ):
    assert isinstance( matrix, numpy.ndarray )
    P, L, U = scipy.linalg.lu(matrix)      # Works with scipy and numpy arrays. 
    return P, L, U
     
#P, L, U = LU_Decomp(AS)

## check
#print '\nCheck if equal to A '
#pprint.pprint(numpy.dot(P,numpy.dot(L,U)))

#print 'A:'
#pprint.pprint(AN)

#print 'P:'
#pprint.pprint(P)

#print 'L:'
#pprint.pprint(L)

#print 'U:'
#pprint.pprint(U)

