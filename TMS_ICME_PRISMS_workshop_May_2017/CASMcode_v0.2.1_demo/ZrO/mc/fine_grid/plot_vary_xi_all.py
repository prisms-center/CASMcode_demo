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
  
  plt.plot(data['xi_up'][i][x_val], data['xi_up'][i][y_val], 'bo')
  plt.plot(data['xi_down'][i][x_val], data['xi_down'][i][y_val], 'rx')
  
plt.xlabel(x_val)
plt.ylabel(y_val)
plt.show()

