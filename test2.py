import pandas as pd


exampleSize = 70

startPosition = 0
churnFlagPosition = 60

churnSamples = []
notChurnSamples = []
notChurnDf = pd.DataFrame()
reader = pd.read_csv('chunk 0.csv')

reader = pd.read_csv('chunk 14.csv')
reader_churnflg = reader[reader['code']=='churn_flg']

churn = reader_churnflg[reader_churnflg['1'] == '1']
chunkSize = 16




def splitChurnAndWrite(files):
    for chunkNumber in range(chunkSize):
        files = 'chunk {chunkOrder}.csv'
        reader = pd.read_csv(files.format(chunkOrder=chunkNumber))
        churnSamples = []
        for i in churn.index:
            startPosition = i-60
            churnSample = reader.loc[startPosition:startPosition+exampleSize-1,:]
            churnSamples.append(churnSample)

        churnSamples = pd.concat(churnSamples, ignore_index=True)
        churnSamples.to_csv(files+'churn.csv',index=False)

def splitNotChurnAndWrite():
    notChurnBool = reader['month'] == 201706
    for i in churn.index:
        startPosition = i - 60
        notChurnBool[startPosition:startPosition + exampleSize] = False


def splitFile():
    reader = pd.read_csv('YBK201704_SORT.txt', sep=',',
                         names= ["month", "id", "code", "1","2","3","4","5","6","7","8","9","10",
                              "11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"],chunksize=7000000)
    chunks = []
    chunkDf = pd.DataFrame()
    i = 0
    files = 'chunk {chunkOrder}.csv'
    for chunk in reader:
        chunks.append(chunk)
        chunkDf = pd.concat(chunks, ignore_index=True)
        chunkDf.to_csv(files.format(chunkOrder=i), index=False)
        i = i + 1
        chunks = []
