from pyscf import gto, scf, mcscf

mol = gto.M(atom = ''' O 0 0 0; O 0 0 1''', basis='631g',spin=2) #2S
mf = scf.ROHF(mol)
mf.kernel()

mc = mcscf.CASSCF(mf, 6, 4)
mc.kernel()

#CASSCF energy = -149.447371969869
#CASCI E = -149.447371969869  E(CI) = -7.44878814091774  S^2 = 2.0000000
