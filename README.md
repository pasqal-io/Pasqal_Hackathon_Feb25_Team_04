# quaNtumFix

Patching electronic structure methods with analog quantum computing.

Dependencies - [pyscf](https://github.com/pyscf/pyscf/tree/master/pyscf)

Installing pyscf
```
pip install pyscf
```

pyscf can also be built from source code, but for our usage, just pip installing it should be sufficient.

Workflow
1. Initialize a molecule in pyscf.
- mol = gto.M(atom = )
2. Generate electron repulsion integrals.
3. Hartree Fock can be done to provide a good initial guess for a multireference method.
4. Setup a multireference calculation
5. Get Hamiltonian from pyscf
6. Define your basis
7. Translate basis into quantum computing language
8. Basis transform the Hamiltonian
9. Adiabatically evolve Hamiltonian on quantum computer


The work is in progress.
