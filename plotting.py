import numpy as np
from matplotlib import pyplot as plt

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True


x = np.linspace(0, 2000, 100)
y1 = x * 2**32 / 1e10
y2 = x * 2**32 / (2e10)
y3 = x * 2**32 / (4e10)
y4 = x * 2**32 / (6e10)
plt.plot(x, y1, color='red',label='1e10')
plt.plot(x, y2, color='blue',label='2e10')
plt.plot(x, y3, color='yellow',label='4e10')
plt.plot(x, y4, color='green',label='6e10')
plt.legend(title='Varying Hash Power')

plt.show()