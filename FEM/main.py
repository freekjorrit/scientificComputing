## @package main
#  This file is used to run the script and call al functions

import numpy
from FEM  import *
from IOlib import *
from MeshDat import *
from output import *


E=70e9
nu=0.33

parameter=Parameter(E, nu)

mesh = read_from_txt('../Mesh/MultiHole.msh')

Force = 1e5

dis_force = Distribute_Force(mesh,Force)

K = getK(mesh,parameter)
F = getF(mesh,dis_force)

U = solveSys(mesh,F,K)
sig=get_FEM_stresses(mesh,U,parameter)

plot_solution( mesh,'output', 'output',U,sig)
