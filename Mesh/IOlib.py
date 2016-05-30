# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 17:53:24 2016

@author: Mark
"""

import numpy 

from MeshDat import * 

## Mesh file reader
#
#  @param  fname Name of the mesh file
#  @return       Finite element mesh
#  @return       Indices of constrained degrees of freedom
def read_from_txt( fname ):
    try:
        #Open the file to read
        #fname = 'simple.msh'
        fin = open( fname )
        
        # this skips the $Physical names section
        line     = fin.readline()
        line     = fin.readline()
        line     = fin.readline()
        line     = fin.readline()
        line     = fin.readline()
        line     = fin.readline()
        line     = fin.readline()
        line     = fin.readline()
        line     = fin.readline()
        line     = fin.readline()
        
        #Read the number of nodes
        line     = fin.readline()
        linelist = line.strip().split()
        assert linelist[0] =='$Nodes'
        line     = fin.readline()
        nnodes = int(line)
        
        nodes   = []
        nodeIDs = []
        for inode in range( nnodes ):
            linelist = fin.readline().strip().split()
            nodeID   = int(linelist[0])
            coord    = numpy.array(linelist[1:3],dtype=float)
            addNode(nodes, nodeID, coord)   
            nodeIDs.append( nodeID )
            
        line     = fin.readline()
        
        #Read the number of elements
        line     = fin.readline()
        linelist = line.strip().split()
        assert linelist[0] =='$Elements'
        line     = fin.readline()
        nelems   = int(line)
        
        elems = []  
        belems = []
        LSnodes = []
        RSnodes = []
        for ielem in range( nelems ):
            linelist    = fin.readline().strip().split()
            elemID    = int(linelist[0])    # Possibly obsolete since all elements are grouped together by gmsh 
            enodesIDs = numpy.array(linelist[5:],dtype=int)
            enodes    = [ nodes[nodeIDs.index(enodesID)] for enodesID in enodesIDs ]
            ElementType = int(linelist[1])
            if ElementType == 1 :
                addBelement(belems, elemID, enodes)
            elif ElementType == 2 :
                addElement(elems, elemID, enodes)
                
            PhysicalGroup = int(linelist[3])    
            if PhysicalGroup == 2 : # Left edge
                Cons = numpy.array([1, 0])
                for node in enodes:
                    node.set_constraint(Cons)
                    LSnodes.append( node.get_ID() )
            elif PhysicalGroup == 3 : # Right edge
                Force = numpy.array([10.0, 0.0])
                for node in enodes:
                    node.set_forcecons(Force)
                    RSnodes.append( node.get_ID() )
        
        LSnodes = list(set(LSnodes)) # Remove duplicates, contains node IDs with an arbitrary order
        RSnodes = list(set(RSnodes))
        
        nodes[nodeIDs.index(0)].setconstraint = numpy.array([1, 1]) # Fix node 1 at (0,0).
                
        mesh = Mesh( nodes, elems, belems, LSnodes, RSnodes )
    
    except:
        fin.close()

    return mesh
