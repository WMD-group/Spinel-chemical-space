# Data-Driven Exploration of AB<sub>2</sub>X<sub>4</sub> (X = O, S, Se, Te) Spinel Chemical Space

This repository contains the complete high-throughput screening (HTS) workflow, data, and code for identifying potentially synthesizable **AB<sub>2</sub>X<sub>4</sub>** spinel compounds. The framework integrates **materials databases**, **empirical heuristics**, and **machine learning predictions** to uncover novel, unexplored candidates.

---

## Overview

Spinels are a versatile class of materials used in applications ranging from energy storage to catalysis. Their crystal structures are similar to the mineral MgAl<sub>2</sub>O<sub>4</sub>, where the A- and B-site cations fill the tetrahedral and octahedral sites, respectively, within a tightly packed cubic structure of X anions, resulting in the space group Fd3̅m. They also possess cation disordering behavior where A and B cations can exchange their positions, forming either "normal" or "inverse" phases. This behavior can be explained using the cation inversion parameter (_x_), where x ∈ [0,1] corresponds to the degree of inversion from fully normal to fully and inverse spinel structures.

However, much of their chemical space remains underexplored. This project aims to explore spinel chemical space for potentially synthesisable compounds within the first 83 elements in the periodic table. We focus our investigation on oxide and chalcogen (sulfides, selenides, and tellurides) spinels. To tackle this vast design space, we developed a high-throughput screening (HTS) framework by combining several computational tools that systematically filters candidates through three main filtering stages:

- **Chemical filtering** (charge neutrality, electronegativity balance)
- **Thermodynamic filtering** (_E_<sub>hull</sub>)
- **Data-driven filtering** (_CLscore_)

A key feature of this work is the introduction of a new unified crystal likelihood metric, the 'super score' (_S_<sub>score</sub>), which combines thermodynamic filter (_E_<sub>hull</sub>) with data-driven filter (CLscore). This allows for more robust candidate ranking across thousands of compositions.

---

## Workflow and Tools

The screening workflow and tools includes:

- Chemical validity check using [**SMACT**](https://github.com/WMD-group/SMACT)
- Structural optimization with [**MACE-MP-0a**](https://github.com/ACEsuit/mace)
- _E_<sub>hull</sub> calculation via [**Pymatgen**](https://github.com/materialsproject/pymatgen)
- _CLscore_ prediction using [**Synthesizability-stoi-CGNF**](https://github.com/kaist-amsg/Synthesizability-stoi-CGNF)
- Unified crystal likelihood scoring (_S_<sub>score</sub>)
- Phonon dispersion analysis via [**MatCalc**](https://github.com/materialsvirtuallab/matcalc) using [**MACE-MP-0a**](https://github.com/ACEsuit/mace)

We begin by generating all possible spinel compositions composed of the first 83 elements in the periodic table and four anions (O, S, Se, and Te). These compositions are first filtered using SMACT for chemically valid spinel compounds and pass through structural optimisation using MACE-MP-0a. Pymatgen package is then used to calculate _E_<sub>hull</sub> using energy from MACE-MP-0a. Synthesizability-stoi-CGNF model is adopted to further refine the screening through a metric called CLscore. Both E<sub>hull</sub> and CLscore are combined to introduce a single unified metric, _S_<sub>score</sub> to quantify crytal likelihood of a compound based on two different perspectives. To determine preferred configurations between normal or inverse, configuration with lower _E_<sub>hull</sub> is chosen as the representative of the composition. To validate our _S_<sub>score</sub>, we compare our results with known spinels on [Materials Project (MP)](https://next-gen.materialsproject.org) and [Inorganic Crystal Structure Database (ICSD)](https://www.psds.ac.uk/icsd). Furthermore, phonon dispersion calculations are carried out on the top 10 candidates, ranked by _S_<sub>score</sub>, for each anion type to confirm the dynamical stability of the structures.

---

## Getting Started

To use this repo, simply start with installations of all the required packages using `pip`.

`pip install numpy matplotlib seaborn pandas smact pymatgen mp-api mace-torch ase`

---
## Notebooks and Usage

This repo contains of three main notebook, 

| Notebook | Description |
|----------|-------------|
| `1_MP_ICSD_SMACT.ipynb` | Retrieves Materials Project entries, cleans ICSD data, and applies SMACT chemical validity filters. |
| `2_chemical_space_plot.ipynb` | Plots chemical space with known and valid spinel compositions from MP/ICSD and SMACT filters. |
| `3_screening.ipynb` | Performs the final screening using _E_<sub>hull</sub>, _CLscore_, and _S_<sub>score</sub> to identify top candidates, and plots. |

You can jump straight into `3_screening.ipynb` if you're only interested in exploring the filtered chemical space. All necessary data is already included. Furthermore, if you would like to explore different chemical system, you can change system in `1_MP_ICSD_SMACT.ipynb` to the targeted system and plot with `2_chemical_space_plot.ipynb`.

---

### ⚙️ Calculation Scripts

To reproduce the full workflow from scratch, follow the steps below:

1. **Chemical filtering and MP data retrieval**  
   → `1_MP_ICSD_SMACT.ipynb`  
   Performs SMACT-based chemical validation and extracts relevant entries from the Materials Project.  
   *(Note: ICSD data must be downloaded and processed manually due to licensing restrictions.)*

2. **Structure optimization using MACE**  
   → `calculation_scripts/MACE/MACE_calculation.py`  
   Optimizes spinel structures using the MACE-MP-0a model.

3. **_CLscore_ prediction via Positive-Unlabeled Learning (PUL)**  
   → `calculation_scripts/PUL_CLscore/PUL_data_preparation.ipynb`  
   Prepares input for the Synthesizability-stoi-CGNF model.  
   > *The PUL model cannot currently be installed via `pip` or imported directly into Jupyter notebooks. Instead, it must be cloned and executed from its own repository. Follow the instructions in the [Synthesizability-stoi-CGNF repository](https://github.com/kaist-amsg/Synthesizability-stoi-CGNF) to run the calculations and then bring the results back into this workflow.*

4. **Thermodynamic stability via _E_<sub>hull</sub>**  
   → `calculation_scripts/Ehull/Ehull_calculation.ipynb`  
   Calculates the _E_<sub>hull</sub> using formation energies from MACE.

5. **Final filtering and ranking with _S_<sub>score</sub>**  
   → `3_screening.ipynb`  
   Combines _E_<sub>hull</sub> and _CLscore_ into _S_<sub>score</sub> to identify the promising candidates.
