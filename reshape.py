import numpy as np

x = np.arange(1000).reshape((10,10,10))
y = x.reshape(10,10,3,-1)
print(y.shape)
print(y)

x = np.arange(10)
y = x.reshape(-1)

