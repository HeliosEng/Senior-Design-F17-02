import h5py

import numpy as np

f1 = h5py.File("data.hdf5",'r')

print("Keys: %s" %f.keys())
a_group_key = list(f.keys)[0]


data = list(f[a_group_key])
