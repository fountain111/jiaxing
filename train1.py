import tensorflow as tf
import data_process as dp
from model import *

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_integer('max_steps', 300000,
                            """Number of batches to run.""")
tf.app.flags.DEFINE_string('summary_dir', '/tmp/jiaxing',
                           """Directory where to write event logs """
                           """and checkpoint.""")
tf.app.flags.DEFINE_string('model_dir', '/tmp/jiaxing',
                           """Directory where to write event logs """
                           """and checkpoint.""")

data = dp.Data_process()
batchSize = 200


def train():
    x = tf.placeholder(tf.float32, shape=[None, data.sampleColumnSize-1])
    target_y = tf.placeholder(tf.int64, shape=[None,])

    model_labels,network = Inference(x)
    loss_op = Loss(output=model_labels, target=target_y)
    optimizer = Optimizer(loss=loss_op)
    correct_predicton = tf.equal(tf.argmax(model_labels,axis=1),target_y)
    accuracy = tf.reduce_mean(tf.cast(correct_predicton,tf.float32))
    init = tf.initialize_all_variables()
    sess = tf.InteractiveSession()
    sess.run(init)
    for step in range(FLAGS.max_steps):
       batch_x,batch_y = data.NextBatch(batchSize)
       feed_dict ={x:batch_x,target_y:batch_y}
       feed_dict.update(network.all_drop)
       _,loss = sess.run([optimizer,loss_op],feed_dict = feed_dict)
       #print(loss)
       if (step %10000 == 0):
           acc = accuracy.eval(feed_dict=feed_dict)
           print(acc)
       #     validation_loss = sess.run(loss_op, feed_dict={x: data.churn_validation[:,1:], target_y: data.churn_validation[:,0:1] })


def main(argv=None):
    #datas = pd.read_csv('training.csv')
    train()




if __name__ == '__main__':
  tf.app.run()