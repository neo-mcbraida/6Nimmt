import os

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

checkpoint_path = "Weights.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

num_actions = 10

model = tf.keras.models.load_model("Weights.h5") 

def OpUpdateModel():
    model = tf.keras.models.load_model("Weights.h5") 

def AIMove(state):
    state_tensor = tf.convert_to_tensor(state)
    state_tensor = tf.expand_dims(state_tensor, 0)
    action_probs = model(state_tensor, training=False)
    # Take best action
    action = tf.argmax(action_probs[0]).numpy()
    action = np.argmax(action)
    return action


