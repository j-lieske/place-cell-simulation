import os, sys, pathlib
script_dir = os.path.dirname( __file__ )
project_dir = os.path.join( script_dir, '..', '..')
sys.path.append( project_dir )
import cnn
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.applications import imagenet_utils
from tensorflow.keras.applications.mobilenet import preprocess_input
import numpy as np

image_path = 'Experiments/CNNArch/Images'
categories = ['Beach', 'Cave', 'Forest', 'Winter']


# categorize images from hand picked categories in order to determine whether the cnn architecture gives useful results
if __name__  == "__main__":

    #load mobilenet
    model, im_size = cnn.full_mobilenet()

    # categorize images from each hand picked category
    image_dir = pathlib.Path(image_path)
    image_ds = image_dataset_from_directory(image_dir, image_size=im_size, batch_size=1, color_mode='rgb', shuffle=False) 
    image_ds = image_ds.map(lambda images, labels: (preprocess_input(images), labels))

    predictions = model.predict(image_ds)
    results = imagenet_utils.decode_predictions(predictions)

    print(model.summary())
    
    for i, category in enumerate(categories):
        cat_dict = {}
        for j in range(5):
            for a in range(3):
                pred = results[i*5+j][a]
                if(cat_dict.get(pred[1])):
                    cat_dict[pred[1]] += pred[2]
                else:
                    cat_dict[pred[1]] = pred[2]
        top = np.array(list(cat_dict.items()))
        print(top)
    