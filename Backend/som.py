import numpy as np
import math
import os

def init(shape, features, min, max, step):
    return np.random.choice(np.arange(min, max, step), size = shape + (features,))

def train(som, learn_rate, r_neighbors, data):        
    somy, somx, _ = som.shape
    datalen = len(data)
    bmus = []
    min_dists = []

    for j, input in enumerate(data):
        min_dist = math.inf
        
        for i, row in enumerate(som):
            for j, vec in enumerate(row):
                # choose best matching unit by smallest euclidian distance to input vector
                eucl_dist = np.linalg.norm(input - vec) 
                if eucl_dist < min_dist:
                    min_dist = eucl_dist
                    bmu_i = (i,j)

        min_dists.append(min_dist)
        bmus.append(bmu_i)   
        # move bmu vector and its neighborhood closer to the input vector
        som[bmu_i] += (input - som[bmu_i]) * learn_rate * (2 - j/datalen)

        curr = [bmu_i]
        for r in range(r_neighbors):
            nxt = []
            for index in curr:
                for dim in range(len(index)):
                    down = index[:dim] + (index[dim]-1,) + index[dim+1:]
                    up = index[:dim] + (index[dim]+1,) + index[dim+1:]
                    if 0 <= down[dim]:
                        som[down] += ( input - som[down]) * (learn_rate / (r+2)) * (1 - j/datalen)
                        nxt.append(down)
                    if up[dim] < somx:
                        som[up] += ( input - som[up]) * (learn_rate / (r+2)) * (1 - j/datalen)
                        nxt.append(up)
            curr = nxt

        
    return som, np.array(bmus), np.array(min_dists)

def test(som, data):
    bmus = []
    min_dists = []

    for j, input in enumerate(data):
        min_dist = math.inf
        
        for i, row in enumerate(som):
            for j, vec in enumerate(row):
                # choose best matching unit by smallest euclidian distance to input vector
                eucl_dist = np.linalg.norm(input - vec)
                if eucl_dist < min_dist:
                    min_dist = eucl_dist
                    bmu_i = (i,j)

        min_dists.append(min_dist)
        bmus.append(bmu_i)
    
    return np.array(bmus), np.array(min_dists)

def save(som, filepath):
    if os.path.exists(filepath): os.remove(filepath)
    np.save(filepath, som)

def load(filepath):
    return np.load(filepath)