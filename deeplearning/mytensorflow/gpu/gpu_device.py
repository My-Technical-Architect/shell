# -*- coding: utf-8 -*-

import tensorflow as tf

a = tf.constant([1.0, 2.0, 3.0], shape=[3], name='a')
b = tf.constant([1.0, 2.0, 3.0], shape=[3], name='b')

c = a + b


if __name__ == "__main__":
	with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
		print sess.run(c)
