import os
import gym
import argparse
import random
import time
import sys, glob
import numpy as np
import cPickle as pickle
from Level import Level
import keras
from keras import backend as K
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Input, Dense, Reshape
from keras.layers.wrappers import TimeDistributed
from keras.optimizers import Adam, Adamax, RMSprop
from keras.layers.advanced_activations import PReLU
from keras.layers.normalization import BatchNormalization
from keras.layers.core import Activation, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.backend import tensorflow_backend as K

#Script Parameters
dimension = 30
input_dim = dimension * dimension
gamma = 0.99
update_frequency = 10
learning_rate = 0.001
resume = False
render = False
data = {}
number_of_inputs = 4

def load(file):
    with open(file, "rb") as input_file:
        d = pickle.load(input_file)
        global data
        data = dict(data.items() + d.items())


def get_as_numpy(x):
  x = [list(y) for y in x.split("\n")]

  width = len(sorted(x, key=len, reverse=True)[0])
  height = len(x)
  padWidth = (dimension - width) / 2
  padHeight = (dimension - height) / 2
  I = np.zeros([dimension, dimension], dtype=float)
  for i, y in enumerate(x):
    for j, z in enumerate(y):
      if z is '#':
        I[padWidth + i, padHeight + j] = 0.2
      elif z is '@':
        I[padWidth + i, padHeight + j] = 1
      elif z is '+':
        I[padWidth + i, padHeight + j] = 0.6
      elif z is '$':
        I[padWidth + i, padHeight + j] = 0.8
      elif z is '.':
        I[padWidth + i, padHeight + j] = 0.4
      elif z is '*':
        I[padWidth + i, padHeight + j] = 0.5
  return I

#Define the main model (WIP)
def learning_model(input_dim=dimension * dimension, model_type=1):
  model = Sequential()
  if model_type == 0:
    model.add(Reshape((1, dimension, dimension), input_shape=(input_dim,)))
    model.add(Flatten())
    model.add(Dense(200, activation='relu'))
    model.add(Dense(number_of_inputs, activation='softmax'))
    opt = RMSprop(lr=learning_rate)
  else:
    model.add(Reshape((1, dimension, dimension), input_shape=(input_dim,)))
    model.add(Conv2D(32, (3, 3), padding='same', kernel_initializer='he_uniform', activation="relu"))
    model.add(keras.layers.Dropout(0.25))
    # model.add(Conv2D(64, (3, 3), padding='same', activation="relu"))
    model.add(Conv2D(64, (3, 3), padding='same', activation="relu"))
    model.add(MaxPooling2D(data_format="channels_first", pool_size=(2, 2)))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(128, kernel_initializer="he_uniform", activation="relu"))
    model.add(Dense(number_of_inputs, activation='softmax'))
    opt = Adam(lr=learning_rate)
  model.compile(loss='categorical_crossentropy', optimizer=opt)
  if resume == True:
    model.load_weights('sokoban_checkpoint.hdf5')
  return model
xs = []
ys = []
model = learning_model()

def getAction(s):
  state = s.toString()
  x = get_as_numpy(state).ravel()
  p = ((model.predict(x.reshape([1, x.shape[0]]), batch_size=1).flatten()))
  dic = {
    "L": p[0],
    "R": p[1],
    "U": p[2],
    "D": p[3]
  }
  l = sorted(dic, key=dic.get)
  l.reverse()
  return "".join(l)


# state = "##############\n#   .$    @  #\n##############"
# getAction(state);

if __name__ == '__main__':
  load("test-0-8-weight.pkl")
  # load("test-1-37476-weight.pkl")
  load("test-2-41617-weight.pkl")
  load("test-3-43652-weight.pkl")
  load("test-4-43837-weight.pkl")
  load("test-5-44118-weight.pkl")
  load("test-6-44193-weight.pkl")
  load("test-7-44414-weight.pkl")
  load("test-8-45029-weight.pkl")
  load("test-9-48413-weight.pkl")
  load("test-10-56545-weight.pkl")
  # load("test-11-1060338-weight.pkl")
  # load("test-12-1085133-weight.pkl")
  # load("test-13-1134657-weight.pkl")
  # load("test-14-1144167-weight.pkl")
  load("magic_sokoban6-1-2340-weight.pkl")
  load("magic_sokoban6-2-1267-weight.pkl")
  load("magic_sokoban6-3-52620-weight.pkl")
  load("magic_sokoban6-4-9330-weight.pkl")
  load("magic_sokoban6-5-29500-weight.pkl")
  load("magic_sokoban6-6-22410-weight.pkl")
  load("magic_sokoban6-7-23044-weight.pkl")
  # load("magic_sokoban6-8-193683-weight.pkl")
  # load("magic_sokoban6-9-313548-weight.pkl")
  # Augment the data with 3 rotations and 2 mirrors

  # We train if run as the main function
  data = {k: v for k, v in data.items() if v is not False and len(v) > 0}
  print "Training from %d training points" % (len(data))
  keys = data.keys()
  key = "LRUD"
  for multiplier in range(8):
    for i in keys:
      o = data[i]
      # i, o = random.choice(list(data.items()))
      x = get_as_numpy(i)
      if len(o) is 0:
        continue;
      if multiplier % 8 is 0:
        # Flip on the x axis
        x = np.flipud(x)
        key = "LRDU"
      elif multiplier % 8 is 1:
        x = np.fliplr(x)
        key = "RLUD"
      elif multiplier % 8 is 2:
        x = np.rot90(x)
        key = "DULR"
      elif multiplier % 8 is 3:
        x = np.rot90(np.rot90(x))
        key = "RLDU"
      elif multiplier % 8 is 4:
        x = np.rot90(np.rot90(np.rot90(x)))
        key = "UDRL"
      elif multiplier % 8 is 5:
        x = np.fliplr(np.rot90(x))
        key = "DURL"
      elif multiplier % 8 is 6:
        x = np.flipud(np.rot90(x))
        key = "UDLR"

      upos = "LRUD".index(o[0]) # Unchanged position
      realValue = key[upos]
      pos = "LRUD".index(realValue)
      y = np.zeros(4)
      y[pos] = 1
      xs.append(x.ravel())
      ys.append(y)
  checkpointer = ModelCheckpoint(
      filepath='sokoban_checkpoint.hdf5', verbose=2, save_best_only=True)
  history = model.fit(x=np.array(xs), y=np.array(
      ys), epochs=50, validation_split=0.2, verbose=2, batch_size=128, callbacks=[checkpointer])
  # list all data in history
  print(history.history.keys())
  # summarize history for accuracy
  plt.plot(history.history['acc'])
  plt.plot(history.history['val_acc'])
  plt.title('model accuracy')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()
  # summarize history for loss
  plt.plot(history.history['loss'])
  plt.plot(history.history['val_loss'])
  plt.title('model loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()
#Predict probabilities from the Keras model
# aprob = ((model.predict(x.reshape([1, x.shape[0]]), batch_size=1).flatten()))
