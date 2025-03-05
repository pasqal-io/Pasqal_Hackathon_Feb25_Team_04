from pyscf import scf, gto

# Define a molecule that you want to work on
mol = gto.M(atom= 'H 0.0 0.0 0.0; H 1.0 0.0 0.0', basis='631g')


mf = scf.HF(mol)

mf.kernel()
#expected result: converged SCF energy = -1.09480796286051"
