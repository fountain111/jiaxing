import glob as gl
import pandas as pd
path = r'D:\samples\201704\churn'
allFiles = gl.glob(path +"\*.csv")
fileList = []
for files in allFiles:
    reader = pd.read_csv(files)
    fileList.append(reader)
df = pd.concat(fileList,ignore_index=True)
df.to_csv(path+'\churn01.csv',index=False)