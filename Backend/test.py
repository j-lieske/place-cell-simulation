import tensorflow as tf
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.applications.mobilenet import preprocess_input
import som as sm
import numpy as np
import cnn
import pathlib, os, shutil
import matplotlib.pyplot as plt
import PIL
from PIL import Image

image_path = '../BA Walking Sim/Assets/Screenshots/Testing'
som_path = 'som_trained.npy'


# tests a trained SOM on all images in the Screenshots folder
if __name__ == '__main__':
    image_dir = pathlib.Path(image_path)
    print(image_dir)
    images = list(image_dir.glob('*\*.png'))
    no_of_images = len(images)
    model, im_size = cnn.mobilenet()

    image_ds = image_dataset_from_directory(image_dir, image_size=im_size, batch_size=1, color_mode='rgb', shuffle=False) 
    image_ds = image_ds.map(lambda images, labels: (preprocess_input(images), labels))

    predictions = model.predict(image_ds)
    print(predictions.shape)
    feature_vectors = predictions.reshape((no_of_images,1024))

    # loads trained som
    som = sm.load(filepath=som_path)
    som_shape = som.shape

    bmus, min_dists = sm.test(som = som, data = feature_vectors)

    print("Der durschnittliche Fehler über der Testmenge beträgt", np.mean(min_dists))

    # save training images into folders corresponding to their best matching unit
    os.chdir('Results')

    if os.path.isdir('Testing'): 
        shutil.rmtree('Testing')
    os.mkdir('Testing')
    os.chdir('Testing')

    for cy in range(som_shape[0]):
        for cx in range(som_shape[1]):
            os.mkdir(str(cy)+"-"+str(cx))

    os.chdir('../../')
    for i in range(no_of_images):
        im = Image.open(str(images[i]))
        im.save('Results/Testing/'+str(bmus[i][0])+'-'+str(bmus[i][1])+'/'+str(i)+'.png')