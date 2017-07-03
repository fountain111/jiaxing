from jiaxing.train_data import TrainData
import tensorlayer as tl
from tensorlayer.layers import *
import tensorflow as tf

data = TrainData()

class Config:
    fc1_n_units = 40
    drop1_keep = 0.5
    fc2_n_units = 25
    drop2_keep = 0.5
    fc3_n_units = 20
    drop3_keep = 0.5
    learning_rate = 1e-4
    batch_size = 200

x = tf.placeholder(tf.float32, [None, 8], 'sample')
y_ = tf.placeholder(tf.int64, [None], 'lable')
network = InputLayer(x, name='input')
network = DenseLayer(network, n_units=Config.fc1_n_units , act = tf.nn.relu,name ='fc1')
network = DropoutLayer(network, keep=Config.drop1_keep, name='drop1')
network = DenseLayer(network, n_units=Config.fc2_n_units , act = tf.nn.relu,name ='fc2')
network = DropoutLayer(network, keep=Config.drop2_keep, name='drop2')
network = DenseLayer(network, n_units=Config.fc3_n_units , act = tf.nn.relu,name ='fc3')
network = DropoutLayer(network, keep=Config.drop2_keep, name='drop3')
network = DenseLayer(network, n_units=2, act = tf.identity,name ='output')
y = network.outputs

cost = tl.cost.cross_entropy(y, y_, name='xentropy')
train_op = tf.train.AdamOptimizer(Config.learning_rate).minimize(cost)
#y_op = tf.argmax(y, 1)
accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(y, 1), y_), tf.float32))

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

for par in network.all_params:
    tf.summary.histogram(par.name, par)
tf.summary.scalar('loss', cost)
merged = tf.summary.merge_all()
train_write = tf.summary.FileWriter('/tmp/jiaxing', sess.graph)

dp_dict = tl.utils.dict_to_one(network.all_drop)
train_step = 0
while True:
    samples, lables= data.next_batch(Config.batch_size)
    if train_step % 1000 == 0:
        dp_dict = tl.utils.dict_to_one(network.all_drop)
        feed_dict = {x: samples, y_: lables}
        feed_dict.update(dp_dict)
        train_accuracy, loss ,result= sess.run([accuracy, cost, merged], feed_dict = feed_dict)
        print("step : %d, training accuracy %g, loss %g" % (train_step, train_accuracy, loss))
        train_write.add_summary(result, train_step / 1000)
        if train_step % 10000 == 0:
            samples, lables = data.test_batch_lw(2000)
            feed_dict = {x: samples, y_: lables}
            feed_dict.update(dp_dict)
            train_accuracy = accuracy.eval(feed_dict=feed_dict)
            print("测试离网正确率%g" % train_accuracy)

            samples, lables = data.test_batch_wlw(2000)
            feed_dict = {x: samples, y_: lables}
            feed_dict.update(dp_dict)
            train_accuracy = accuracy.eval(feed_dict=feed_dict)
            print("测试未离网正确率%g" % train_accuracy)

    feed_dict =  {x: samples, y_: lables}
    feed_dict.update(network.all_drop)
    train_op.run(feed_dict=feed_dict)
    train_step += 1

# 模型保存
# saver = tf.train.Saver()
# saver.save(sess, 'model/model1')
train_write.close()