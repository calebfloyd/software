from __future__ import division

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.io import loadmat, savemat
import matplotlib.pyplot as plt

s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')
net = s['cites']
s.close()

t_net = net.head(1000000)

t_idx = pd.Series(np.union1d(t_net['citing'].unique(),
    t_net['cited'].unique()))

d = t_idx.to_dict()
inv_d = {v:k for k, v in d.iteritems()}

### Full iterative
rows = []
cols = []

for k in t_net.index:
    i = inv_d[t_net.ix[k]['citing']]
    j = inv_d[t_net.ix[k]['cited']]
    rows.append(i)
    cols.append(j)
    if k % 1000 == 0:
        print k

rows = np.array(rows)
cols = np.array(cols)
data = np.ones(len(t_net))
N = np.max([cols.max(), rows.max()])
sp = sparse.coo_matrix((data, (rows, cols)), shape=(N + 1, N + 1))
savemat('/Users/tom/tom/DataStorage/Patents/sparse_out.mat', {'A': sp})
## Plotting ##

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.matshow(sp.toarray(), cmap=plt.cm.binary)
# print(sp.todense())
