import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model

def mobilenet():
    img_size = (224,224)
    mobile = tf.keras.applications.mobilenet.MobileNet()
    print(mobile.summary())
    output = mobile.layers[-5].output
    model = Model(inputs = mobile.input, outputs = output)

    return model, img_size

def full_mobilenet():
    img_size = (224,224)
    mobile = tf.keras.applications.mobilenet.MobileNet()
    return mobile, img_size