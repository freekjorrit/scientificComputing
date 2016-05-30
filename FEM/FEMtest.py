import numpy

from FEM  import *
from IOlib import *
from MeshDat import *

# Parameters
TSTEP=0.01;
TOTITERATIONS=100

E=70e9
nu=0.33
b=2.5e-10
L_e=6*b
B=10e6
tau_nuc = 50e6
stdtau_nuc = 0.2*tau_nuc
L_nuc = 125*b
t_nuc = 0.01e-6
tau_obs = 150e6
SPS=80*b
SPS_init_source=16e-6
SPS_init_obstacle=8e-6
parameter=Parameter(E, nu, b, L_e, B, tau_nuc, stdtau_nuc, L_nuc, t_nuc, tau_obs, SPS, SPS_init_source, SPS_init_obstacle)

mesh = read_from_txt('../Mesh/simple.msh')
Force = numpy.array([[5, 1e10, 0]])
#mesh.get_node(1).set_constraint(numpy.array([1, 1]))
#mesh.get_node(4).set_constraint(numpy.array([1, 0]))
#mesh.get_node(8).set_constraint(numpy.array([1, 0]))
K = getK(mesh,parameter)
F = getF(mesh,Force)
U = solveSys(mesh,F,K)
sig=get_FEM_stresses(mesh,U,parameter)
nodeslist=mesh.get_nodes()
#for node in nodeslist:
#    print node.get_constraint()
for x in ([0,1,2,3,4,5,6,7, 8]):
    print U[2*x],'\t\t',U[2*x+1]