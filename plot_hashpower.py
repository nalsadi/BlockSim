from matplotlib import pyplot as plt
import pandas as pd 
import re 

file1 = open("hashtime.csv","r+")
data = file1.read().split(',')
data = pd.DataFrame(data)

data[0]= data[0].str.replace("", '0')

data[0]= data[0].astype(float)

print(data)
data.plot()
plt.show()