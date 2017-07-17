import tensorlayer as tl
from tensorlayer.layers import  *
import tensorflow as tf

class Config:
    fc1_n_units = 800
    drop1_keep = 0.8
    fc2_n_units = 800
    drop2_keep = 0.8
    fc3_n_units = 800
    drop3_keep = 0.8
    fc4_n_units = 800
    drop4_keep = 0.8
    learning_rate = 1e-4
def Inference(x):

    network = InputLayer(x, name='input')
    network = DenseLayer(network, n_units=Config.fc1_n_units , act = tf.nn.relu,name ='fc1')
    network = DropoutLayer(network, keep=Config.drop1_keep, name='drop1')
    network = DenseLayer(network, n_units=Config.fc2_n_units , act = tf.nn.relu,name ='fc2')
    network = DropoutLayer(network, keep=Config.drop2_keep, name='drop2')
    network = DenseLayer(network, n_units=Config.fc3_n_units , act = tf.nn.relu,name ='fc3')
    network = DropoutLayer(network, keep=Config.drop3_keep, name='drop3')
    network = DenseLayer(network, n_units=Config.fc4_n_units , act = tf.nn.relu,name ='fc4')
    network = DropoutLayer(network, keep=Config.drop4_keep, name='drop4')

    network = DenseLayer(network, n_units=2, act = tf.identity,name ='output')
    return network.outputs,network

def Loss(output,target):
   return tl.cost.cross_entropy(output=output,target=target,name='entropy')

def Optimizer(loss):
    return tf.train.AdamOptimizer(Config.learning_rate).minimize(loss=loss)