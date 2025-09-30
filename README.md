# 🧪 Data-Driven Exploration of AB<sub>2</sub>X<sub>4</sub> (X = O, S, Se, Te) Spinel Chemical Space

This repository contains the complete high-throughput screening (HTS) workflow, data, and code for identifying potentially synthesizable **AB<sub>2</sub>X<sub>4</sub>** spinel compounds. The framework integrates **materials databases**, **empirical heuristics**, and **machine learning predictions** to uncover novel, unexplored candidates.

---

## 🚀 Overview

Spinels are a versatile class of materials used in applications ranging from energy storage to catalysis. Structurally similar to MgAl<sub>2</sub>O<sub>4</sub>, they consist of A- and B-site cations occupying tetrahedral and octahedral sites, respectively, within a tightly packed cubic lattice of X anions, forming the **Fd3̅m** space group. Spinels also exhibit **cation disordering**, forming "normal" and "inverse" phases, which can be described using the **cation inversion parameter** _x_, where x ∈ [0, 1].

Despite their broad utility, much of the spinel chemical space remains unexplored. This project targets spinels formed from the first 83 elements with four anions: O, S, Se, and Te. A multi-stage HTS pipeline is developed to filter candidates through:

- ⚗️ **Chemical filtering** (valency, charge balance)
- ⚛️ **Thermodynamic filtering** (stability via _E_<sub>hull</sub>)
- 🤖 **Data-driven filtering** (via _CLscore_)

A key innovation is the introduction of the **Unified Crystal Likelihood Score**, or **_S_<sub>score</sub>**, which combines thermodynamic and data-driven metrics to rank compositions by their synthesizability. Dynamical stability is further verified through **phonon dispersion** analysis.

---

## 🧩 Workflow and Tools

We generate all possible spinel compositions using the first 83 elements and four anions (O, S, Se, Te). The screening workflow includes:

- 🧪 Chemical validity check using [**SMACT**](https://github.com/WMD-group/SMACT)
- ⚛️ Structural optimization with [**MACE-MP-0a**](https://github.com/ACEsuit/mace)
- 🧮 _E_<sub>hull</sub> calculation via [**Pymatgen**](https://github.com/materialsproject/pymatgen)
- 🤖 _CLscore_ prediction using [**Synthesizability-stoi-CGNF**](https://github.com/kaist-amsg/Synthesizability-stoi-CGNF)
- 📊 Unified crystal likelihood scoring (_S_<sub>score</sub>)
- 🧊 Phonon dispersion analysis via [**MatCalc**](https://github.com/materialsvirtuallab/matcalc)

All predictions are compared against known spinels from the [**Materials Project**](https://next-gen.materialsproject.org) and [**ICSD**](https://www.psds.ac.uk/icsd).

---

## 📊 Key Results

- 🔍 **55,112** total compositions (including inverse structures)
- ✅ **2,303** potentially synthesizable candidates
- 🧊 **12** dynamically stable structures among top 40
- ♻️ **66.9%** recovery of known oxide spinels

---

## 💻 Getting Started

Install dependencies via `pip`:

```bash```
`pip install numpy matplotlib seaborn pandas smact pymatgen mp-api mace-torch ase`

---
## 📘 Notebooks and Usage

You can directly run the screening using `3_screening.ipynb` — all required data is provided.

### 🧠 Jupyter Notebooks

| Notebook | Description |
|----------|-------------|
| `1_MP_ICSD_SMACT.ipynb` | Retrieves Materials Project entries, cleans ICSD data, and applies SMACT chemical validity filters. |
| `2_chemical_space_plot.ipynb` | Plots chemical space with known and valid spinel compositions from MP/ICSD and SMACT filters. |
| `3_screening.ipynb` | Performs the final screening using _E_<sub>hull</sub>, _CLscore_, and _S_<sub>score</sub> to identify top candidates. |

You can jump straight into `3_screening.ipynb` if you're only interested in exploring the filtered chemical space. All necessary data is included.

---

### 🛠️ Calculation Scripts

If you'd like to **reproduce the full workflow from scratch**, follow the steps below:

1. **SMACT filtering & MP data retrieval**  
   → `notebooks/1_MP_ICSD_SMACT.ipynb`

2. **Structure optimization with MACE**  
   → `calculation_scripts/MACE/MACE_calculation.py`

3. **_CLscore_ prediction using PUL model**  
   → `calculation_scripts/PUL_CLscore/PUL_data_preparation.ipynb`

4. **_E_<sub>hull</sub> calculation**  
   → `calculation_scripts/Ehull/Ehull_calculation.ipynb`

5. **Final filtering and ranking with _S_<sub>score</sub>**  
   → `notebooks/3_screening.ipynb`

> **Note**: ICSD data is manually curated due to licensing restrictions and is not publicly redistributed here.

To use this repo, simply start with installations of all the required packages using pip. However, if you prefer installing from the source code, please refer to their repository.
pip install numpy, matplotlib, seaborn, pandas, smact, pymatgen, mp-api, mace-torch, ase

This repo contains of three main notebook, 

1_MP_ICSD_SMACT.ipynb shows how to perform SMACT screening, data mining from MP, and data cleaning from ICSD, 
2_chemical_space_plot.ipynb shows how to plot chemical space of compositions allowed by SMACT with known data from MP and ICSD, and
3_screening.ipynb shows how to screen for candidates using _E_<sub>hull</sub>, _CLscore_, and _S_<sub>score</sub>.

All the required data has been provided so you don't need to run any calculations to replicate this work. You can directly jump to 3_screening.ipynb if you would like to perform chemical space screening of spinels. The idea for 1_MP_ICSD_SMACT.ipynb and 2_chemical_space_plot.ipynb is that you can perform quick SMACT screening for the chemically valid chemical space of any system. You only need to change the system in the scripts to your targeted one. More details are provided in the notebooks.

However, if you would like to run the calculations please refer to these scripts:

1) Start with SMACT screening and data mining from MP (ICSD data are manually downloaded so I don't have any script for that) using 1_MP_ICSD_SMACT.ipynb
2) Perform MACE calculations using calculation_scripts/MACE/MACE_calculation.py
3) Perform PUL calculations for _CLscore_ using calculation_scripts/PUL_CLscore/PUL_data_preparation.ipynb
4) Perform _E_<sub>hull</sub> calculations once MACE calculations are finished using calculation_scripts/Ehull/Ehull_calculation.ipynb
5) Combine all the results and perform data analysis using 3_screening.ipynb
