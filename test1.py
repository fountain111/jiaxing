import numpy as np
import pandas as pd
exampleSize = 70

startPosition = 0
churnFlagPosition = 60


reader = pd.read_csv('chunk 0.csv')
'''reader = pd.read_csv('201705_sort.txt', sep=',',
                     names= ["month", "id", "code", "1","2","3","4","5","6","7","8","9","10",
                          "11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"],chunksize=7000000)
'''


reader = reader.drop(['month','id','code'])
#reader = pd.read_csv('201705_sort.txt',sep=',',chunksize=700)
chunks = []
chunkDf = pd.DataFrame()
i =0
files = 'chunk {chunkOrder}.csv'
for chunk in reader:

    chunks.append(chunk)
    chunkDf = pd.concat(chunks, ignore_index=True)
    chunkDf.to_csv(files.format(chunkOrder = i),index=False)
    i = i+1
    chunks = []
def test():

    chunkSize = 7000
    notChurnDf = pd.DataFrame()
    churnDf = pd.DataFrame
    loop = True
    notChurnSamples = []
    churnSamples = []
    while(loop):
        startPosition = 0
        try:
            chunk = reader.get_chunk(chunkSize)
        except StopIteration:

            loop = False

        while(startPosition<chunkSize):
            if(startPosition == chunkSize):
                print()
            sample = chunk.iloc[startPosition:(startPosition + exampleSize), :]
            if (sample.iloc[60,:]['1'] == '1'):
                churnSamples.append(sample)
                churnDf = pd.concat(churnSamples, ignore_index=True)
                print('离网')
            if (sample.iloc[60,:]['1'] == '0'):
                notChurnSamples.append(sample)
                notChurnDf= pd.concat(notChurnSamples, ignore_index=True)

            startPosition = startPosition+exampleSize
    notChurnDf.to_csv('notChurn.csv', index=False)
    churnDf.to_csv('churn.csv', index=False)


