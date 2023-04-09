from matplotlib import pyplot as plt
import numpy as np 
plt.bar([1,2,3],[611098137304.53233,418813079633.6103,470077106631.85724])
plt.xlabel("Miner ID")
plt.ylabel("Hash Rate")
plt.xticks(np.arange(1, 4, 1))
plt.show()