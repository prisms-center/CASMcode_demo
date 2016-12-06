from casm.project import Project, Selection, write_eci
from casm.learn import open_halloffame, open_input, checkhull, to_json
import pandas
import matplotlib.pyplot as plt

### Input files
casm_learn_input = 'fit_1_ga.json'
selection = 'all_lt_0p7'


### Get casm-learn input and data
#
# This assumes you've already run casm-learn and have results in a Hall Of Fame

# load casm-learn input
input = open_input(casm_learn_input)

# open casm-learn halloffame
hall = open_halloffame(input["halloffame_filename"])


### Check convex hull, store results in CASM project

# select ECI to use, get convex hull configurations and add pandas.DataFrame 
# attributes to hall[indiv_i]:
#  
#    "dft_gs" : DFT calculated ground states
#    "clex_gs" : predicted ground states
#    "gs_missing" : DFT ground states that are not predicted ground states
#    "gs_spurious" : Predicted ground states that are not DFT ground states
#    "uncalculated" : Predicted ground states and near ground states that have not been calculated
#    "below_hull" : All configurations predicted below the prediction of the DFT hull
#    "ranged_rms": root-mean-square error calculated for the subset of configurations
#      whose DFT formation energy lies within some range of the DFT convex hull.
#      Currently calculated for ranges 0.001, 0.005, 0.01, 0.05, 0.1, 0.5 eV/unit cell
#
indiv_i = 0
checkhull(input, hall, indices=[indiv_i])

proj = Project()

# make sure ECI are saved into CASM project
indiv = hall[indiv_i]
write_eci(proj, hall[0].eci, to_json(indiv_i, hall[indiv_i]))


### Get data for plotting

# query properties from CASM
sel = Selection(proj, selection, all=False)

comp_a = 'comp(a)'
is_calculated = 'is_calculated'
dft_Ef = 'formation_energy'
clex_Ef = 'clex(formation_energy)'
sel.query([comp_a, is_calculated, dft_Ef, clex_Ef])

# data is stored in a pandas.DataFrame
df = sel.data

# 'formation_energy' includes 'unknown' strings for configurations that have not
# been calculated.  Here we create a DataFrame including only calculated configs
# and enforce the datatype to be numeric
df_calc = df[df.loc[:,is_calculated] == 1].apply(pandas.to_numeric, errors='ignore')


### Generate plot

# to plot dft formation energy & hull
h0 = plt.scatter(df_calc[comp_a], df_calc[dft_Ef], facecolors='none', edgecolors='b', label='dft')
h0_hull = plt.plot(indiv.dft_gs[comp_a], indiv.dft_gs[dft_Ef], 'bo-', label='_nolegend_')

# to plot calculated configurations predicted Ef & predicted hull
h1 = plt.scatter(df_calc[comp_a], df_calc[clex_Ef], color='r', marker='.', label='clex')
h1_hull = plt.plot(indiv.clex_gs[comp_a], indiv.clex_gs[clex_Ef], 'r.-', label='_nolegend_')

# to plot all enumerated configurations predicted Ef
#h2 = plt.plot(df[comp_a], df[clex_Ef], 'r.', label='clex')
#h2_hull = plt.plot(indiv.clex_gs[comp_a], indiv.clex_gs[clex_Ef], 'r-', label='_nolegend_')

plt.xlabel(comp_a)
plt.ylabel('Formation energy (eV/unit cell)')

plt.legend()
plt.show()


