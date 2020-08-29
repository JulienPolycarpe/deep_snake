from tkinter import *
import random
import time

root = Tk()
root.title = "Game"
root.resizable(0,0)
root.wm_attributes("-topmost", 1)

canvas = Canvas(root, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()

class Ball:
	def __init__(self, canvas, color):
		self.canvas = canvas
		self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
		self.canvas.move(self.id, 245, 100)

	def draw(self):
		self.canvas.move(self.id, 0, -1)
		self.canvas.after(50, self.draw)




ball = Ball(canvas, "red")
ball.draw()  #Changed per Bryan Oakley's comment.
root.mainloop()