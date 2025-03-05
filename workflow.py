# function to run the entire workflow

import pyscf
#import pulser
import random
#import molecule_to_adjacency
#import adjacency_to_map 
#import map_to_circuit
#import hamiltonian_generator

#class pyscf2pulser(kernel, mol, norb_act, nelec_act, spin = 0, ):

def mol2mf(mol):
#you probably don't need to run this thing for the system to work.
    mf=pyscf.scf.ROHF(mol)
    return mf

def mf2adjacency(mf):
# could probably be replaced by something better than the absolute value of overlap, but it's a first pass.
# also thinking spin separated 2rdm, but that scales exponentially with the size of active space. 
# could do lasscf with various active spaces. 
    overlap_matrix = mf.mol.intor("int1e_ovlp")
    return np.abs(overlap_matrix)

def adjacency2distances(adjacency_matrix):
#from a matrix M_ij, R_ij and {R_i} where M is adjacency matrix, R_ij is distance between i and j, and R_i is the vector position of R_i. M_ij = C/R_ij^6
#assume reasonable values for R_ij when M_ij = 0
    pass

def distances2circuit(orbital_map):
#given {R_i}, place them on a 2d map that is used in a quantum circuit layout
    pass

def hamiltonian_generator(mf, adjacency):
    pass

def kernel(mol):
    mf = mol2mf(mol)
    overlap = mf2adjacency(mf)
    print(overlap)

mol = pyscf.gto.M(atom= "H 0 0 0; H 0 0 1",basis='ccpvdz',verbose=3)
print(mol.nao)
mf = mol2mf(mol)
overlap = mf2adjacency(mf)
print(overlap)
