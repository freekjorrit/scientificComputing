# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 12:57:28 2016

@author:
"""
import numpy 
from MeshDat import *
from StressDat import *
from DislocDat import *
from LU_Mark import *
from class_parameter import *


# returns the externam forces on the nodes due to the stress caused by dislocations
def getBoundryForce(F,mesh):

    belems = mesh.get_belems()
    for belem in belems:
        nodes = belem.get_nodes()
        length = abs(numpy.linalg.norm((nodes[0].get_coordinate()-nodes[0].get_coordinate())))

        n = 1/length * numpy.array((nodes[0].get_coordinate()-nodes[0].get_coordinate()))
        n[0:2]=[n[1],-n[0]]
        sig = numpy.zeros((2,2)) #get stresses in boundry element
        Fint = numpy.linalg.norm(sig.dot(n))

        for node in belem:
            F[2*node.get_ID():2*node.get_ID()+1]=Fint*length/2
    return F


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
             node_ID[count1] = node.get_ID()
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

            F[2*node.get_ID()] += fe[2*count3]
            F[2*node.get_ID()+1] += fe[2*count3+1]
            count3 += 1
    return F

# rewrites the KU=F to retrieve a solvable system.
def solveSys(mesh,F,K):
    nr_of_nodes_w_cons = mesh.get_nr_of_nodes_with_constraints()
    cons = numpy.zeros((nr_of_nodes_w_cons,3))
    consDis = numpy.zeros((nr_of_nodes_w_cons,3))
    nodes = mesh.get_nodes()
    c=0

    #temporary prescribed displacement, must be replaced with timestep * velocity
    for node in nodes:
        if node.get_constraint().sum()>0:
            cons[c,0:]=[node.get_ID(), node.get_constraint()[0],node.get_constraint()[1]]
            consDis[c,0:]=[node.get_ID(), 0.001*node.get_displacementcons()[0],0.001*node.get_displacementcons()[1]]
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
        if cons[row,c.__mod__(2)+1] == 1:
            cci=0
            for cc in range (2*nnodes):
                row2= numpy.where(cons[:,0] == cc//2)[0]
                if row2.size == 0 or cons[row2,cc.__mod__(2)+1] == 0:
                    f[cci]-=K[cc,c]*consDis[row,c.__mod__(2)+1]
                    cci+=1

    #LU, solve and replace the known displacements

    P, L, U = LU_Decomp(Kn)
    y=numpy.linalg.solve(L,f)
    x=numpy.linalg.solve(U,y)
    u=numpy.zeros(2*nnodes)

    # restore the full U, so add the prescribed displacements.
    ci=0
    for c in range(2*nnodes):
        row = numpy.where(cons[:,0] == c//2)[0]
        if row.size == 0 or cons[row,c.__mod__(2)+1] == 0:
            u[c]=x[c-ci]
        if cons[row,c.__mod__(2)+1] == 1:
            u[c]=consDis[row,c.__mod__(2)+1]
            ci+=1
    return u


# Assamble K from the separate Ke parts
def getK(mesh,param):
    C = param.E/((1+param.nu)*(1-2*param.nu))*numpy.array([[1-param.nu, param.nu, 0],
                                     [param.nu, 1-param.nu, 0],
                                     [0, 0, (1-2*param.nu)/2]])
    nnodes=mesh.get_nr_of_nodes()
    K = numpy.zeros( (2*nnodes,)*2 )

    for element in mesh:
        Ke = numpy.zeros( (2*len(element),)*2 )
        xis, ws = element.get_integration_scheme( 'gauss', 1 )

        #create Ke with the weight functions
        for xi, w in zip( xis, ws ):
            GradN = element.get_shapes_gradient( xi )

            GradN2d = numpy.zeros((3,2*len(element)))
            for inode in range(0,len(element)):
                GradN2d[0,0+2*inode] = GradN[inode,0]
                GradN2d[1,1+2*inode] = GradN[inode,1]
                GradN2d[2,0+2*inode] = GradN[inode,1]
                GradN2d[2,1+2*inode] = GradN[inode,0]
            Ke +=  w * numpy.dot( numpy.dot( GradN2d.T, C ),GradN2d)
        counti = 0
        ## put the values of Ke in K at the node positions
        for nodei in element:
            countj = 0
            for nodej in element:
                for i1 in [0,1]:
                    for i2 in [0,1]:
                        K[2*nodei.get_ID()+i1,2*nodej.get_ID()+i2] += Ke[2*counti+i1,2*countj+i2]
                countj += 1
            counti += 1
    #symmetry check
    if ((K.round(1) == K.round(1).T).all()):
        print 'K is symmetric'
    else:
        print 'K is unsymmetric'
    return K

#returns a array of stresses in all elements in [xx yy xy]
def get_FEM_stresses(mesh,U,param):
    C = param.E/((1+param.nu)*(1-2*param.nu))*numpy.array([[1-param.nu, param.nu, 0],
                                     [param.nu, 1-param.nu, 0],
                                     [0, 0, (1-2*param.nu)/2]])
    siglist = numpy.zeros((mesh.get_nr_of_elements(),3))
    for element in mesh:
        xis, ws = element.get_integration_scheme( 'gauss', 1 )
        sig = 0
        q=numpy.zeros((6,1))
        qi=0
        for node in element:
            id=node.get_ID()
            q[2*qi]=U[2*id]
            q[2*qi+1]=U[2*id+1]
            qi+=1
        for xi, w in zip( xis, ws ):
            GradN = element.get_shapes_gradient( xi )
            GradN2d = numpy.zeros((3,2*len(element)))
            for inode in range(0,len(element)):
                GradN2d[0,0+2*inode] = GradN[inode,0]
                GradN2d[1,1+2*inode] = GradN[inode,1]
                GradN2d[2,0+2*inode] = GradN[inode,1]
                GradN2d[2,1+2*inode] = GradN[inode,0]
            sig += w* numpy.dot( numpy.dot( C , GradN2d),q)
        siglist[element.get_ID(),:]=sig.T
    return siglist

def get_shapes ( xi ):
    return numpy.array([1-xi[0]-xi[1],xi[0],xi[1]])
