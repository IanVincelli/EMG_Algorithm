
import tensorflow as tf
import numpy as np
import tensorboard

data = np.load("data1.npy")
print(np.shape(data))
y_true = []
input =[]
input_shape = []
input_size = 20
#need to put something here for taking initial inputs
for n in range(0,3):
    inp = []
    for m in range(0,4):
        x = data[n,m]
        x_size = np.size(x)

        if x_size % input_size != 0:
            rem = x_size%input_size
            del x[0:rem]

        inp.extend(x)
        print(np.shape(inp))
        x_size = np.size(x)
        input_shape.append(x_size/input_size)
        if n == 0:
            if m == 0:
                for i in range(0,int(x_size/input_size)):
                    y_true.append([1,0,0])
            elif m == 1 or m == 3:
                for i in range(0,int(x_size/input_size)):
                    y_true.append([0,1,0])
            else:
                for i in range(0,int(x_size/input_size)):
                    y_true.append([0,0,1])
    input.append(inp)




print(np.shape(input[0]))
in_shape = sum(input_shape)
print(np.shape(y_true))


#now we begin the tensorflow section
#x = tf.constant(data[0,0])

##x_max = tf.reduce_max(x)
##x_min = tf.reduce_min(x)

##x_n = (x[:] - x_min)/(x_max-x_min)

#in_y = tf.constant(input_size,dtype = tf.float32)
#in_x = tf.constant(input_shape,dtype = tf.float32)
#inputs = tf.reshape(x_n,[in_x,in_y],name = "inputs")
#print(inputs)
##slices = tf.data.Dataset.from_tensor_slices(inputs)
##next_row = slices.make_one_shot_iterator().get_next()
#layer1 = tf.layers.Dense(units = 20,activation = tf.sigmoid)
#l1 = layer1(inputs)
#layer2 = tf.layers.Dense(units = 3,activation = tf.sigmoid)
#y_true = np.zeros([18,3])
#y_pred = layer2(l1)
#print(y_pred)
#loss = tf.losses.mean_squared_error(labels=y_true, predictions=y_pred)
#sess = tf.Session()
##writer.add_graph(tf.get_default_graph())
#init = tf.global_variables_initializer()
#sess.run(init)
#print(sess.run(loss))





