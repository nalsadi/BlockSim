import numpy as np
from matplotlib import pyplot as plt

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True


x = np.linspace(1e10, 6e10, 100)
y1 = 10 * 2**32 / x
y2 = 100 * 2**32 / (x)
y3 = 300 * 2**32 / (x)
y4 = 500 * 2**32 / (x)
plt.plot(x, y1, color='red',label='10')
plt.plot(x, y2, color='blue',label='100')
plt.plot(x, y3, color='yellow',label='300')
plt.plot(x, y4, color='green',label='500')
plt.legend(title='Varying Difficulty')
plt.ylabel('Hash Time')
plt.xlabel('Hash Rate')

plt.show()