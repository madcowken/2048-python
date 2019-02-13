
from time import sleep
from threading import Thread

import logging
logging.basicConfig(level=logging.DEBUG)

from logic import new_game, add_two, game_state, up, down, left, right
from dqn import DQNAgent

from tkinter import Tk
from render import init_grid, update_grid_cells

import numpy as np

RENDER = True
GAME_SIZE = 4
episodes = 10
action_map = {0: up, 1:down, 2:left, 3:right}
action_string = {0:"up", 1:"down", 2:"left", 3:"right"}

def newGame():
	game = new_game(GAME_SIZE)
	game = add_two(game)
	game = add_two(game)
	return game

def takeAction(game, action):
	done = False
	if action in action_map:
		game, done = action_map[action](game)
		if done:
			game = add_two(game)
	else:
		logging.error("Invalid action '{}'".format(action))

	return game, done

def normalize(n):
	return (n-1024)/2048

def preprocessState(mat):
	state = np.array(mat, dtype=np.float).reshape(1,GAME_SIZE*GAME_SIZE)
	for i in range(state.shape[1]):
		state[0][i] = (state[0][i] - 1024)/2048
	return state

def main():
	for e in range(episodes):
		_state = newGame()

		frame = 0
		while True:
			frame += 1

			state = preprocessState(_state)
			action = agent.act(state)
			if action in action_string:
				logging.debug("{}: action: {}".format(frame, action_string[action]))

			_next_state, action_done = takeAction(_state, action)
			reward = 0
			done = False

			if not action_done:
				reward += -0.5
			if game_state(_next_state) == 'win':
				reward += 1
				done = True
			elif game_state(_next_state) == 'lose':
				reward += -1
				done = True

			next_state = preprocessState(_next_state)
			agent.remember(state, action, reward, next_state, done)
			_state = _next_state

			if done:
				logging.info("{}: {}/{}".format(frame, e, episodes))
				break

def render_main(e, frame, _state, agent, grid_cells, root):
	state = preprocessState(_state)
	action = agent.act(state)
	if action in action_string:
		logging.debug("{}-{}: action: {}".format(e, frame, action_string[action]))

	_next_state, action_done = takeAction(_state, action)
	reward = 0
	done = False

	if not action_done:
		reward += -0.5
	if game_state(_next_state) == 'win':
		reward += 1
		done = True
	elif game_state(_next_state) == 'lose':
		reward += -1
		done = True

	next_state = preprocessState(_next_state)
	agent.remember(state, action, reward, next_state, done)
	_state = _next_state

	if done:
		logging.info("{}: {}/{}".format(frame, e, episodes))
		_state = newGame()
		e += 1
		frame = -1
		logging.info("{}-{}: Replaying".format(e, frame))
		agent.replay(-1)

	update_grid_cells(grid_cells, _state)

	frame += 1
	if e < episodes:
		root.after(10, render_main, e, frame, _state, agent, grid_cells, root)

if __name__ == "__main__":
	agent = DQNAgent(GAME_SIZE*GAME_SIZE, 4)

	if RENDER:
		root = Tk()
		grid_cells = init_grid(root, GAME_SIZE)

		root.after(10, render_main, 0, 0, newGame(), agent, grid_cells, root)
		root.mainloop()



		# agent.replay(10)

# if RENDER:
#
