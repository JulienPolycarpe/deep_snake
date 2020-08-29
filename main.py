from tkinter import *
from random import randint

class Snake():
	"""docstring for ClassName"""
	def __init__(self, canvas):
		self.x = []
		self.y = []
		self.canvas = canvas
		self.cell_nb = 0
		self.moving_left = False
		self.moving_right = True
		self.moving_up = False
		self.moving_down = False

	def spawn(self):
		self.x.append(randint(0, CELL_NB - 1) * 100)
		self.y.append(randint(0, CELL_NB - 1) * 100)
		self.cell_nb += 1
		x = self.x[0]
		y = self.y[0]
		print(f"snake spawning : {x}, {y}")
		self.canvas.create_rectangle(x, y, x + 100, y + 100, fill = "green", tag = 'snake_head')

	def addCell(self):
		x = self.x[-1] + 100
		y = self.y[-1]
		self.x.append(x)
		self.y.append(y)
		tag = f"snake_body_{self.cell_nb}"
		print(f"{tag} spawning {x}, {y}")
		self.cell_nb += 1
		self.canvas.create_rectangle(x, y, x + 100, y + 100, fill = "green", tag = tag)



	def moveLeft(self, event):
		"""
		print(f"pressed : {event}{repr(event.char)}")
		print(self.moving_left, self.moving_right, self.moving_down, self.moving_up)
		if (self.x[0] > 0) and (self.cellIsOkay(self.x[0] - 100, self.y[0])):
				x_tmp, y_tmp = self.x[0], self.y[0]
				self.canvas.move("snake_head", -100, 0)
				self.x[0] -= 100
				self.moveBody(x_tmp, y_tmp)
				#self.canvas.after(250, self.moveLeft)
		"""
		self.moving_right = False
		self.moving_left = True
		self.moving_down = False
		self.moving_up = False



	def moveRight(self, event,):
		"""
		if (self.x[0] < SIZE - 100) and (self.cellIsOkay(self.x[0] + 100, self.y[0])):
			x_tmp, y_tmp = self.x[0], self.y[0]
			self.canvas.move("snake_head", 100, 0)
			self.x[0] += 100
			self.moveBody(x_tmp, y_tmp)
			#self.canvas.after(250, self.moveRight)
		"""
		self.moving_right = True
		self.moving_left = False
		self.moving_down = False
		self.moving_up = False



	def moveUp(self, event):
		"""
		if (self.y[0] > 0) and (self.cellIsOkay(self.x[0], self.y[0] - 100)):
			x_tmp, y_tmp = self.x[0], self.y[0]
			self.canvas.move("snake_head", 0, -100)
			self.y[0] -= 100
			self.moveBody(x_tmp, y_tmp)
			#self.canvas.after(250, self.moveUp)
		"""
		self.moving_right = False
		self.moving_left = False
		self.moving_down = False
		self.moving_up = True



	def moveDown(self, event):
		"""
		if (self.y[0] < SIZE - 100) and (self.cellIsOkay(self.x[0], self.y[0] + 100)):
			x_tmp, y_tmp = self.x[0], self.y[0]
			self.canvas.move("snake_head", 0, 100)
			self.y[0] += 100
			self.moveBody(x_tmp, y_tmp)
			#self.canvas.after(250, self.moveDown)
		"""
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
		self.canvas.after(250, self.moveHead)




	def moveBody(self, old_head_x, old_head_y):
		x_tmp = old_head_x
		y_tmp = old_head_y
		cell_nb_to_move = len(self.x)
		for i in range(1, cell_nb_to_move):
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


				
class Apple():
	"""docstring for Apple"""
	def __init__(self):
		self.x = None
		self.y = None
		self.eaten = False

	def spawn(self, canvas):
		x1 = randint(0, CELL_NB - 1) * 100
		y1 = randint(0, CELL_NB - 1) * 100
		print(f"apple spawning : {x1}, {y1}")
		canvas.create_rectangle(x1, y1, x1 + 100, y1 + 100, fill = "red")



def create_grid(Event = None):
	for i in range(0, SIZE, 100):
		c.create_line([(i, 0), (i, SIZE)])
	for i in range(0, SIZE, 100):
		c.create_line([(0, i), (SIZE, i)])

def key(event):
	print(f"pressed : {event}")

root = Tk()
SIZE = 800
CELL_NB = int(SIZE / 100)
c = Canvas(root, height = SIZE, width = SIZE, bg = 'white')
c.pack(fill = BOTH, expand = True)
c.bind('<Configure>', create_grid)
c.focus_set()
x = Apple()
x.spawn(c)
y = Snake(c)
y.spawn()
c.bind('<Left>', y.moveLeft)
c.bind('<Right>', y.moveRight)
c.bind('<Up>', y.moveUp)
c.bind('<Down>', y.moveDown)
#c.bind('<Key>', key)
y.moveHead()
root.mainloop()