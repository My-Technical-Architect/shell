# -*- coding: utf-8 -*-
import time
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


import mnist_inference
import mnist_train

# 每10秒加载一次最新的模型，并在测试数据上测试最新模型的正确率
EVAL_INTERVAL_SECS = 10


def evaluate(mnist):
	with tf.Graph().as_default() as g:
		# 定义输入输出的格式
		x = tf.placeholder(tf.float32, [None, mnist_inference.INPUT_NODE], name="x-input")
		y_ = tf.placeholder(tf.float32, [None, mnist_inference.OUTPUT_NODE], name="y-input")
		
		validate_feed = {x: mnist.validation.images, y_: mnist.validation.labels}
		
		# 通过封装好的函数来计算前向传播结果
		# 测试时不需要关注正则化损失的值，所以正则化损失的函数置为None
		y = mnist_inference.inference(x, None)
		
		# --------------------------------------------------------------------------------------------
		# 使用前向传播结果计算正确率
		# tf.equal 判断两个张量的每一维是否相等，相等返回True，否则返回False
		# 如果对未知的样例进行分类，使用tf.argmax就可以得到输入样例的预测类别
		correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
		# 将bool的数值转为实数型，然后计算平均值。这个平均值就是模型在这一组数据上的正确率
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

		# --------------------------------------------------------------------------------------------
		# 通过变量重命名的方式来加载模型，这样在前向传播的过程就不需要在调用求滑动平均的函数来获取平均值了
		# 这样可以完全共用mnist_inference.py中定义的前向传播过程
		variable_averages = tf.train.ExponentialMovingAverage(mnist_train.MOVING_AVERAGE_DECAY)
		variables_to_restore = variable_averages.variables_to_restore()
		saver = tf.train.Saver(variables_to_restore)
	
		# --------------------------------------------------------------------------------------------
		# 每隔EVAL_INTERVAL_SECS秒调用一次计算正确率的过程以检测训练过程中正确率的变化
		while True:
			with tf.Session() as sess:
				# tf.train.get_checkpoint_state函数会通过checkpoint文件自动找到目录中最新模型的文件名
				ckpt = tf.train.get_checkpoint_state(mnist_train.MODEL_SAVE_PATH)
				if ckpt and ckpt.model_checkpoint_path:
					# 加载模型
					saver.restore(sess, ckpt.model_checkpoint_path)
					# 通过文件名获取模型保存时迭代的轮数
					global_step = ckpt.model_checkpoint_path.split("/")[-1].split("-")[-1]
					accuracy_score = sess.run(accuracy, feed_dict=validate_feed)
					print "After %s training step(s), validation accuracy = %g" % (global_step, accuracy_score)
				else:
					print "No checkpoint file dound"
					return
			
			time.sleep(EVAL_INTERVAL_SECS)
			

def main(argv=None):
	mnist = input_data.read_data_sets("/Users/xxx/work5/tensorflow/mnist", one_hot=True)
	evaluate(mnist)
	
if __name__ == "__main__":
	tf.app.run()
