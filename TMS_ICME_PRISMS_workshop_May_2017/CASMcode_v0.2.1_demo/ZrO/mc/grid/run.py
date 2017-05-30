import subprocess
import json
import os
import numpy as np
import copy
from casm.project import Project
import pbs

print """
Running a grid of Monte Carlo calculations
  (This may take a while)

"""


# Grid space to run Monte Carlo calculations (min, max, delta)
T_grid = (200, 1000, 100)
xi_grid = (-2.2, -1.6, 0.05)

d = {
  "mode" : "incremental",
  "dependent_runs" : True, 
  "motif" : {
    "configname" : "restricted_auto",
  },
  "initial_conditions" : {
    "param_chem_pot" : {
      "a" : -3.00
    },
    "temperature" : 1000.0,
    "tolerance" : 0.01
  },
  "final_conditions" : {
    "param_chem_pot" : {
      "a" : -3.00
    },
    "temperature" : 200.0,
    "tolerance" : 0.01
  },
  "incremental_conditions" : {
    "param_chem_pot" : {
      "a" : 0.0
    },
    "temperature" : -100.0,
    "tolerance" : 0.01
  }
}

proj = None

# For submission on personal computer...
def monte_cmd(input):
  global proj
  if proj is None:
    proj = Project()
  stdout, stderr, returncode = proj.command('monte -s input.json')
  print stdout

# For submission on PRISMS cluster...
#
#def monte_cmd(input):
#  jobname = os.path.basename(os.getcwd())
#  
#  cmd = """
#source ~/privatemodules/casm
#casm monte -s input.json
#"""
#  
#  job = pbs.PrismsDebugJob(name = jobname,
#                           nodes = "1",
#                           ppn = "1",
#                           walltime = "6:00:00",
#                           pmem = "3800mb",
#                           exetime = None,
#                           message = "a",
#                           email = None,
#                           command = cmd,
#                           auto = False).submit()
  
  
def submit_T_up(T_grid, xi_grid):
  index = 0
  for xi in np.arange(*xi_grid):
    path = "T_up." + str(index)
    
    tinput = copy.deepcopy(input)
    tinput['driver'] = d
    tinput['driver']['initial_conditions']['temperature'] = T_grid[0]
    tinput['driver']['final_conditions']['temperature'] = T_grid[1]
    tinput['driver']['incremental_conditions']['temperature'] = T_grid[2]
    
    tinput['driver']['initial_conditions']['param_chem_pot']['a'] = xi
    tinput['driver']['final_conditions']['param_chem_pot']['a'] = xi
    tinput['driver']['incremental_conditions']['param_chem_pot']['a'] = 0.0
    
    cwd = os.getcwd()
    if not os.path.exists(path):
      os.mkdir(path)
    os.chdir(path)
    print "Running:", path
    
    with open('input.json','w') as f:
      json.dump(tinput, f)
    
    monte_cmd(tinput)
    
    os.chdir(cwd)
    index += 1

def submit_T_down(T_grid, xi_grid):
  index = 0
  for xi in np.arange(*xi_grid):
    path = "T_down." + str(index)
    
    tinput = copy.deepcopy(input)
    tinput['driver'] = d
    tinput['driver']['initial_conditions']['temperature'] = T_grid[1]
    tinput['driver']['final_conditions']['temperature'] = T_grid[0]
    tinput['driver']['incremental_conditions']['temperature'] = -T_grid[2]
    
    tinput['driver']['initial_conditions']['param_chem_pot']['a'] = xi
    tinput['driver']['final_conditions']['param_chem_pot']['a'] = xi
    tinput['driver']['incremental_conditions']['param_chem_pot']['a'] = 0.0
    
    cwd = os.getcwd()
    if not os.path.exists(path):
      os.mkdir(path)
    os.chdir(path)
    print "Running:", path
    
    with open('input.json','w') as f:
      json.dump(tinput, f)
    
    monte_cmd(tinput)
    
    os.chdir(cwd)
    index += 1

def submit_xi_up(T_grid, xi_grid):
  index = 0
  for T in np.arange(*T_grid):
    path = "xi_up." + str(index)
    
    tinput = copy.deepcopy(input)
    tinput['driver'] = d
    tinput['driver']['initial_conditions']['temperature'] = T
    tinput['driver']['final_conditions']['temperature'] = T
    tinput['driver']['incremental_conditions']['temperature'] = 0.0
    
    tinput['driver']['initial_conditions']['param_chem_pot']['a'] = xi_grid[0]
    tinput['driver']['final_conditions']['param_chem_pot']['a'] = xi_grid[1]
    tinput['driver']['incremental_conditions']['param_chem_pot']['a'] = xi_grid[2]
    
    cwd = os.getcwd()
    if not os.path.exists(path):
      os.mkdir(path)
    os.chdir(path)
    print "Running:", path
    
    with open('input.json','w') as f:
      json.dump(tinput, f)
    
    monte_cmd(tinput)
    
    os.chdir(cwd)
    index += 1

def submit_xi_down(T_grid, xi_grid):
  index = 0
  for T in np.arange(*T_grid):
    path = "xi_down." + str(index)
    
    tinput = copy.deepcopy(input)
    tinput['driver'] = d
    tinput['driver']['initial_conditions']['temperature'] = T
    tinput['driver']['final_conditions']['temperature'] = T
    tinput['driver']['incremental_conditions']['temperature'] = 0.0
    
    tinput['driver']['initial_conditions']['param_chem_pot']['a'] = xi_grid[1]
    tinput['driver']['final_conditions']['param_chem_pot']['a'] = xi_grid[0]
    tinput['driver']['incremental_conditions']['param_chem_pot']['a'] = -xi_grid[2]
    
    cwd = os.getcwd()
    if not os.path.exists(path):
      os.mkdir(path)
    os.chdir(path)
    print "Running:", path
    
    with open('input.json','w') as f:
      json.dump(tinput, f)
    
    monte_cmd(tinput)
    
    os.chdir(cwd)
    index += 1



####  

with open('metropolis_grand_canonical.json','r') as f:
  input = json.load(f)

submit_T_up(T_grid, xi_grid)
#submit_T_down(T_grid, xi_grid)
#submit_xi_up(T_grid, xi_grid)
#submit_xi_down(T_grid, xi_grid)


