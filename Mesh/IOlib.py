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
#  def read_from_txt( fname ):
#try:
    #Open the file to read
fname = 'simple.msh'
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
        Cons = numpy.array([0, 0])
        for node in enodes:
            node.set_constraint(Cons)
    elif PhysicalGroup == 3 : # Right edge
        Force = numpy.array([10.0, 0.0])
        for node in enodes:
            node.set_forcecons(Force)





     
     
   # enodesIDs = numpy.array(linelist[1:],dtype=int)
    #enodes    = [ nodes[nodeIDs.index(enodesID)] for enodesID in enodesIDs ]
    #addElement(elems, elemID, enodes)
    
#        #Read the nodes
#        nodes   = []
#        nodeIDs = []
#        for inode in range( nnodes ):
#            linelist = fin.readline().strip().split()
#            nodeID   = int(linelist[0])
#            coord    = numpy.array(linelist[1:],dtype=float)
#            addNode(nodes, nodeID, coord)   
#            nodeIDs.append( nodeID )
#        
#        #Empty line
#        fin.readline()
#        
#        #Read the number of elements
#        linelist = fin.readline().strip().split()
#        assert linelist[0]=='NELEM'
#        nelems = int(linelist[1])
#        
#        #Read the elements
#        elems = []  
#        for ielem in range( nelems ):
#            linelist    = fin.readline().strip().split()
#            elemID    = int(linelist[0])
#            enodesIDs = numpy.array(linelist[1:],dtype=int)
#            enodes    = [ nodes[nodeIDs.index(enodesID)] for enodesID in enodesIDs ]
#            addElement(elems, elemID, enodes)
#            
#        #Empty line
#        fin.readline()
#        
#        #Read the number of boundary elements
#        linelist = fin.readline().strip().split()
#
#        assert linelist[0]=='NBELEM'
#        nbelems = int(linelist[1])
#        
#        #Read the elements
#        belems = []
#        for ibelem in range( nbelems ):
#            linelist    = fin.readline().strip().split()
#            belemID     = int(linelist[0])
#            benodesIDs  = numpy.array(linelist[1:],dtype=int)
#            benodes    = [ nodes[nodeIDs.index(benodesID)] for benodesID in benodesIDs ]
#            addBelement(belems, belemID, benodes)
#
#        #Empty line
#        fin.readline()
#        
#        #Read the number of boundary nodes
#        linelist = fin.readline().strip().split()
#        assert linelist[0]=='NBNODE'
#        nbnodes = int(linelist[1])
#        
#        #Read the elements
#        bnodes = []
#        for ibnode in range( nbnodes ):
#            linelist    = fin.readline().strip().split()
#            bnodeID     = int(linelist[0])
#            bnodes.append(bnodeID)
#        
#        #Empty line
#        fin.readline()
#        
#        #Read the number of constraints
#        linelist = fin.readline().strip().split()
#        assert linelist[0]=='CONS'
#        ncons = int(linelist[1])
#        
#        #Read and set the constraints
#        for icon in range( ncons ):
#            linelist = fin.readline().strip().split()
#            nodeID   = int(linelist[0])
#            cons     = numpy.array(linelist[1:],dtype=int)
#            nodes[nodeID].set_constraint(cons)
#            
#        #Empty line
#        fin.readline()
#        
#        #Read the number of displacement constraints 
#        linelist = fin.readline().strip().split()
#        assert linelist[0]=='DISP'
#        ndispcon = int(linelist[1])
#        
#        #Read and set the displacement constraints
#        displist = []
#        for icon in range( ndispcon ):
#            linelist = fin.readline().strip().split()
#            nodeID   = int(linelist[0])
#            disp     = numpy.array(linelist[1:],dtype=float)
#            nodes[nodeID].set_displacementcons(disp)
#            displist.append(nodeID)
#
#        mesh = Mesh( nodes, elems, belems, bnodes )

#except:
#    fin.close()

    #return mesh, displist
    