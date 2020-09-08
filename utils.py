def pxToGrid(x, cell_size):
	return int((x - x % cell_size) / cell_size)

def gridToPx(x, cell_size):
	return x * cell_size