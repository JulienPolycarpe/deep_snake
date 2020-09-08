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