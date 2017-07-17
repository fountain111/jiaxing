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


notChurnBool = reader['month']==201705
for i in churn.index:
    startPosition = i-60
    notChurnBool[startPosition:startPosition+exampleSize] =False

#churnSamples = pd.concat(churnSamples, ignore_index=True)
#churnSamples.to_csv('chunk 0 churn.csv')
newReader = reader[notChurnBool]
newReader.to_csv('chunk 0 notChurn.csv')