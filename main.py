print('Hello, world!')
import numpy as np
import os
import pandas as pd

print(os.listdir(os.getcwd()))




#root = tk.Tk()
#labelDictionary = {}
#for i in range(10):
#  labelDictionary[str(i)] = tk.Label(root, text=str(np.sin(i)))
#  labelDictionary[str(i)].pack()
#root.mainloop()

#print(np.sin(10))

print(os.getcwd())

df = pd.read_csv(os.path.join(os.getcwd(), 'testData.csv'), index_col=0)

df.insert(2, 'attribute3', [0,1,0,1])
df.insert(3, 'attribute4', ['a','a','b','b'])
df.insert(4, 'attribute5', ['a','b','a','b'])

print(df)

df.to_csv('analyzedData.csv')
df = df[df['attribute1'] > 1]
print(df.groupby('attribute3').mean())
print(df.groupby('attribute4').mean())
print(df.groupby('attribute5').mean())



