## @package FEM
#  This module contains the functions used for the FEM.

import numpy
from MeshDat import *
from class_parameter import *
import scipy.sparse.linalg

## Distribute the Force over the nodes on the righthand side
#
#  @param  mesh This is a MeshDat.Mesh()
#  @param  Force Force on the nodes on the righthand side
#  @return       Distributed force on nodes
def Distribute_Force(mesh,Force):
    
    nnodes = len(mesh.get_RSnodes())
    c = 0
    f = Force / (nnodes-1)
    dis_force = numpy.zeros((nnodes,3))
    
    for node in mesh.get_RSnodes():
        if c<2:
        
            dis_force[c] = numpy.array([node.get_index(),f/2,0])
            
        else:
            
            dis_force[c] = numpy.array([node.get_index(),f,0])
        
        c+=1
        
    return dis_force

## Limit F to f where the entries of K in KU=F are known
#
#  @param  mesh This is a MeshDat.Mesh()
#  @param  Force Distributed force on nodes
#  @return       Limited F
def getF(mesh,Force):
    nnodes=mesh.get_nr_of_nodes()
    ff = numpy.zeros( (nnodes,2) )
    for iforce in range(len(Force)):
        ff[(Force[iforce,0]),0] = Force[iforce,1]
        ff[(Force[iforce,0]),1] = Force[iforce,2]
    F =  numpy.zeros( (2*nnodes,1) )
    for element in mesh:
         fe = numpy.zeros( 2*len(element) )

         node_ID = numpy.zeros(len(element))
         count1 = 0
         for node in element:
             node_ID[count1] = node.get_index()
             count1 += 1
         count2 = 0
         xis, ws = element.get_integration_scheme( 'gauss', 1 )
         for xi, w in zip( xis, ws ):                    #get Ke for each element
             N = get_shapes(xi)
             N2d = numpy.zeros((2,2*len(element)))
             for inode in range(0,len(element)):
                 N2d[0,0+2*inode] = N[inode]
                 N2d[1,1+2*inode] = N[inode]
             fe += w * ff[(node_ID[count2],)].dot(N2d)
             count2 += 1
         count3 = 0
         for node in element:

            F[2*node.get_index()] += fe[2*count3]
            F[2*node.get_index()+1] += fe[2*count3+1]
            count3 += 1
    for x in range(len(ff)):
        F[2*x]=ff[x,0]
        F[2*x+1]=ff[x,1]
    return F

