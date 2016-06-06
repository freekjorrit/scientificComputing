import numpy
from FEM  import *
from IOlib import *
from MeshDat import *
from output import *


E=70e9
nu=0.33
parameter=Parameter(E, nu)

mesh = read_from_txt('../Mesh/SingleHole_Circle.msh')

Force = -1e10

dis_force = Distribute_Force(mesh,Force)

#mesh.get_node(1).set_constraint(numpy.array([1, 1]))
#mesh.get_node(4).set_constraint(numpy.array([1, 0]))
#mesh.get_node(8).set_constraint(numpy.array([1, 0]))
K = getK(mesh,parameter)
F = getF(mesh,dis_force)

U = solveSys(mesh,F,K)
sig=get_FEM_stresses(mesh,U,parameter)

plot_solution( mesh,'output', 'output',U,sig)
