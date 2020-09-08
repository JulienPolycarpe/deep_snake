class Snake():
	def __init__(self, canvas, x_head, y_head, size):
		self.x = [x_head]
		self.y = [y_head]
		self.size = size
		self.canvas = canvas
		self.snake_length = 1
		self.moving_left = True
		self.moving_right = False
		self.moving_up = False
		self.moving_down = False

	def spawn(self):
		x = self.x[0]
		y = self.y[0]
		print(f"snake spawning : {x}, {y}")
		self.canvas.create_rectangle(x, y, x + self.size, y + self.size, fill = "green", tag = 'snake_head')
		self.moveHead()

	def addCell(self):
		x = self.x[-1] + 100
		y = self.y[-1]
		self.x.append(x)
		self.y.append(y)
		tag = f"snake_body_{self.snake_length}"
		print(f"{tag} spawning {x}, {y}")
		self.snake_length += 1
		self.canvas.create_rectangle(x, y, x + 100, y + 100, fill = "green", tag = tag)



	def moveLeft(self, event):
		self.moving_right = False
		self.moving_left = True
		self.moving_down = False
		self.moving_up = False



	def moveRight(self, event,):
		self.moving_right = True
		self.moving_left = False
		self.moving_down = False
		self.moving_up = False



	def moveUp(self, event):
		self.moving_right = False
		self.moving_left = False
		self.moving_down = False
		self.moving_up = True



	def moveDown(self, event):
		self.moving_right = False
		self.moving_left = False
		self.moving_down = True
		self.moving_up = False

	def moveHead(self):
		if self.moving_right:
			if (self.x[0] < SIZE - 100) and (self.cellIsOkay(self.x[0] + 100, self.y[0])):
				x_tmp, y_tmp = self.x[0], self.y[0]
				self.canvas.move("snake_head", 100, 0)
				self.x[0] += 100
				self.moveBody(x_tmp, y_tmp)
		if self.moving_left :
			if (self.x[0] > 0) and (self.cellIsOkay(self.x[0] - 100, self.y[0])):
					x_tmp, y_tmp = self.x[0], self.y[0]
					self.canvas.move("snake_head", -100, 0)
					self.x[0] -= 100
					self.moveBody(x_tmp, y_tmp)
		if self.moving_up:
			if (self.y[0] > 0) and (self.cellIsOkay(self.x[0], self.y[0] - 100)):
				x_tmp, y_tmp = self.x[0], self.y[0]
				self.canvas.move("snake_head", 0, -100)
				self.y[0] -= 100
				self.moveBody(x_tmp, y_tmp)
		if self.moving_down:
			if (self.y[0] < SIZE - 100) and (self.cellIsOkay(self.x[0], self.y[0] + 100)):
				x_tmp, y_tmp = self.x[0], self.y[0]
				self.canvas.move("snake_head", 0, 100)
				self.y[0] += 100
				self.moveBody(x_tmp, y_tmp)

		self.canvas.after(250, self.moveHead)




	def moveBody(self, old_head_x, old_head_y):
		x_tmp = old_head_x
		y_tmp = old_head_y
		snake_length_to_move = len(self.x)
		for i in range(1, snake_length_to_move):
			old_x_save = self.x[i]
			old_y_save = self.y[i]
			print(f"moving: snake_body {i}")
			tag = f"snake_body_{i}"
			self.canvas.coords(tag, x_tmp, y_tmp, x_tmp + 100, y_tmp + 100)
			self.x[i] = x_tmp
			self.y[i] = y_tmp
			x_tmp = old_x_save
			y_tmp = old_y_save



	def cellIsOkay(self, new_head_x, new_head_y):
		move_is_ok = True

		for x, y in zip(self.x, self.y):
			if (x == new_head_x) and (y == new_head_y):
				move_is_ok = False

		return move_is_ok