# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 17:44:14 2016

@author: Mark
"""

import numpy 

def addNode( nlist, ID, coord ):
    index = len(nlist)
    NewNode = Node(ID, coord, index)
    return nlist.append( NewNode )
    
def addElement( elist, ID, Enodes ):
    NewElement = Element(ID, StandardTriangle(), Enodes)
    return elist.append( NewElement )
    
def addBelement( belist, ID, Benodes ):
    NewBelement = Element(ID, StandardTruss(), Benodes)
    return belist.append( NewBelement )
       
#==============================================================================
    
class Node:
    
    ## Constructor
    #  @param ID    Node ID
    #  @param coord Node coordinate
    #  @param index Node index
    def __init__ ( self, ID, coord, index ):
        self.__ID = ID
        self.__index = index
        self.set_coordinate( coord )
        self.set_constraint( numpy.array([0 , 0]) )
    ## Get the Node ID
    def get_ID ( self ):
        return self.__ID
    
    ## Get the Node index    
    def get_index( self ):
        return self.__index
    
    ## Set the coordinate
    #  @param coord Node coordinate   
    def set_coordinate( self, coord ):
        assert isinstance( coord, numpy.ndarray )
        assert coord.ndim==1
        assert coord.dtype==float
        self.__coord = coord

    ## Get the Node coordinate
    def get_coordinate( self ):
        return self.__coord
        
    ## String function
    def __str__ ( self ):
        s  = 'Node ID           : %d\n' % self.get_ID()
        s += 'Node coordinates  : %s\n' % numpy.array_str(self.get_coordinate())
        s += 'Node index        : %d\n' % self.get_index()
        return s
    
    ## Set Constraint
    def set_constraint( self, cons ):
        assert isinstance( cons, numpy.ndarray )
        assert cons.ndim==1
        assert cons.dtype==int
        self.__cons = cons
        
    ## Get Constraint
    def get_constraint( self ):
        return self.__cons

    ## Set Constraint
    def set_forcecons( self, consF ):
        assert isinstance( consF, numpy.ndarray )
        assert consF.ndim==1
        assert consF.dtype==float
        self.__conF = consF

    ## Get Constraint
    def get_forcecons( self ):
        return self.__conF

#==============================================================================

class Element:

    ## Constructor
    #  @param ID     Element ID
    #  @param parent Standard/parent element
    #  @param nodes  List of finite element Nodes
    def __init__ ( self, ID, parent, nodes ):
        self.__ID     = ID
        self.__nodes  = nodes
        self.__parent = parent
        self.__nnodes = len(parent)
        assert len(parent)==len(nodes)

    ## Get element ID
    def get_ID(self):
        return self.__ID
    
    ## Get nodes
    def get_nodes( self ):
        return self.__nodes
        
    ## Get node IDs from element
    def get_node_IDs( self ):
        IDlist = []
        for node in self.__nodes:
            IDlist.append(node.get_ID())
        return IDlist     
            
    ## Get the number of nodes
    def get_nr_of_nodes ( self ):
        return self.__nnodes
        
    ## Iterator function
    def __iter__( self ):
        return iter(self.__nodes)

    ## Length function
    def __len__( self ):
        return self.get_nr_of_nodes()

    ## String function
    def __str__( self ):
        s  = 'Element %d with nodes: ' % self.__ID
        s += ', '.join(str(node) for node in self.__nodes)
        return s
        
    ## Get item function
    def __getitem__ ( self, index ):
        return self.__nodes[index]
        
    ## Get the jacobian
    #  @param  xi Local coordinate vector
    #  @return    Jacobian matrix
    def __get_jacobian ( self, xi ):
        coords          = self.get_coordinates()
        std_shapes_grad = self.__parent.get_shapes_gradient(xi)
        return coords.T.dot( std_shapes_grad )
        
    ## Get the integration scheme
    #  @param  name The type of integration scheme (e.g. 'gauss')
    #  @param  npts The number of integration points
    #  @return      Matrix of integration point coordinates
    #  @return      Vector of integration point weights
    def get_integration_scheme ( self, name, npts ):
        xis, ws = self.__parent.get_integration_scheme( name, npts )
        ws = numpy.array([w*numpy.linalg.det(self.__get_jacobian( xi )) for xi, w in zip(xis,ws)])
        return xis, ws
        
    ## Get the shape functions gradient
    #  @param  xi Local coordinate vector
    #  @return    Matrix of shape function gradients
    def get_shapes_gradient ( self, xi ):
        J_inv = numpy.linalg.inv( self.__get_jacobian( xi ) )
        std_shapes_grad = self.__parent.get_shapes_gradient(xi)
        return std_shapes_grad.dot( J_inv )
        
    ## Get the matrix of nodal coordinates
    def get_coordinates( self ):
        return numpy.array([node.get_coordinate() for node in self])
        
    ## Get the global coordinate
    #  @param  xi Local coordinate vector
    #  @return    Global coordinate vector
    def get_coordinate ( self, xi ):
        coords     = self.get_coordinates()
        std_shapes = self.__parent.get_shapes( xi )
        return coords.T.dot( std_shapes )
        
#==============================================================================
        
## Finite element mesh
class Mesh:
    ## Constructor
    #  @param nodes list of finite element nodes
    #  @param elems list of finite elements
    def __init__ ( self, nodes, elems, belems, bnodes ):
       self.__nodes = nodes
       self.__elems = elems
       self.__belems = belems
       self.__bnodes = bnodes
              
    ## Get a node
    #  @param ID Node ID
    def get_node ( self, ID ):
        for node in self.__nodes:
            if node.get_ID()==ID:
                return node
        raise RuntimeError( 'Node ID %d not found' % ID )
        
    ## Iterator function
    def __iter__ ( self ):
        return iter(self.__elems)

    ## Length function
    def __len__ ( self ):
        return len(self.__elems)

    ## String function
    def __str__ ( self ):
        s  = 'Number of nodes   : %d\n' % self.get_nr_of_nodes()
        s += 'Number of elements: %d\n' % len(self)
        return s
        
    def get_nodes( self ):
        return self.__nodes
        
    def get_elems( self ):
        return self.__elems

    def get_belems( self ):
        return self.__belems

    def get_bnodes( self ):
        bnodelist = []
        for i in self.__bnodes:
            bnodelist.append(self.get_node(i))
        return bnodelist

    ## Get the number of nodes
    def get_nr_of_nodes ( self ):
        return len(self.__nodes)

    ## Get the number of elements
    def get_nr_of_elements ( self ):
        return len(self.__elems)
        
    ## Get the number of boundary elements
    def get_nr_of_belements ( self ):
        return len(self.__belems)
        
    ## Get the number of boundary nodes
    def get_nr_of_bnodes ( self ):
        return len(self.__bnodes)

    def get_nr_of_constraints( self ):
        total = 0
        for node in self.__nodes:
            total += node.get_constraint().sum();
        return total

    def get_nr_of_nodes_with_constraints( self ):
        total = 0
        for node in self.__nodes:
            if node.get_constraint().sum()>0:
                total += 1
        return total
#==============================================================================
    
#  Linear triangle parent element with local coordinates (0,0), (1,0), (0,1)         
class StandardTriangle:
    
    ## Dictionary of integration schemes
    #
    #  See e.g. 'http://www.cs.rpi.edu/~flaherje/pdf/fea6.pdf' for details
    __ischemes = {
                   ('gauss',1 ) : ( numpy.array([[1./3.,1./3.]]),
                                    numpy.array([1./2.]) )
                 }

    ## Number of nodes
    __nnodes = 3

    ## Length function
    def __len__ ( self ):
        return self.get_nr_of_nodes()

    ## Get the number of nodes
    def get_nr_of_nodes ( self ):
        return self.__nnodes

    ## Get the shape functions
    #  @param  xi Local coordinate vector
    #  @return    Vector of shape functions
    def get_shapes ( self, xi ):
        return numpy.array([1-xi[0]-xi[1],xi[0],xi[1]])

    ## Get the shape functions gradient
    #  @param  xi Local coordinate vector
    #  @return    Matrix of shape function gradients
    def get_shapes_gradient ( self, xi ):
        return numpy.array([[-1.,-1.],
                            [ 1., 0.],
                            [ 0., 1.]])

    ## Get the integration scheme
    #  @param  name The type of integration scheme (e.g. 'gauss')
    #  @param  npts The number of integration points
    #  @return      Matrix of integration point coordinates
    #  @return      Vector of integration point weights
    def get_integration_scheme ( self, name, npts ):
        xis, ws = self.__ischemes[ (name,npts) ]
        return xis, ws

    def get_connections_scheme (self):
        return numpy.array([[ 0 , 1 ],
                           [ 1 , 2 ],
                           [ 2 , 0 ]])

#==============================================================================
    
#  Linear truss parent element with local coordinates (-1,0), (1,0)         
class StandardTruss:
    
    ## Dictionary of integration schemes
    #
    #  See e.g. 'http://www.cs.rpi.edu/~flaherje/pdf/fea6.pdf' for details
    __ischemes = {
                   ('gauss',1 ) : ( numpy.array([0.5]),
                                    numpy.array([1]) )
                 }

    ## Number of nodes
    __nnodes = 2

    ## Length function
    def __len__ ( self ):
        return self.get_nr_of_nodes()

    ## Get the number of nodes
    def get_nr_of_nodes ( self ):
        return self.__nnodes

    ## Get the shape functions
    #  @param  xi Local coordinate vector
    #  @return    Vector of shape functions
    def get_shapes ( self, xi ):
        return numpy.array([1-xi[0],xi[0]])

    ## Get the shape functions gradient
    #  @param  xi Local coordinate vector
    #  @return    Matrix of shape function gradients
    def get_shapes_gradient ( self, xi ):
        return numpy.array([[-1.],
                            [ 1.],])

    ## Get the integration scheme
    #  @param  name The type of integration scheme (e.g. 'gauss')
    #  @param  npts The number of integration points
    #  @return      Matrix of integration point coordinates
    #  @return      Vector of integration point weights
    def get_integration_scheme ( self, name, npts ):
        xis, ws = self.__ischemes[ (name,npts) ]
        return xis, ws

    def get_connections_scheme (self):
        return numpy.array([[ 0 , 1 ]])