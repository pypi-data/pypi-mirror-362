
# Elemental abundances. Taken from chemcomp/helpers/units/chemistry_const.py
import numpy as np

OH_init_abu = 4.9e-4  # O/H abundance, solar value
CH_init_abu = 2.69e-4  # C/H abundance, solar value
SiH_init_abu = 3.24e-5  # Si/H adundance, solar value
FeH_init_abu = 3.16e-5  # Fe/H adundance, solar value
SH_init_abu = 1.32e-5  # S/H adundance, solar value
MgH_init_abu = 3.98e-5  # Mg/H adundance, solar value
HeH_init_abu = 0.085 
AlH_init_abu = 2.82e-6
TiH_init_abu = 8.91e-8
KH_init_abu = 1.07e-7
NaH_init_abu = 1.74e-6
NH_init_abu = 6.76e-5
VH_init_abu = 8.59e-9

# array of species names. Taken from chemcomp/helpers/analysis_helper.py
element_array = ["C_elem", "O", "Fe", "S", "Mg", "Si", "Na", "K", "N", "Al", "Ti", "V", "H", "He"]
molecule_array = [ 
    "rest",
    "CO",
    "N2",
    "CH4",
    "CO2",
    "NH3",
    "trapped_CO_water",
    "trapped_CO2_water",
    "H2S",
    "H2O",
    "Fe3O4",
    "C",
    "FeS",
    "NaAlSi3O8",
    "KAlSi3O8",
    "Mg2SiO4",
    "Fe2O3",
    "VO",
    "MgSiO3",
    "Al2O3",
    "TiO",
]

iceline_names = [
                "CO & N2",
                "CH4",
                "CO2",
                "NH3",
                "H2O &\nH2S",
                "Fe3O4",
                "C grains",
                "FeS",
                "NaAlSi3O8",
                "KAlSi3O8",
                "Mg2SiO4",
                "Fe2O3",
                "VO",
                "MgSiO3",
                "Al2O3",
                "TiO",
            ]

# Used to skip over trapped molecules
iceline_molecules_and_temps = { 
    "CO" : 20,
    "N2" : 20,
    "CH4" : 30,
    "CO2": 70,
    "NH3": 90,
    "Trapped CO": 130,
    "Trapped CO2": 130,
    "H2S" : 150,
    "H2O" : 150,
    "Fe3O4" : 371,
    "C" : 631,
    "FeS" : 704,
    "NaAlSi3O8" : 958,
    "KAlSi3O8" : 1006,
    "Mg2SiO4": 1354,
    "Fe2O3" : 1357,
    "VO" : 1423,
    "MgSiO3" : 1500,
    "Al2O3" : 1653,
    "TiO" : 2000
}

iceline_temperatures = [20, 20, 30, 70, 90, 130, 130, 150, 150, 371, 631, 704, 958, 1006, 1354, 1357, 1423, 1500, 1653, 2000]

# Masses
MassO = 16.0
MassH = 1.0
MassFe = 56.0
MassMg = 24.3
MassSi = 28.0
MassS = 32.0
MassHe = 4.0
MassTi = 47.867
MassAl = 27
MassK = 39.0983
MassNa = 23
MassN = 14
MassV = 50.9415
MassC = 12.0  # C in terms of H

#   Masses in terms of H (atomic unit)
MassCO                = MassC + MassO  # 28.0   # CO mass in terms of H
MassTrapped_CO_in_H2O = MassC + MassO           # CO trapped in water
MassCH4 = MassC + 4 * MassH  # CH4 in terms of H
MassCO2                = MassC + 2 * MassO      # CO2 in terms of H
MassTrapped_CO2_in_H2O = MassC + 2 * MassO      # CO2 trapping in water
MassH2O = MassO + 2 * MassH  # H20 in terms of H

MassFe2O3 = 2 * MassFe + 3 * MassO
MassFe3O4 = 3 * MassFe + 4 * MassO
MassFeS = MassFe + MassS
MassMgSiO3 = MassMg + MassSi + 3 * MassO  # MgSiO3 in terms of H
MassMg2SiO4 = 2 * MassMg + MassSi + 4 * MassO  # MgSiO3 in terms of H
MassNH3 = 3 * MassH + MassN
MassN2 = 2 * MassN
MassH2S = 2 * MassH + MassS
MassNaAlSi3O8 = MassNa + MassAl + 3 * MassSi + 8 * MassO
MassKAlSi3O8 = MassK + MassAl + 3 * MassSi + 8 * MassO
MassTiO = MassTi + MassO
MassAl2O3 = 2 * MassAl + 3 * MassO
MassVO = MassV + MassO

mass_array = np.array(
    [
        MassCO,
        MassN2,
        MassCH4,
        MassCO2,
        MassNH3,
        MassTrapped_CO_in_H2O,     # Trapped CO
        MassTrapped_CO2_in_H2O,    # Trapped CO2
        MassH2S,
        MassH2O,
        MassFe3O4,
        MassC,
        MassFeS,
        MassNaAlSi3O8,
        MassKAlSi3O8,
        MassMg2SiO4,
        MassFe2O3,
        MassVO,
        MassMgSiO3,
        MassAl2O3,
        MassTiO
    ]
)
