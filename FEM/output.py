## @package post_proc
#  This module contains the functions used for creating the VTK files

## Create VTK file
#
#  @param mesh          Finite element mesh
#  @param position      Solution vector
#  @param outfile       number of the output file
import numpy
def plot_solution( mesh,outfile, outfolder,U,sig):


    # Create output folder
    create_folder(outfolder)

    #create or empty output file and print vtk headers
    output = open(outfolder+'/post_proc_'+str(outfile).zfill(3)+'.vtk','w+')
    output.write('# vtk DataFile Version 2.0 \nDiscrete Dislocations \nASCII \n\n')

    # Plot Nodes
    nrNodes=mesh.get_nr_of_nodes()
    nodes_list=mesh.get_nodes()
    output.write('DATASET UNSTRUCTURED_GRID \nPOINTS '+str(nrNodes)+' float\n')
    for c in range(nrNodes):
        output.write(' '.join(map(str,nodes_list[c].get_coordinate()+[U[2*c],U[2*c+1]])))
        output.write(' 0.0\n')



    # Plot Elements
    nrElements=mesh.get_nr_of_elements()
    output.write('\nCELLS '+str(nrElements)+' '+str(nrElements*4)+'\n')
    for ele in mesh:
        elenodes=[]
        for node in ele:
            elenodes.append(node.get_index())
        output.write('3 ')
        output.write(' '.join(map(str,elenodes)))
        output.write('\n')

    # output Celltypes (every cell is a triangular element)
    output.write('\nCELL_TYPES '+str(nrElements)+'\n')
    for ele in mesh:
        output.write('5\n')


    # Plot stresses in cells
    output.write('\nCELL_DATA '+str(nrElements)+' \nSCALARS stress FLOAT \nLOOKUP_TABLE default\n')
    for c in range(nrElements):
        #output.write(str(nodes_list[c].get_stress_n()))
        output.write(vonMises(sig[c,:]))
        output.write('\n')

    #plot displacements in nodes
    output.write('\nPOINT_DATA '+str(nrNodes)+' \nSCALARS displacement FLOAT \nLOOKUP_TABLE default\n')
    for c in range(nrNodes):
        #output.write(str(nodes_list[c].get_stress_n()))
        output.write(str(numpy.linalg.norm(numpy.array([U[2*c], U[2*c+1]]))))
        output.write('\n')

    output.close()
    print 'File written to '+outfolder+'/post_proc_'+str(outfile).zfill(3)+'.vtk'

# Funtction to create Folder if it does not exist already
import os
def create_folder(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

# Calculate Von Mises stress on elememts
def vonMises(la):
    stress = numpy.sqrt((((la[0]-la[1])/2)**2)+la[2]**2)
    return str(stress)