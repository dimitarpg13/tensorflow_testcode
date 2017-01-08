import tensorflow as tf
import os
 

W= tf.Variable(tf.zeros([5,1]),name="weights")
b= tf.Variable(0.,name="bias")

def read_csv(batch_size, file_name, record_defaults):
    filename_queue = tf.train.string_input_producer([os.path.abspath(".") + "/" + file_name])

    reader = tf.TextLineReader(skip_header_lines=1)

    key, value = reader.read(filename_queue)

    # decode_csv will convert a Tensor from type string (the text line) in 
    # a tuple of tensor columns with the sepcified defaults, which also
    # sets the data type for each column

    decoded = tf.decode_csv(value, record_defaults=record_defaults)

    # batch actually reads the file and loads "batch_size" rows in a single
    # tensor

    return tf.train.shuffle_batch(decoded, batch_size=batch_size,
                                  capacity=batch_size * 50,
                                  min_after_dequeue=batch_size)

def inputs():

    passengerid, survived, pclass, name, sex, age, sibsp, parch, ticket, fare, cabin, embarked =  read_csv(100, "train.csv", [[0.0], [0.0], [0], [""], [""], [0.0], [0.0], [0.0], [""], [0.0], [""], [""]])

    # convert categorical data
    is_first_class = tf.to_float(tf.equal(pclass, [1]))
    is_second_class = tf.to_float(tf.equal(pclass, [2]))
    is_third_class = tf.to_float(tf.equal(pclass, [3]))


    gender = tf.to_float(tf.equal(sex, ["female"]))

    # finally we pack all the features in a single matrix
    # we then transpose to have a matrix with one example per row and
    # one feature per column
    
    features = tf.transpose(tf.pack([is_first_class, is_second_class, 
                            is_third_class, gender, age]))

    survived = tf.reshape(survived, [100, 1])

    return features, survived
     
def train(total_loss):

    learning_rate = 0.01

    return tf.train.GradientDescentOptimizer(learning_rate).minimize(total_loss)

def evaluate(sess, X, Y):

    predicted = tf.cast(inference(X) > 0.5, tf.float32)

    print (sess.run(tf.reduce_mean(tf.cast(tf.equal(predicted, Y), tf.float32))))

def combine_inputs(X):
    return tf.matmul(X, W) + b

def inference(X):
    return tf.sigmoid(combine_inputs(X))

def loss(X, Y):
    return tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(combine_inputs(X), Y))

X, Y = inputs()

with tf.Session() as sess:
    tf.global_variables_initializer().run()
    
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    example = sess.run([X])
    print(example)
    
    coord.request_stop()
    coord.join(threads)
#    total_loss = loss(X, Y)
#    train_op = train(total_loss)

#    training_steps = 1000
#    initial_step = 0

#    for step in range(initial_step, training_steps):
#        sess.run([train_op])
        
#        if step % 10 == 0:
#            print("loss: ", sess.run([total_loss]))

#        evaluate(sess, X, Y) 