import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf

trainAndValidationProportion = 0.7
shapeOfRows = 0
churnAndNotChurnProportion = 2
postionOfChurnFlag = 1


class Data_process:
    #when samples imblance
    def __init__(self):
        self.startNotChurnTrainDatasLocation = 0
        self.startTrainDatasLocation = 0
        self.epoch = 0
        self.datas = pd.read_csv('new_datas.csv')
        self.churn_datas = self.datas[self.datas['CHURN_FLAG'] == 1]
        self.notchurn_datas = self.datas[self.datas['CHURN_FLAG'] == 0]
        self.churn_train = self.churn_datas.sample(frac=trainAndValidationProportion)
        self.churn_validation = self.churn_datas.drop(self.churn_train.index).as_matrix()
        self.notChurn_train = self.notchurn_datas.sample(frac=trainAndValidationProportion)
        self.notChurn_validation = self.notchurn_datas.drop(self.notChurn_train.index).as_matrix()
        self.sampleColumnSize = self.churn_train.shape[1]
        self.trainDatas = pd.concat([self.notChurn_train.iloc[self.startNotChurnTrainDatasLocation:self.startNotChurnTrainDatasLocation +
                                                                                                   self.churn_train.shape[shapeOfRows] * churnAndNotChurnProportion],self.churn_train])
        self.trainDatas = self.trainDatas.sample(frac=1).as_matrix()
        self.startNotChurnTrainDatasLocation =self.churn_train.shape[shapeOfRows]* churnAndNotChurnProportion

    def BuildTrainDatas(self):
        if (self.startNotChurnTrainDatasLocation + self.churn_train.shape[shapeOfRows]) > self.notChurn_train.shape[shapeOfRows]:
            self.ShuffleChurnAndNotChurnTrainDatas()
            self.startNotChurnTrainDatasLocation = 0
            self.startTrainDatasLocation = 0
            self.epoch = self.epoch+ 1
            print('epoch',self.epoch)

        self.trainDatas = pd.concat((self.notChurn_train.iloc[self.startNotChurnTrainDatasLocation:self.startNotChurnTrainDatasLocation +
                                                                                                  self.churn_train.shape[shapeOfRows]*churnAndNotChurnProportion],
                                                                                                  self.churn_train))
        self.trainDatas = self.trainDatas.sample(frac=1).as_matrix()
        self.startNotChurnTrainDatasLocation =  self.startNotChurnTrainDatasLocation+ self.churn_train.shape[shapeOfRows]

        return self.trainDatas

    def ShuffleChurnAndNotChurnTrainDatas(self):
        # shuffle for next BuildTrainDatas with new epoch,
        self.churn_train = self.churn_train.sample(frac=1)
        self.notChurn_train = self.notChurn_train.sample(frac=1)
        return self.churn_train,self.notChurn_train

    def NextBatch(self,batchSize):
        samples = np.zeros([batchSize,self.sampleColumnSize])
        lables = np.zeros([batchSize],np.int64)
        if (self.startTrainDatasLocation+batchSize > self.trainDatas.shape[shapeOfRows]):
            self.BuildTrainDatas()
            print("ReBuildTrainDatas")
            self.startTrainDatasLocation = 0
        samples = self.trainDatas[self.startTrainDatasLocation:self.startTrainDatasLocation+ batchSize]
        lables = samples[:,postionOfChurnFlag-1]
        samples = samples[:,postionOfChurnFlag:]
        self.startTrainDatasLocation += batchSize


        return  samples,lables