## Rewrite K to Kn (rows with known U are removed) and solve the linear system
#
#  @param  mesh This is a MeshDat.Mesh()
#  @param  F Limited Force Distribution
#  @param  K Stiffness Matrix
#  @return Displacement U
def solveSys(mesh,F,K):
    nr_of_nodes_w_cons = mesh.get_nr_of_nodes_with_constraints()
    cons = numpy.zeros((nr_of_nodes_w_cons,3))
    consDis = numpy.zeros((nr_of_nodes_w_cons,3))
    nodes = mesh.get_nodes()
    c=0

    #read constraints
    for node in nodes:
        if node.get_constraint().sum()>0:
            cons[c,0:]=[node.get_index(), node.get_constraint()[0],node.get_constraint()[1]]
            consDis[c,0:]=[node.get_index(), 0,0]
            c+=1
    #limit F to f. The values at f where the position of u is prescribed or fixed are pulled out
    nnodes = mesh.get_nr_of_nodes()
    boundryLen=numpy.sum(cons[:,1:])

    Kn=numpy.zeros((2*nnodes-boundryLen,2*nnodes-boundryLen))
    f=numpy.zeros(2*nnodes-boundryLen)
    ci=0
    for c in range(2*nnodes):
        row = numpy.where(cons[:,0] == c//2)[0]
        if row.size == 0 or cons[row,c.__mod__(2)+1] == 0:
            f[ci]=F[c]
            ci+=1

    # remove the rows and columns where u is known (prescribed), put them in the righthand side
    ci=0
    for c in range(2*nnodes):
        row = numpy.where(cons[:,0] == c//2)[0]
        if row.size == 0 or cons[row,c.__mod__(2)+1] == 0:
            cci=0
            for cc in range(2*nnodes):
                row2= numpy.where(cons[:,0] == cc//2)[0]
                if row2.size == 0 or cons[row2,cc.__mod__(2)+1] == 0:
                    Kn[ci,cci]=K[c,cc]
                    cci+=1
            ci+=1
        else:
            cci=0
            for cc in range (2*nnodes):
                row2= numpy.where(cons[:,0] == cc//2)[0]
                if row2.size == 0 or cons[row2,cc.__mod__(2)+1] == 0:
                    f[cci]-=K[cc,c]*consDis[row,c.__mod__(2)+1]
                    cci+=1

    #solve and replace the known displacements
    u=numpy.zeros(2*nnodes)

    sKn = scipy.sparse.csr_matrix(Kn)    
    
    sx = scipy.sparse.linalg.spsolve(sKn,f)

    # restore the full U, so add the prescribed displacements.
    ci=0
    for c in range(2*nnodes):
        row = numpy.where(cons[:,0] == c//2)[0]
        if row.size == 0 or cons[row,c.__mod__(2)+1] == 0:
            u[c]=sx[c-ci]
        if cons[row,c.__mod__(2)+1] == 1:
            u[c]=consDis[row,c.__mod__(2)+1]
            ci+=1
    return u


## Make stiffness matrix K from all separate Ke from the elements
#
#  @param  mesh This is a MeshDat.Mesh()
#  @param  param This is a class_parameter.Parameter()
#  @return Stifness K
def getK(mesh,param):
    C = param.E/((1-param.nu**2))*numpy.array([[1, param.nu, 0],
                                     [param.nu, 1, 0],
                                     [0, 0, (1-param.nu)/2]])
    nnodes=mesh.get_nr_of_nodes()
    K = numpy.zeros( (2*nnodes,)*2 )
    for element in mesh:
        Ke = numpy.zeros( (2*len(element),)*2 )
        xi, w = element.get_integration_scheme( 'gauss', 1 )

        #create Ke with the weight functions

        GradN = element.get_shapes_gradient( xi )

        GradN2d = numpy.zeros((3,2*len(element)))
        for inode in range(0,len(element)):
            GradN2d[0,0+2*inode] = GradN[inode,0]
            GradN2d[1,1+2*inode] = GradN[inode,1]
            GradN2d[2,0+2*inode] = GradN[inode,1]
            GradN2d[2,1+2*inode] = GradN[inode,0]
        Ke =  w * numpy.dot( numpy.dot( GradN2d.T, C ),GradN2d)
        counti = 0
        ## put the values of Ke in K at the node positions
        for nodei in element:
            countj = 0
            for nodej in element:
                for i1 in [0,1]:
                    for i2 in [0,1]:
                        K[2*nodei.get_index() +i1,2*nodej.get_index()+i2] += Ke[2*counti+i1,2*countj+i2]
                countj += 1
            counti += 1
    #symmetry check
    if ((K.round(3) != K.round(3).T).all()):
        print 'K is unsymmetric'
    return K



## returns a array of stresses in all elements in [xx yy xy]
#
#  @param  mesh This is a MeshDat.Mesh()
#  @param  U Displacement of nodes
#  @param  param This is a class_parameter.Parameter()
#  @return Stiffness K
def get_FEM_stresses(mesh,U,param):
    C = param.E/((1-param.nu**2))*numpy.array([[1, param.nu, 0],
                                     [param.nu, 1, 0],
                                     [0, 0, (1-param.nu)/2]])
    siglist = numpy.zeros((mesh.get_nr_of_elements(),3))
    elec=0
    for element in mesh:
        xi, w = element.get_integration_scheme( 'gauss', 1 )
        sig = 0
        q=numpy.zeros((6,1))
        qi=0
        for node in element:
            id=node.get_index()
            q[2*qi]=U[2*id]
            q[2*qi+1]=U[2*id+1]
            qi+=1

        GradN = element.get_shapes_gradient( xi )
        GradN2d = numpy.zeros((3,2*len(element)))
        for inode in range(0,len(element)):
            GradN2d[0,0+2*inode] = GradN[inode,0]
            GradN2d[1,1+2*inode] = GradN[inode,1]
            GradN2d[2,0+2*inode] = GradN[inode,1]
            GradN2d[2,1+2*inode] = GradN[inode,0]
        sig = w * numpy.dot( numpy.dot( C , GradN2d),q)
        siglist[elec,:]=sig.T
        elec+=1
    return siglist

def get_shapes ( xi ):
    return numpy.array([1-xi[0]-xi[1],xi[0],xi[1]])

