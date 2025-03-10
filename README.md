# Pasqal_Hackathon_Feb25_Team_04
quaNtumFix
Patching electronic structure methods with analog quantum computing.

Dependencies - [pyscf](https://github.com/pyscf/pyscf/tree/master/pyscf)

Installing pyscf
```
pip install pyscf
```

Code adaptations(XBK and other functions and code) from the paper below and github(https://github.com/jcopenh/Quantum-Chemistry-with-Annealers).
```
J. Copenhaver, A. Wasserman, and B. Wehefritz-Kaufmann. “Using Quantum Annealers to Calculate Ground State 
    Properties of Molecules,” (2020), arXiv:2009.10779v2 [quant-ph].
```

pyscf can also be built from source code, but for our usage, just pip installing it should be sufficient.



Workflow
1. Initialize a molecule in pyscf.
2. Generate electron repulsion integrals.
3. Hartree Fock can be done to provide a good initial guess for a multireference method.
4. Setup a multireference calculation
5. Get Hamiltonian from pyscf
6. Define your basis
7. Translate basis into quantum computing language
8. Basis transform the Hamiltonian
9. Adiabatically evolve Hamiltonian on quantum computer


The work is in progress.
