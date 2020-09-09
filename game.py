import numpy as np
from tkinter import *
from random import randrange
from snake import *
from utils import *
import pandas as pd
from model import *

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
		print(self.grid, self.snake_x, self.snake_y)
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



	def initSnake(self):
		x = self.middle * self.size
		y = self.middle * self.size
		"""
		self.canvas.bind('<Left>', self.moveLeft)
		self.canvas.bind('<Right>', self.moveRight)
		self.canvas.bind('<Up>', self.moveUp)
		self.canvas.bind('<Down>', self.moveDown)
		"""
		self.canvas.create_rectangle(x, y, x + 100, y + 100, fill = "yellow", tag = 'snake_body_0')
		return [self.middle], [self.middle]



	def initApple(self):
		x, y = randrange(0, self.cell_nb), randrange(0, self.cell_nb)
		while self.grid[x][y] != 0:
			x, y = randrange(0, self.cell_nb), randrange(0, self.cell_nb)

		self.grid[x][y] = -1
		canvas_x, canvas_y = x * self.size, y * self.size

		if self.apple_exists:
			self.canvas.coords('apple', canvas_y, canvas_x, canvas_y + 100 , canvas_x + 100)
		else:
			self.canvas.create_rectangle(canvas_y, canvas_x, canvas_y + 100 , canvas_x + 100, fill = "red", tag = 'apple')
			self.apple_exists = True

		return x, y



	def upgradeSnake(self):
		self.score += 1
		self.canvas.itemconfigure(self.score_widget, text=str(self.score))
		x = self.snake_x[-1]
		y = self.snake_y[-1]
		tag = f"snake_body_{len(self.snake_x)}"
		lost = False
		print(x, y, self.moving_down, self.moving_up, self.moving_right, self.moving_left)
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
			self.canvas.create_rectangle(canvas_y, canvas_x, canvas_y + 100 , canvas_x + 100, fill = "green", tag = tag)



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
		#self.direction_int = np.random.randint(4)
		x = np.reshape(self.grid, (1, len(self.grid) ** 2)).flatten()
		y = np.concatenate((x, [self.score, distance_to_apple]))
		self.direction_int, direction = predict(model, y)

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

		last_x = self.snake_x[-1]
		last_y = self.snake_y[-1]

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
				self.canvas.coords(tag, canvas_y, canvas_x, canvas_y + 100, canvas_x + 100)

			self.snake_x[0] += dx
			self.snake_y[0] += dy
			canvas_x, canvas_y = self.snake_x[0] * self.size, self.snake_y[0] * self.size
			self.canvas.coords('snake_body_0', canvas_y, canvas_x, canvas_y + 100, canvas_x + 100)

			tmp = self.grid[first_x + dx][first_y + dy]

			self.grid[first_x + dx][first_y + dy] = 1
			self.grid[last_x][last_y] = 0

			if tmp == -1:
				self.apple_x, self.apple_y = self.initApple()
				self.upgradeSnake()
			#new_distance_to_apple = abs(self.apple_x - self.snake_x[0]) + abs(self.apple_y - self.snake_y[0])
			print(self.grid, self.snake_x, self.snake_y, direction)#, distance_to_apple, new_distance_to_apple)#, predict(model, self.grid))
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
			self.snake_x = [self.middle]
			self.snake_y = [self.middle]
			self.canvas.coords("snake_body_0", self.middle * self.size, self.middle * self.size, self.middle * self.size + 100, self.middle * self.size + 100)
			self.grid = self.createGrid()
			self.canvas.itemconfigure(self.score_widget, text = "0")
			self.apple_x, self.apple_y = self.initApple()
			print(self.grid, self.snake_x, self.snake_y)

		self.canvas.after(250, self.updateSnakeBody)



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
	def saveMove(self, to_save):
		np.savetxt(self.grid_file, to_save, delimiter=';', fmt='%d')
		np.savetxt(self.move_file, [self.direction_int], delimiter=';', fmt='%d')

model = train()
x = Game(9, 100)