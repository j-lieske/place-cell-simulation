import zmq
import time
import numpy as np
import cnn
import som as sm
import tensorflow as tf
from tensorflow.keras.applications.mobilenet import preprocess_input
from matplotlib import pyplot as plt
import gc

def img_from_buff(byte_buffer):
     byte_array = np.frombuffer(byte_buffer, dtype="B")
     int_array = byte_array[:-8].astype('int32') #last 8 bytes are 2 ints specifying width and height
     int_array = np.delete(int_array, np.arange(3, int_array.size, 4)) # remove alpha channel
     img_array = int_array.reshape(int.from_bytes(byte_array[-4:], "little"), int.from_bytes(byte_array[-8:-4], "little"),3) # reshape to image dimensions determined by last two ints
     img_array = np.flipud(img_array) # flip image vertically to counteract Unity's bottom left origin
     return img_array

def prep_img(img):
     img = np.expand_dims(img, 0)
     img = tf.image.resize(img, im_size)
     img = preprocess_input(img)
     return img

if __name__ == '__main__':
     #initialize nnet
     model, im_size = cnn.mobilenet()

     # initialize som
     som = sm.load('som_trained.npy')

     # initialize socket
     context = zmq.Context()
     socket = context.socket(zmq.REP)
     socket.bind("tcp://*:5555")

     print("Server started")

     while True:
          bytes_received = socket.recv()
          img = img_from_buff(bytes_received)
          img = prep_img(img)
          prediction = model.predict(img) # feature extraction
          features = prediction.reshape((1,1024))
          bmus, _ = sm.test(som, features) # inferencing on SOM using features
          byte_ans = bmus.tobytes()
          socket.send(byte_ans)
          gc.collect()
