import numpy as np
from tkinter import *
from random import randrange
#from snake import *
from utils import *
import pandas as pd
from model import *
import time
TRAINING = True	

class Game():
	def __init__(self, cell_nb, size):
		self.game_lost = False
		self.cell_nb = cell_nb
		self.size = size
		self.width = cell_nb * size
		self.middle = int(cell_nb / 2)
		self.root = Tk()
		self.canvas, self.score_widget = self.initCanvas()
		self.snake_x, self.snake_y = self.initSnake()
		self.grid = self.createGrid()
		self.apple_exists = False
		self.apple_x, self.apple_y = self.initApple()
		self.score = 0
		#print(self.grid, self.snake_x, self.snake_y)
		self.moving_left = False
		self.moving_right = True
		self.moving_up = False
		self.moving_down = False
		self.direction_int = 1
		self.grid_file = open('grids.csv', 'a')
		self.move_file = open('moves.csv', 'a')
		self.updateSnakeBody()
		self.root.mainloop()



	def initCanvas(self):
		canvas = Canvas(self.root, height = self.width, width = self.width + 400, bg = 'white')
		canvas.pack(fill = BOTH, expand = True)
		canvas.focus_set()
		for i in range(0, self.width + self.size, self.size):
			canvas.create_line([(i, 0), (i, self.width)])
			canvas.create_line([(0, i), (self.width, i)])
		canvas.create_text(self.width + 200, self.width / 2 - 100,fill="black",font="Times 40 bold",text="Score")
		score_widget = canvas.create_text(self.width + 200, self.width / 2 ,fill="black",font="Times 40 bold",text="0")
		return canvas, score_widget



	def createGrid(self):
		grid = np.zeros((self.cell_nb, self.cell_nb))

		for i in range(len(self.snake_x)):
			grid[self.snake_x[i]][self.snake_y[i]] = i + 1

		return grid



	def randomBorder(self):
		randoms_pos = set()
		for i in range(self.cell_nb):
			randoms_pos.add((i, 0))
			randoms_pos.add((0, i))
			randoms_pos.add((self.cell_nb - 1, i))
			randoms_pos.add((i, self.cell_nb - 1))

		idx = np.random.choice(len(randoms_pos))

		return list(randoms_pos)[idx]



	def initSnake(self):
		if TRAINING:
			idx1, idx2 = self.randomBorder()
		else:
			idx1, idx2 = self.middle, self.middle

		x, y =  idx1 * self.size, idx2 * self.size
		"""
		self.canvas.bind('<Left>', self.moveLeft)
		self.canvas.bind('<Right>', self.moveRight)
		self.canvas.bind('<Up>', self.moveUp)
		self.canvas.bind('<Down>', self.moveDown)
		"""
		self.canvas.create_rectangle(y, x, y + self.size, x + self.size, fill = "yellow", tag = 'snake_body_0')
		return [idx1], [idx2]



	def initApple(self):
		x, y = randrange(0, self.cell_nb), randrange(0, self.cell_nb)
		while self.grid[x][y] != 0:
			x, y = randrange(0, self.cell_nb), randrange(0, self.cell_nb)

		self.grid[x][y] = -1
		canvas_x, canvas_y = x * self.size, y * self.size

		if self.apple_exists:
			self.canvas.coords('apple', canvas_y, canvas_x, canvas_y + self.size , canvas_x + self.size)
		else:
			self.canvas.create_rectangle(canvas_y, canvas_x, canvas_y + self.size , canvas_x + self.size, fill = "red", tag = 'apple')
			self.apple_exists = True

		return x, y



	def upgradeSnake(self):
		self.score += 1
		self.canvas.itemconfigure(self.score_widget, text=str(self.score))
		x = self.snake_x[-1]
		y = self.snake_y[-1]
		tag = f"snake_body_{len(self.snake_x)}"
		lost = False
		#print(x, y, self.moving_down, self.moving_up, self.moving_right, self.moving_left)
		if not(self.moving_down) and x + 1 < self.cell_nb and self.grid[x + 1][y] == 0:
			dx = 1
			dy = 0
		elif not(self.moving_up) and x - 1 > 0 and self.grid[x - 1][y] == 0:
			dx = - 1
			dy = 0
		elif not(self.moving_right) and y + 1 < self.cell_nb and self.grid[x][y + 1] == 0:
			dx = 0
			dy = 1
		elif not(self.moving_left) and y - 1 > 0 and self.grid[x][y - 1] == 0:
			dx = 0
			dy = - 1
		else:
			self.game_lost = True

		if not self.game_lost:
			self.grid[x + dx][y + dy] = len(self.snake_x) + 1
			self.snake_x.append(x + dx)
			self.snake_y.append(y + dy)
			canvas_x, canvas_y = (x + dx) * self.size, (y + dy) * self.size
			self.canvas.create_rectangle(canvas_y, canvas_x, canvas_y + self.size , canvas_x + self.size, fill = "green", tag = tag)



	def moveLeft(self, event):
		self.moving_right = False
		self.moving_left = True
		self.moving_down = False
		self.moving_up = False
		self.direction_int = 0

	def moveRight(self, event):
		self.moving_right = True
		self.moving_left = False
		self.moving_down = False
		self.moving_up = False
		self.direction_int = 1

	def moveUp(self, event):
		self.moving_right = False
		self.moving_left = False
		self.moving_down = False
		self.moving_up = True
		self.direction_int = 2

	def moveDown(self, event):
		self.moving_right = False
		self.moving_left = False
		self.moving_down = True
		self.moving_up = False
		self.direction_int = 3

	def updateSnakeBody(self):
		dx = 0
		dy = 0

		distance_to_apple = abs(self.apple_x - self.snake_x[0]) + abs(self.apple_y - self.snake_y[0])
		old_score = self.score
		obstacle_left = 0
		obstacle_right = 0
		obstacle_up = 0
		obstacle_down = 0
		self.direction_int = np.random.randint(4)
		#x = np.reshape(self.grid, (1, len(self.grid) ** 2)).flatten()
		#y = np.concatenate((x, [self.score, distance_to_apple]))
		#self.direction_int, direction = predict(model, y)

		if self.direction_int == 0:
			self.moveLeft(None)
		elif self.direction_int == 1:
			self.moveRight(None)
		elif self.direction_int == 2:
			self.moveUp(None)
		elif self.direction_int == 3:
			self.moveDown(None)

		first_x = self.snake_x[0]
		first_y  = self.snake_y[0]

		apple_x = self.apple_x
		apple_y = self.apple_y

		last_x = self.snake_x[-1]
		last_y = self.snake_y[-1]
		#print(self.grid)

		vector = [apple_y - first_y, apple_x - first_x]
		angle = np.angle(np.complex(vector[0], vector[1]), deg = True) / 180

		if (first_y == self.cell_nb - 1) or (self.grid[first_x][first_y + 1] > 0):
			obstacle_right = 1
		if (first_y == 0) or (self.grid[first_x][first_y - 1] > 0):
			obstacle_left = 1
		if (first_x == 0) or (self.grid[first_x - 1][first_y] > 0):
			obstacle_up = 1
		if (first_x == self.cell_nb - 1) or (self.grid[first_x + 1][first_y] > 0):
			obstacle_down = 1


		if not TRAINING:
			parameters = np.reshape(np.array([obstacle_left, obstacle_right, obstacle_up, obstacle_down, angle, self.direction_int]), (1, 6))
			prediction = model.predict(parameters).flatten()[0]
			solution =  0 if prediction <= 0.5 else 1

			print(self.grid)
			print("left right up down")
			print([obstacle_left, obstacle_right, obstacle_up, obstacle_down], self.direction_int, prediction, solution)

			while solution == 0:
				self.direction_int = np.random.randint(4)

				if self.direction_int == 0:
					self.moveLeft(None)
				elif self.direction_int == 1:
					self.moveRight(None)
				elif self.direction_int == 2:
					self.moveUp(None)
				elif self.direction_int == 3:
					self.moveDown(None)

				parameters = np.reshape(np.array([obstacle_left, obstacle_right, obstacle_up, obstacle_down, angle, self.direction_int]), (1, 6))
				result = model.predict(parameters).flatten()[0]
				print(self.direction_int, result)
				solution =  0 if result <= 0.8 else 1


		if self.moving_right and first_y < self.cell_nb - 1 and self.cellIsOkay(first_x, first_y + 1):
			dx = 0
			dy = 1
		elif self.moving_left and first_y > 0 and self.cellIsOkay(first_x, first_y - 1):
			dx = 0
			dy = -1
		elif self.moving_up and first_x > 0 and self.cellIsOkay(first_x - 1, first_y):
			dx = -1
			dy = 0
		elif self.moving_down and first_x < self.cell_nb - 1 and self.cellIsOkay(first_x + 1, first_y):
			dx = 1
			dy = 0

		if dx != 0 or dy != 0:
			for i in range(len(self.snake_x) - 1, 0, -1):
				tag = f"snake_body_{i}"
				self.snake_x[i] = self.snake_x[i - 1]
				self.snake_y[i] = self.snake_y[i - 1]
				self.grid[self.snake_x[i]][self.snake_y[i]] = i + 1
				canvas_x, canvas_y = self.snake_x[i] * self.size, self.snake_y[i] * self.size
				self.canvas.coords(tag, canvas_y, canvas_x, canvas_y + self.size, canvas_x + self.size)

			self.snake_x[0] += dx
			self.snake_y[0] += dy
			canvas_x, canvas_y = self.snake_x[0] * self.size, self.snake_y[0] * self.size
			self.canvas.coords('snake_body_0', canvas_y, canvas_x, canvas_y + self.size, canvas_x + self.size)

			tmp = self.grid[first_x + dx][first_y + dy]

			self.grid[first_x + dx][first_y + dy] = 1
			self.grid[last_x][last_y] = 0

			if tmp == -1:
				self.apple_x, self.apple_y = self.initApple()
				self.upgradeSnake()

			new_distance_to_apple = abs(self.apple_x - self.snake_x[0]) + abs(self.apple_y - self.snake_y[0])
			out = 1 #1 good move, -1 bad move
			#print("\n", self.grid)
			save = np.reshape(np.array([obstacle_left, obstacle_right, obstacle_up, obstacle_down, angle, self.direction_int]), (1, 6))
			#print(old_score, self.score, new_distance_to_apple, distance_to_apple)

			if old_score > self.score:
				out = 0
			elif old_score < self.score:
				out = 1
			else:
				if new_distance_to_apple >= distance_to_apple: #going away from apple or maintaining distance
					out = 0
				else:
					out = 1

			#print("left right up down angle direct out")
			#print(obstacle_left, obstacle_right, obstacle_up, obstacle_down, angle, self.direction_int, out, model.predict(save))
			if TRAINING:
				self.saveMove(obstacle_left, obstacle_right, obstacle_up, obstacle_down, angle, self.direction_int, out)
			
			#print(self.grid, self.snake_x, self.snake_y, direction)#, distance_to_apple, new_distance_to_apple)#, predict(model, self.grid))
			"""
			if new_distance_to_apple < distance_to_apple:
				x = np.reshape(self.grid, (1, len(self.grid) ** 2)).flatten()
				y = np.concatenate((x, [self.score, new_distance_to_apple]))
				#self.saveMove([y])
			"""
		else:
			self.game_lost = True

		if self.game_lost:
			self.game_lost = False

			for i in range(self.score):
				self.canvas.delete(f"snake_body_{i + 1}")

			self.score = 0
			if TRAINING:
				idx1, idx2 = self.randomBorder()
				self.snake_x, self.snake_y = [idx1], [idx2]
			else:
				idx1, idx2, = self.middle, self.middle
				self.snake_x, self.snake_y = [self.middle], [self.middle]

			self.canvas.coords("snake_body_0", idx2 * self.size, idx1 * self.size, idx2 * self.size + self.size, idx1 * self.size + self.size)
			self.grid = self.createGrid()
			self.canvas.itemconfigure(self.score_widget, text = "0")
			self.apple_x, self.apple_y = self.initApple()
			#print(self.grid, self.snake_x, self.snake_y)

		if TRAINING:
			self.canvas.after(10, self.updateSnakeBody)
		else:
			self.canvas.after(500, self.updateSnakeBody)
		



	def cellIsOkay(self, new_head_x, new_head_y):
		move_is_ok = True

		for x, y in zip(self.snake_x, self.snake_y):
			if (x == new_head_x) and (y == new_head_y):
				move_is_ok = False

		return move_is_ok

	def finishGame(self):
		self.grid_file.close()
		self.move_file.close()

	"""
		direction:
			0 left
			1 right
			2 up
			3 down
	"""
	def saveMove(self, obstacle_left, obstacle_right, obstacle_up, obstacle_down, angle, direction_int, out):
		to_save = np.reshape(np.array([obstacle_left, obstacle_right, obstacle_up, obstacle_down, angle, direction_int]), (1, 6))
		#print(to_save, out)
		np.savetxt(self.grid_file, to_save, delimiter=';', fmt='%f')
		np.savetxt(self.move_file, [out], delimiter=';', fmt='%d')

if not TRAINING:
	model = train()
	x = Game(9, 100)
else:
	x = Game(9, 10)	