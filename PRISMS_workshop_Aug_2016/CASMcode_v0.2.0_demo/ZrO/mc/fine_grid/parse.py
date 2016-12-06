import json
import pickle
from os.path import exists, join
import pandas

def read(base, col, data):
  index = 0
  while True:
    path = base + "." + str(index)
    
    if not exists(path):
      break
    
    ### open Monte Carlo results.json file
    with open(join(path, 'results.json'), 'r') as f:
      res = pandas.read_json(f)
    
    if base not in data:
      data[base] = []
    data[base].append(res[col])
    
    index += 1


data = dict()
col = ['<comp(a)>', 'param_chem_pot(a)', 'T', 'Beta', '<potential_energy>']
read("T_up", col, data)
read("T_down", col, data)
read("xi_up", col, data)
read("xi_down", col, data)

with open('../example_lte1/results.json','r') as f:
  lte_res = pandas.read_json(f)
data['lte'] = lte_res

with open('data.pkl','wb') as f:
  pickle.dump(data,f)
