#!/usr/bin/env python
import sys
from ase.io import read, write
from ase.cell import Cell
import numpy as np




def main():
    # Read the input xyz file from command line
    input_file = sys.argv[1]
    
    # Read the xyz file
    atoms = read(input_file)
    
    # Only keep the first 100 atoms
    atoms = atoms[:100]
    
    # Add cell information
    box = np.array([31.7900009155, 31.0900001526, 30.3899993896])
    atoms.set_cell(Cell(np.eye(3)*box))
    
    # Save the new xyz file
    output_file = "waterRemoved_xyz_file.xyz"
    write(output_file, atoms)
    

if __name__ == "__main__":
    main()
