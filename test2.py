import numpy as np
import pandas as pd
exampleSize = 70

startPosition = 0
churnFlagPosition = 60

churnSamples = []
notChurnSamples = []
notChurnDf = pd.DataFrame()
reader = pd.read_csv('chunk 0.csv')

reader_churnflg = reader[reader['code']=='churn_flg']

churn = reader_churnflg[reader_churnflg['1'] == '1']

for i in churn.index:
    startPosition = i-60
    churnSample = reader.loc[startPosition:startPosition+exampleSize,:]
    churnSamples.append(churnSample)
    reader.drop(reader.index[startPosition:startPosition + exampleSize], inplace=True)
churnSamples = pd.concat(churnSamples, ignore_index=True)
churnSamples.to_csv('chunk 0 churn.csv')
reader.to_csv('chunk 0 notChurn.csv')