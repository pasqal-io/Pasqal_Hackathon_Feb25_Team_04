from pyscf import scf, gto, ao2mo
import numpy as np

def get_integrals(mol, mo_basis=False):
    #The kinetic energy term
    T = mol.intor('cint1e_kin_sph')
    #Nuclear Repulsion term
    V = mol.intor('cint1e_nuc_sph')
    #Exchange terms
    Fock = T + V
    v2e = mol.intor('cint2e_sph').reshape((nao,)*4)
    if mo_basis:
        #Running a scf procedure
        mf = scf.RHF(mol).run()
        #extracting useful quantities
        E_hf = mf.e_tot
        hf_mo_E = mf.mo_energy
        hf_mo_coeff = mf.mo_coeff
        #Changing the fock and 2 electron repulsion matrix for to be used with other codes
        Fock = np.einsum('ab,ac,cd->bd',hf_mo_coeff,Fock,hf_mo_coeff) 
        #oneelecint_mo[abs(oneelecint_mo) < 10**(-8)] = 0
        if 1:
            v2e = np.einsum('zs,wxyz->wxys',hf_mo_coeff,v2e) 
            v2e = np.einsum('yr,wxys->wxrs',hf_mo_coeff,v2e)
            v2e = np.einsum('xq,wxrs->wqrs',hf_mo_coeff,v2e)
            v2e = np.einsum('wp,wqrs->pqrs',hf_mo_coeff,v2e)
            #twoelecint_mo[abs(twoelecint_mo) < 10**(-8)] = 0
        else:
            v2e = ao2mo.incore.full(v2e, hf_mo_coeff)
        #v2e=np.swapaxes(v2e,1,2) #if you need to change notations (see integral notation chemists vs physicists)
    return Fock,v2e



#mol = gto.M('Li 0 0 0; H 0 0 1', basis = {'Li':'ccpvtz','H':'ccpvdz'},charge=0,spin=0)
mol = gto.M('H 0 0 0; H 0 0 1', basis = 'sto3g')#{'Li':'ccpvtz','H':'ccpvdz'},charge=0,spin=0)
nao=mol.nao_nr()
nelec=mol.nelectron;

get_integrals(mol, mo_basis=True)
