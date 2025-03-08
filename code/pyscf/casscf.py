from pyscf import gto, scf, mcscf
import numpy as np
import random
mol = gto.M(atom = ''' O 0 0 0; O 0 0 1''', basis='631g',spin=2) #2S
mf = scf.UHF(mol)
mf.kernel()

#print(mf.make_rdm1s())
mc = mcscf.CASSCF(mf, 6, (5,3))
#mc.kernel()
#print(mc.make_rdm1()>0)
#rdm1 = ((np.array([mc.make_rdm1()>0])-0.5)*2)[0]
#print(mc.mo_coeff)
#rdm1 = ((np.array([mc.mo_coeff>0])-0.5)*2)[0]
rdm1s = mc.make_rdm1s()
print(rdm1s[0].shape)
#CASSCF energy = -149.447371969869
#CASCI E = -149.447371969869  E(CI) = -7.44878814091774  S^2 = 2.0000000
