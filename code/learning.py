import os
import gym
import argparse
import random
import time
import sys
import glob
import numpy as np
import cPickle as pickle
from Level import Level
from keras import backend as K
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Input, Dense, Reshape
from keras.layers.wrappers import TimeDistributed
from keras.optimizers import Adam, Adamax, RMSprop
from keras.layers.advanced_activations import PReLU
from keras.layers.normalization import BatchNormalization
from keras.layers.core import Activation, Dropout, Flatten
from keras.layers.convolutional import UpSampling2D, Convolution2D

#Script Parameters
dimension = 32
input_dim = dimension * dimension
gamma = 0.99
update_frequency = 10
learning_rate = 0.001
resume = False
render = False
level_set = "test"
min_level = 19
max_level = 19
num_actions_for_fail = 10
current_level = 0
last_level = 0


def loadRandomLevel():
  global current_level
  global last_level
  # TODO: Make more levels by rotation and mirroring
  last_level = current_level
  current_level = random.randint(min_level, max_level)
  matrix = Level(level_set, current_level).matrix
  matrix.moves = 0
  matrix.actions = ""
  return matrix


#Initialize
# env = gym.make("Pong-v0")
# number_of_inputs = env.action_space.n #This is incorrect for Pong (?)
number_of_inputs = 4  # LRUD
#number_of_inputs = 1
observation = loadRandomLevel()  # env.reset()
prev_x = None
xs, dlogps, drs, probs = [], [], [], []
running_reward = None
reward_sum = 0
episode_number = 0
train_X = []
train_y = []


def get_as_numpy(x):
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

  # I = I[35:195]
  # I = I[::2,::2,0]
  # I[I == 144] = 0
  # I[I == 109] = 0
  # I[I != 0] = 1
  return I.ravel()


def perform_action(matrix, action):
  move = "LRUD"[action]
  matrix.successor(move, True)
  matrix.actions = matrix.actions + move
  # matrix.moves = -1 if matrix.moves is None else matrix.moves - 1
  reward = 0.0
  done = False
  if matrix.isSuccess():
    reward = 1.0  # - (len(matrix.actions) / 2.0 * num_actions_for_fail)
    done = True
    # print "Moves %s"%(matrix.actions)
  if len(matrix.actions) >= num_actions_for_fail:
    done = True  # Failure
    reward = -1.0
  # if current_level is 19:
    # print "Moves %s"%(matrix.actions)
  return matrix, reward, done


def discount_rewards(r):
  discounted_r = np.zeros_like(r)
  running_add = 0
  for t in reversed(xrange(0, r.size)):
    if r[t] != 0:
      running_add = 0
    running_add = running_add * gamma + r[t]
    discounted_r[t] = running_add
  return discounted_r

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
    model.add(Convolution2D(8, 3, 3, border_mode='same',
                            activation='relu', init='he_uniform'))
    model.add(Flatten())
    model.add(Dense(32, activation='relu', init='he_uniform'))
    model.add(Dense(16, activation='relu', init='he_uniform'))
    model.add(Dense(number_of_inputs, activation='softmax'))
    opt = Adam(lr=learning_rate)
  model.compile(loss='categorical_crossentropy', optimizer=opt)
  if resume == True:
    model.load_weights('sokoban_checkpoint.h5')
  return model


model = learning_model()
victory = 0
#Begin training
while True:
  x = get_as_numpy(observation)
  #Predict probabilities from the Keras model
  aprob = ((model.predict(x.reshape([1, x.shape[0]]), batch_size=1).flatten()))
  xs.append(x)
  probs.append(aprob)
  action = np.random.choice(number_of_inputs, 1, p=aprob)[0]
  y = np.zeros([number_of_inputs])
  y[action] = 1
  dlogps.append(np.array(y).astype('float32') - aprob)
  observation, reward, done = perform_action(
      observation, action)  # env.step(action)
  reward_sum += reward
#   drs.append(reward)
  if done:
    episode_number += 1
    epx = np.vstack(xs)
    epdlogp = np.vstack(dlogps)
    # epr = np.vstack(drs)
    # discounted_epr = discount_rewards(epr)
    # discounted_epr -= np.mean(discounted_epr)
    # discounted_epr /= np.std(discounted_epr)
    # epdlogp *= epr #discounted_epr
    #Slowly prepare the training batch
    train_X.append(xs)
    train_y.append(np.multiply(epdlogp, reward))
    xs, dlogps, drs = [], [], []
    #Periodically update the model
    if episode_number % update_frequency == 0:
      y_train = probs + learning_rate * \
          np.squeeze(np.vstack(train_y))  # Hacky WIP
    #   y_train[y_train<0] = 0
    #   y_train[y_train>1] = 1
    #   y_train = y_train / np.sum(np.abs(y_train), axis=1, keepdims=True)
      # print 'Training Snapshot:'
    #   print train_y
    #   exit()
    #   time.sleep(.1)
      model.train_on_batch(np.squeeze(np.vstack(train_X)), y_train)
      #Clear the batch
      train_X = []
      train_y = []
      probs = []
      #Save a checkpoint of the model
      os.remove('sokoban_checkpoint.h5') if os.path.exists(
          'sokoban_checkpoint.h5') else None
      model.save_weights('sokoban_checkpoint.h5')
    #Reset the current environment nad print the current results
    running_reward = reward_sum if running_reward is None else running_reward * \
        0.99 + reward_sum * 0.01
    # print 'Environment reset imminent. Total Episode Reward: %f. Running Mean: %f' % (reward_sum, running_reward)
    reward_sum = 0
    #env.reset()
    # prev_x = None
    if reward != 0:
      if reward != -1:
        victory = victory + 1
      if episode_number % 100 == 0:
        print ('Episode %d Level %d Result: %s, Percentage Win: %f' % (
            episode_number, current_level,  ('Defeat!' if reward == -1 else 'VICTORY!'), victory))
        print observation.actions
        victory = 0
        # print aprob
    observation = loadRandomLevel()
