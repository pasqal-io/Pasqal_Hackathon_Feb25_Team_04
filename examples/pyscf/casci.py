from pyscf import gto, scf, mcscf

mol = gto.M(atom = ''' O 0 0 0; O 0 0 1''', basis='631g',spin=2) #2S
mf = scf.ROHF(mol)
mf.kernel()

mc = mcscf.CASCI(mf, 6, 4)
mc.kernel()

#CASCI E = -149.427624064998  E(CI) = -5.95678950845220  S^2 = 2.0000000
#notice how energy is higher than CASSCF - because there is no orbital optimization. 
#2/20/25 - Maybe we can stick to CASCI only because it's a single CI problem not requring orbital optimization that is more classical (but GPUs can make it really fast)
