#!/usr/bin/env python
import matplotlib.pyplot as plt
import pandas
from os.path import join, exists
import pickle

with open('data.pkl','rb') as f:
  data = pickle.load(f)

x_val = 'param_chem_pot(a)'
y_val = '<comp(a)>'

for i in range(len(data['T_up'])):
  
  plt.plot(data['xi_up'][i][x_val], data['xi_up'][i][y_val], 'bo-', label='increasing')
  plt.plot(data['xi_down'][i][x_val], data['xi_down'][i][y_val], 'rx-', label='decreasing')
  
  T = data['xi_up'][i]['T'][0]
  
  plt.title('Temperature: ' + str(T) + ' (K)')
  plt.xlabel(x_val)
  plt.ylabel(y_val)
  plt.legend(loc=0)
  plt.ylim([0.0,0.2])
  plt.show()

