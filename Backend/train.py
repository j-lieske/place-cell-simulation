import tensorflow as tf
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.applications.mobilenet import preprocess_input
import numpy as np
import cnn
import math, os, pathlib, sys, shutil
import PIL
from PIL import Image
import som as sm
import matplotlib.pyplot as plt
import tikzplotlib as tkz

image_path = '../BA Walking Sim/Assets/Screenshots/Training'

# som parameters
som_shape = (3,3)
som_inf_radius = 1
som_learn_rate = 0.02


# trains a new SOM on all images in the Screenshots folder and saves the vectors in a csv file
if __name__ == '__main__':
    image_dir = pathlib.Path(image_path)
    images = list(image_dir.glob('*\*.png'))
    no_of_images = len(images)
    model, im_size = cnn.mobilenet()

    image_ds = image_dataset_from_directory(image_dir, image_size=im_size, batch_size=1, color_mode='rgb')
    image_ds = image_ds.map(lambda images, labels: (preprocess_input(images), labels))

    predictions = model.predict(image_ds)
    feature_vectors = predictions.reshape((no_of_images,1024))

    # initializes som weight vectors with random values between 0 and 2
    som = sm.init(shape = som_shape, features = 1024, min = 0, max = 2, step = 0.001)

    # trains the som on the feature vectors generated from the training images
    som, bmus, min_dists = sm.train(som = som, learn_rate = som_learn_rate, r_neighbors = som_inf_radius, data = feature_vectors)

    plt.plot(range(0,len(min_dists),500), np.mean(min_dists.reshape(-1,500), axis=1))
    plt.xlabel('Anzahl präsentierter Bilder')
    plt.ylabel('durchschnittliche Distanz zur BMU')
    tkz.save("training.tex")
    plt.show()

    sm.save(som = som, filepath = "som")

    """ # save training images into folders corresponding to their best matching unit
    os.chdir('Results')

    if os.path.isdir('Training'): 
        shutil.rmtree('Training')
    os.mkdir('Training')
    os.chdir('Training')

    for cy in range(som_shape[0]):
        for cx in range(som_shape[1]):
            os.mkdir(str(cy)+"-"+str(cx))

    os.chdir('../../')
    for i in range(no_of_images):
        im = Image.open(str(images[i]))
        im.save('Results/Training/'+str(bmus[i][0])+'-'+str(bmus[i][1])+'/'+str(i)+'.png') """