'''
A logistic regression learning algorithm example using TensorFlow library.
This example is using the MNIST database of handwritten digits
(http://yann.lecun.com/exdb/mnist/)

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import print_function

import tensorflow as tf

# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

# Parameters
learning_rate = 0.01
training_epochs = 20
batch_size = 100
display_step = 1

# tf Graph Input
x = tf.placeholder(tf.float32, [None, 784])  # mnist data image of shape 28*28=784
y = tf.placeholder(tf.float32, [None, 10])  # 0-9 digits recognition => 10 classes

# Set model weights
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))


# Construct model
pred = tf.nn.softmax(tf.matmul(x, W) + b)   # Softmax

# Minimize error using cross entropy
cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred), reduction_indices=1))
# Gradient Descent
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# Initializing the variables
init_op = tf.global_variables_initializer()
saver = tf.train.Saver()

# Launch the graph
with tf.Session() as sess:
    sess.run(init_op)

    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = int(mnist.train.num_examples/batch_size)
        # Loop over all batches
        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_xs,
                                                          y: batch_ys})
            # Compute average loss
            avg_cost += c / total_batch
        # Display logs per epoch step
        if (epoch+1) % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost))

    print("Optimization Finished!")

    # Test model
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # Save the variables to disk.

    save_path = saver.save(sess,"/Users/mac/PycharmProjects/untitled1/MyModel",write_meta_graph=True)
    print("Model saved in file: %s" % save_path)
    print("Accuracy_old:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))

    new_saver = tf.train.import_meta_graph('MyModel.meta')
    new_saver.restore(sess, tf.train.latest_checkpoint('./'))
    all_vars = tf.get_collection('vars')
    for v in all_vars:
        v_ = sess.run(v)
        print(v_)

    #Zeroes = tf.mul(tf.zeros([784, 10]),Rand)

    #assign_op = W.assign(tf.mul(W, Rand)

    ones_mask = tf.Variable(tf.ones([784, 10]))
    index_num= tf.Variable(tf.random_uniform([784,]))
    indexNum= tf.cast(index_num, tf.int64)
    update = tf.scatter_update(ones_mask, indexNum, tf.zeros([784,10]))

    assign_op = W.assign(tf.mul(W, update))
    sess.run(tf.global_variables_initializer())
    sess.run(assign_op)
    print("Accuracy_new:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))
