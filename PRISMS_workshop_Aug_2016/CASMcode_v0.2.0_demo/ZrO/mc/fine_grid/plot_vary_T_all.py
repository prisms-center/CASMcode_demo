#!/usr/bin/env python
import matplotlib.pyplot as plt
import pandas
from os.path import join, exists
import pickle

with open('data.pkl','rb') as f:
  data = pickle.load(f)

x_val = '<comp(a)>'
y_val = 'T'

for i in range(len(data['T_up'])):
  
  plt.plot(data['T_up'][i][x_val], data['T_up'][i][y_val], 'bo-')
  plt.plot(data['T_down'][i][x_val], data['T_down'][i][y_val], 'rx-')
  
  
xi_min = data['T_up'][0]['param_chem_pot(a)'][0]
xi_max = data['T_up'][-1]['param_chem_pot(a)'][0]
  
plt.title('param_chem_pot(a): ' + str(xi_min) + ':' + str(xi_max) + ' (eV/unitcell)')
plt.xlabel(x_val)
plt.ylabel(y_val)
plt.ylim([200.,1000.])
plt.show()
