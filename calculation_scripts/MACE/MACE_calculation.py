import re
import os
os.environ['MPLCONFIGDIR'] = os.getcwd() + "/configs/"
from pymatgen.core import Composition
from ase.io import read,write
from ase.optimize import FIRE
from typing import Optional
import numpy as np
from ase import Atoms
from ase.calculators.calculator import Calculator
from ase.optimize import FIRE
from mace.calculators import MACECalculator
from ase.filters import FrechetCellFilter
from datetime import datetime
import pandas as pd
import concurrent.futures as cfutures
from concurrent.futures import as_completed
from concurrent.futures import wait, FIRST_COMPLETED
import csv

##Setting up calculations for normal/inverse spinels with different anions
##Only edit area between the lines of hashes
################################Change the following variables according to your needs
type_spinels='normal'
# type_spinels='inverse'
type_anion = 0 ##Edit this to change the anion type 0=oxide, 1=sulfide, 2=selenide, 3=telluride
################################

type_anion_lists = ['oxide','sulfide','selenide','telluride']
type_anion_directories = ['1_Oxide','2_Sulfide','3_Selenide','4_Telluride']

##Generate POSCAR files for normal and inverse spinels
init_poscar=f'prototype_structures/POSCAR_{type_spinels}'
edit_poscar=f'prototype_structures/POSCAR_{type_spinels}_edit'

smact_elements=pd.read_csv(f'../../data/SMACT/smact_allowed_{type_anion_lists[type_anion]}_comps_low_poscar.csv',header=None)
smact_elements_list=smact_elements[0].tolist()

################################Edit this to change the range of your calculations
start_range=0
end_range=len(smact_elements_list)
################################

smact_poscar=smact_elements_list[start_range:end_range]

line_number_to_edit = 6

for i in range(len(smact_poscar)):
        new_text = smact_poscar[i]
        with open(init_poscar, 'r') as file:
            lines = file.readlines()
        lines[line_number_to_edit - 1] = new_text + '\n'
        with open(edit_poscar, 'w') as file:
            file.writelines(lines)
        os.system(f'cp {edit_poscar} {type_anion_directories[type_anion]}/1_initial_structure_dir/POSCAR_{type_spinels}_{type_anion_lists[type_anion]}_{i}')

start_datetime = datetime.now()
start_formatted_datetime = start_datetime.strftime("%A-%d-%m-%Y %H:%M:%S")
print("Calculation started at:", start_formatted_datetime)

## Run MACE calculations
################################Change this if you want to change to another model, this model can be downloaded from https://github.com/ACEsuit/mace-foundations/releases/download/mace_mp_0/2023-12-03-mace-128-L1_epoch-199.model
calc=MACECalculator(model_paths="2023-12-03-mace-128-L1_epoch-199.model", default_dtype="float64", device='cpu')
################################

def optimize_atoms(
    calc: Calculator,
    atoms: Atoms,
    i,
    max_steps: int = 600,
    fmax: float = 0.05,
) -> Optional[Atoms]:
    structure = atoms.copy()
    result = False

    force_conv = 'unchecked'
    _fmax = 'unchecked'

    structure = structure.copy()
    structure.calc = calc

    cell_filter = FrechetCellFilter(structure)
    result=FIRE(cell_filter, trajectory=f'{type_anion_directories[type_anion]}/3_traj_dir/optimization_{type_spinels}_{type_anion_lists[type_anion]}_{i}.traj', logfile=f'{type_anion_directories[type_anion]}/4_log_dir/optimization_{type_spinels}_{type_anion_lists[type_anion]}_{i}.log')
    result.run(fmax=fmax, steps=max_steps)

    final_energy = structure.get_potential_energy()
    final_cell_lengths_angles = structure.cell.cellpar()
    final_volume = structure.get_volume()
    num_steps = result.get_number_of_steps()
        
    if result:
        conv = 'pass'
    else:
        conv = 'fail'
       
    # Fail if the forces are too large
    forces = cell_filter.get_forces()
    _fmax = np.sqrt((forces**2).sum(axis=1).max())

    if _fmax > 1000:
        force_conv = 'fail'
    else:
        force_conv = 'pass'

    # Result settings    
    compositions_split = tuple(smact_poscar[i].split())
    compositions = ''
    if len(compositions_split) == 3:
        compositions = (compositions_split[0] + compositions_split[1] + '2' + compositions_split[2] + '4')
    elif len(compositions_split) == 2:
        compositions = (compositions_split[0] + '3' + compositions_split[1] + '4')

    final_energy = structure.get_potential_energy()
    final_cell_lengths_angles = structure.cell.cellpar()
    final_volume = structure.get_volume()
    num_steps = result.get_number_of_steps()
    write(f'{type_anion_directories[type_anion]}/2_final_structure_dir/CIF_{type_spinels}_{type_anion_lists[type_anion]}_{i}_final.cif', structure, format='cif')
    return (compositions, final_cell_lengths_angles[0], final_cell_lengths_angles[1], final_cell_lengths_angles[2], final_cell_lengths_angles[3], final_cell_lengths_angles[4], final_cell_lengths_angles[5], final_energy, final_volume, num_steps, conv, force_conv, _fmax)

# Define column names for the CSV
results_columns = [('Compositions', 'a', 'b', 'c', 'angle_a', 'angle_b', 'angle_c', 'energy', 'volume', 'steps','conv','force_conv','force')]

nprocs = 128
print('Running with '+ str(nprocs)+' processors')
with cfutures.ProcessPoolExecutor(max_workers=nprocs) as executor:
    futures = {executor.submit(optimize_atoms, calc, read(f'{type_anion_directories[type_anion]}/1_initial_structure_dir/POSCAR_{type_spinels}_{type_anion_lists[type_anion]}_{i}', format='vasp'), i): i for i in range(len(smact_poscar))}
    results = [future.result() for future in futures]

finish_datetime = datetime.now()
finish_formatted_datetime = finish_datetime.strftime("%A-%d-%m-%Y %H:%M:%S")
print("Calculation finished at:", finish_formatted_datetime)

for i in range(len(results)):
    results_columns.append(results[i])

df_results = pd.DataFrame(results_columns[1:], columns=results_columns[0])
df_results.to_csv(f'{type_anion_directories[type_anion]}/results_{type_spinels}_{type_anion_lists[type_anion]}.csv', index=False)
