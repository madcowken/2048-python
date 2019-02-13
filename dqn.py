
from collections import deque
import random

import numpy as np

import logging

from keras.models import Sequential
from keras.layers import Activation, Dense
from keras import backend as K

class DQNAgent:

	def __init__(self, state_size, action_size):
		self.state_size = state_size
		self.action_size = action_size

		self.memory = deque(maxlen=2000)

		self.gamma = 0.95 # discount rate
		self.epsilon = 1 # exploration rate
		self.epsilon_min = 0.01
		self.epsilon_decay = 0.995
		self.learning_rate = 0.001

		self.model = self._build_model()

	def _build_model(self):
		model = Sequential()
		model.add(Dense(self.action_size, activation='softmax', input_shape=(self.state_size,)))
		model.summary()

		model.compile(loss='categorical_crossentropy',
						optimizer='adam',
						metrics=['accuracy'])

		return model

	def remember(self, state, action, reward, next_state, done):
		self.memory.append((state, action, reward, next_state, done))

	def act(self, state):
		if state is None:
			raise Exception("State is None")
		if np.random.rand() <= self.epsilon:
			rand_action = random.randrange(self.action_size)
			logging.debug("rand_action: '{}' from state: '{}'".format(rand_action, state))
			return rand_action

		act_values = np.argmax(self.model.predict(state))
		if type(act_values) is np.ndarray and len(act_values) > 0:
			logging.debug("act_values: '{}' from state:{}".format(act_values, state))
			return np.argmax(act_values[0])
		else:
			logging.debug("act_values: '{}' from state: '{}'".format(act_values, state))
			return act_values

	def replay(self, batch_size):
		if batch_size < 0:
			minibatch = self.memory
		else:
			minibatch = random.sample(self.memory, batch_size)
		for state, action, reward, next_state, done in minibatch:
			target = reward
			if not done:
				target = reward + self.gamma * \
							np.amax(self.model.predict(next_state)[0])
			target_f = self.model.predict(state)
			target_f[0][action] = target
			logging.debug("Training: '{}'".format(target_f))
			self.model.fit(state, target_f, epochs=1, verbose=0)
		if self.epsilon > self.epsilon_min:
			self.epsilon *= self.epsilon_decay




