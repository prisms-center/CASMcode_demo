import pickle
import numpy as np

with open('phi.pkl','rb') as f:
  phi = pickle.load(f)

with open('data.pkl','rb') as f:
  data = pickle.load(f)

xi = np.arange(-2.2, -1.6, 0.01)
T = np.arange(200, 1000, 10)
N_T = len(T)

import matplotlib.pyplot as plt

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
    left.append(down_comp[-index])
    right.append(up_comp[index])
    T_bound.append(T[i])

plt.plot(left,T_bound,'bo-')
plt.plot(right,T_bound,'rx-')

plt.xlabel('<comp(a)>')
plt.ylabel('T')
plt.show()


