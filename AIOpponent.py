import os

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

checkpoint_path = "Weights.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

num_actions = 10

def create_q_model():
    inputs = layers.Input(shape=(5, 10))
    #add masking
    layer1 = layers.Dense(64, activation="relu")(inputs)#Hopefully to estimate penalty of each deck
    layer2 = layers.Dense(64, activation="relu")(layer1)#Hopefully to estimate which will be picked up 
    layer3 = layers.Dense(32, activation="relu")(layer2)#Hopefully to estimate which card is closest to best deck
    layer4 = layers.Dense(16, activation="relu")(layer3)#Hopefully to estimate best card

    action = layers.Dense(num_actions, activation="linear")(layer4)

    return keras.Model(inputs=inputs, outputs=action)

Opp = create_q_model()

# Loads the weights
Opp.load_weights(checkpoint_path)

