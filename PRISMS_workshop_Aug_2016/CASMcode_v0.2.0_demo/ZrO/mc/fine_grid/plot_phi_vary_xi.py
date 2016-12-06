import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

with open('phi.pkl','rb') as f:
  phi = pickle.load(f)

with open('data.pkl','rb') as f:
  data = pickle.load(f)


step_size = 5

xi = np.arange(-2.2, -1.6, 0.01)
T = np.arange(200, 1000, 10)
N_T = len(T)


T_bound = []
left = []
right = []

for i in range(N_T):
  diff = phi['xi_down'][N_T-i-1,:] - phi['xi_up'][N_T-i-1,:]

  up_comp = np.array(data['xi_up'][i]['<comp(a)>'])
  down_comp = np.array(data['xi_down'][i]['<comp(a)>'])
  
  if diff[0] > 0.0 and diff[-1] < 0.0:
    abs_diff = abs(diff)
    index = np.where(abs_diff==min(abs_diff))[0][0]
    right.append(down_comp[-index])
    left.append(up_comp[index])
    T_bound.append(T[i])
  
  if i % step_size == 0:
  
    # create figure
    fig = plt.figure(figsize=(12,8)) 
    gs = gridspec.GridSpec(2, 4)
    
    
    # show phi vs xi
    fig.add_subplot(gs[0:1,0:2])
    plt.plot(xi, phi['xi_up'][N_T-i-1,:], 'bo-')
    plt.plot(xi, phi['xi_down'][N_T-i-1,:], 'rx-')
    plt.plot(xi, phi['lte'], 'g-')
    plt.title('T: ' + str(T[i]))
    plt.xlim([-2.2,-1.6])
    ylim_min = -0.06
    ylim_max = 0.03
    plt.ylim([ylim_min, ylim_max])
    plt.ylabel('phi')
    if diff[0] > 0.0 and diff[-1] < 0.0:
      plt.plot([xi[index], xi[index]], [ylim_min, phi['xi_up'][N_T-i-1,index]], 'k--')
      
    
    # show comp vs xi
    fig.add_subplot(gs[1:2,0:2])
    plt.plot(data['xi_up'][i]['param_chem_pot(a)'], up_comp, 'bo-')
    plt.plot(data['xi_down'][i]['param_chem_pot(a)'], down_comp, 'rx-')
    if diff[0] > 0.0 and diff[-1] < 0.0:
      plt.plot([xi[index], xi[index]], [up_comp[index], down_comp[-index]], 'k--')
      plt.plot([-2.2, xi[index]], [up_comp[index], up_comp[index]], 'b--')
      plt.plot([-2.2, xi[index]], [down_comp[-index], down_comp[-index]], 'r--')
    
    plt.xlim([-2.2,-1.6])
    plt.ylabel('<comp(a)>')
    plt.xlabel('xi')
    
    
    # show T vx comp
    fig.add_subplot(gs[0:2,2:4])
    plt.plot(left,T_bound,'bo-')
    plt.plot(right,T_bound,'rx-')
    plt.plot([left[-1],right[-1]],[T[i],T[i]],'k--')
    plt.xlabel('<comp(a)>')
    plt.ylabel('T')
    plt.xlim([0.0,0.2])
    plt.ylim([180,1020])
    
    plt.show()


