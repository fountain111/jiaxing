import csv
import numpy as np
import random
def conversion_data():
    csv_reader = csv.reader(open('data/data.csv'))


    csv_writer_lw_train = csv.writer(open('data/data_lw_train.csv', 'w'))
    csv_writer_wlw_train = csv.writer(open('data/data_wlw_train.csv', 'w'))

    csv_writer_lw_test = csv.writer(open('data/data_lw_test.csv', 'w'))
    csv_writer_wlw_test = csv.writer(open('data/data_wlw_test.csv', 'w'))

    FILE_HEADER = ['MONTH3', 'MONTH4',
                   'B_M_FLAG','M_M_FLAG', 'E_M_FLAG', 'AVERAGE_CHARGE',
                   'STOP_COUNTS', 'OWE_AVERGE',
                   'CHURN_FLAG']
    # 0"REGION_ID", 1"ACCT_MONTH", 2"ACCT_ID",3"CHURN_FLAG",4"REMARK",
    # 5"B_M_FLAG",6"M_M_FLAG",7"E_M_FLAG",8"CHARGE_AMOUNT",
    # 9"AMOUNT_COUNTS",10"AVERAGE_CHARGE",11"OWE_AMOUNT",12"STOP_COUNTS",13"OWE_AVERGE"
    line_num = -1
    f = lambda x: 0 if x == '' else int(x)
    for row in csv_reader:
        line_num += 1
        if (line_num == 0):
            continue
        new_row = []
        #月份做成one-hot
        if   row[1] == '201703':
            new_row += [1, 0]
        elif row[1] == '201704':
            new_row += [0, 1]
        else:
            print('month error')

        # 充值次数
        new_row.append(f(row[5]))
        new_row.append(f(row[6]))
        new_row.append(f(row[7]))

        #平均充值，归一
        new_row.append(f(row[10])/5000)

        #停机次数
        new_row.append(f(row[12]))

        #平均欠费，归一
        new_row.append(f(row[13])/1500)

        #标签
        new_row.append(f(row[3]))

        #未离网
        if (new_row[-1] == 0):
            #80%训练集
            if random.randint(0, 1000) > 200:
                csv_writer_wlw_train.writerow(new_row)
            #20%测试集
            else:
                csv_writer_wlw_test.writerow(new_row)
        #离网
        else:
            if random.randint(0, 1000) > 200:
                csv_writer_lw_train.writerow(new_row)
            else:
                csv_writer_lw_test.writerow(new_row)





#统计均值
def xxxxx():
    csv_reader = csv.reader(open('../data/data.csv'))
    line_num = -1
    amount_counts = 0
    stop_counts = 0
    ave_cha = 0
    ave_owe = 0
    f = lambda x: 0 if x=='' else int(x)
    for row in csv_reader:
        line_num += 1
        #print(line_num)
        if (line_num == 0):
            continue
        #print(f(row[9]))
        amount_counts += f(row[9])
        stop_counts += f(row[12])
        ave_cha += f(row[10])
        ave_owe += f(row[13])

    print('amount_counts', amount_counts, amount_counts/line_num)
    print('stop_counts', stop_counts, stop_counts/line_num)
    print('ave_cha', ave_cha, ave_cha/line_num)
    print('ave_owe', ave_owe, ave_owe/line_num)

    # amount_counts 1952601 1.0954344764907518
    # stop_counts 1101200 0.617787477068595
    # ave_cha 9456513354 5305.226595380619
    # ave_owe 2692796788 1510.6939102042647




class TrainData:
    def __init__(self):
        #导入训练集
        self.data_lw_train = np.loadtxt(open("data/data_lw_train.csv", "rb"),dtype=np.float32, delimiter=",", skiprows=0)
        self.data_wlw_train = np.loadtxt(open("data/data_wlw_train.csv", "rb"), dtype=np.float32, delimiter=",", skiprows=0)

        #导入测试集
        self.data_lw_test = np.loadtxt(open("data/data_lw_test.csv", "rb"), dtype=np.float32, delimiter=",", skiprows=0)
        self.data_wlw_test = np.loadtxt(open("data/data_wlw_test.csv", "rb"), dtype=np.float32, delimiter=",",  skiprows=0)



    def next_batch(self, batch_size):
        num_wlw = self.data_wlw_train.shape[0] - 1
        num_lw = self.data_lw_train.shape[0] - 1

        arr = np.zeros([batch_size, 8], np.float32)
        lable = np.zeros([batch_size], np.int64)
        for i in range(batch_size):
            #训练数据70%是未离网的，30%是离网的
            if random.randint(0, 1000) > 300:
                arr[i] = self.data_wlw_train[random.randint(0, num_wlw), 0:8]
                lable[i] = 0
            else:
                arr[i] = self.data_lw_train[random.randint(0, num_lw), 0:8]
                lable[i] = 1
        return arr, lable

    def test_batch_wlw(self, batch_size):
        arr = np.random.randint(0, self.data_wlw_test.shape[0] - 1, size= batch_size)
        return self.data_wlw_test[arr, 0:8], self.data_wlw_test[arr, -1]

    def test_batch_lw(self, batch_size):
        arr = np.random.randint(0, self.data_lw_test.shape[0] - 1, size=batch_size)
        return self.data_lw_test[arr, 0:8], self.data_lw_test[arr, -1]


if __name__ =='__main__':
    conversion_data()

