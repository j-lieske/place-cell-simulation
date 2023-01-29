import os, sys, pathlib
script_dir = os.path.dirname( __file__ )
project_dir = os.path.join( script_dir, '..', '..')
sys.path.append( project_dir )
import tensorflow as tf
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import cnn
import som as sm
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# general parameters
dataset = "WeatherConditions"
train_path = "Experiments/Classifier/Images/{}/Training".format(dataset)
test_path = "Experiments/Classifier/Images/{}/Testing".format(dataset)

# som parameters
som_shape = (3,3)
som_inf_radius = 1
som_learn_rate = 0.02

# feature extraction
image_dir = pathlib.Path(train_path)
model, im_size = cnn.mobilenet()

image_ds = image_dataset_from_directory(image_dir, image_size=im_size, batch_size=1, color_mode='rgb')
image_ds = image_ds.map(lambda images, labels: (preprocess_input(images), labels))

predictions = model.predict(image_ds)
feature_vectors = predictions.reshape((-1,1024))

# training
som = sm.init(shape = som_shape, features = 1024, min = 0, max = 2, step = 0.001)
som, _, min_dists = sm.train(som = som, learn_rate = som_learn_rate, r_neighbors = som_inf_radius, data = feature_vectors)

plt.plot(range(0,len(min_dists),100), np.mean(min_dists.reshape(-1,100), axis=1))
plt.xlabel('Anzahl präsentierter Bilder')
plt.ylabel('durchschnittliche Distanz zur BMU')
plt.show()

# testing
directs = [ f.path for f in os.scandir(test_path) if f.is_dir() ]
classes = list(map(lambda direct: direct.split("\\")[1], directs))

# feature extraction
image_dir = pathlib.Path(test_path)
image_ds = image_dataset_from_directory(image_dir, image_size=im_size, batch_size=1, color_mode='rgb', shuffle=False)
image_ds = image_ds.map(lambda images, labels: (preprocess_input(images), labels))

predictions = model.predict(image_ds)
feature_vectors = predictions.reshape((-1,1024))

bmus, _ = sm.test(som = som, data = feature_vectors)

results = []

for c in np.reshape(bmus, (-1,50,2)):
    c_results = [0] * 9
    for bmu in c:
        c_results[bmu[0]*3+bmu[1]]+= 1
    results.append(c_results)

accs = []
for c in results:
    accs.append(max(c)/50)

print("Average accuracy of classification compared to labels is: {}".format(np.mean(accs)))