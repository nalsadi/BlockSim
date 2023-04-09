from matplotlib import pyplot as plt
import pandas as pd 
import re 

file1 = open("diff.csv","r+")
#file1 = open("avg_hashpower.csv","r+")

data = file1.read().split(',')
data = pd.DataFrame(data)
data= data[:-1]

data[0]= data[0].astype(float)

print(data)
data.plot()
plt.legend().remove()
plt.xlabel('Time')
plt.ylabel('Difficulty')
plt.show()