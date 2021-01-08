from Grid import Grid
from PIL import Image, ImageDraw
import math
from io import BytesIO

def Cells(HGrid, VGrid): #function that creates dataset of the XY coords of every cell
	def cells(grid, Cells):
		for x in range(len(grid)-1):
			cell = [y for y in range(grid[x]+1, grid[x+1])]
			Cells.append(cell)
	
	XCells = []
	YCells = []
	cells(HGrid, YCells)
	cells(VGrid, XCells)
	return XCells, YCells
	


def drawCell(X,Y,color,draw): #draws cell
	for y in Y:
		for x in X:
			draw.point([x, y], color)

def distance(x, y): #calculates distance from current node to start/end node
	diag = 0
	a=x[:]
	b=y[:]
	HVCost = 10 #horizontal and vertical cost
	DCost = 14 #diagonal cost

	if a[0] == b[0]:
		return abs(a[1]-b[1]) * HVCost
	elif a[1] == b[1]:
		return abs(a[0]-b[0]) * HVCost

	elif b[0] < a[0] and b[1] < a[1]:
		while b[0] != a[0] and b[1] != a[1]:
			a[0] = a[0] -1
			a[1] = a[1] -1
			diag +=DCost
		if b[0] == a[0]:
			return abs(a[1]-b[1]) * HVCost + diag
		elif b[1] == a[1]:
			return abs(a[0]-b[0]) * HVCost + diag


	elif b[0] > a[0] and b[1] > a[1]:
		while b[0] != a[0] and b[1] != a[1]:
			a[0] = a[0] +1
			a[1] = a[1] +1
			diag +=DCost
		if b[0] == a[0]:
			return abs(a[1]-b[1]) * HVCost + diag
		elif b[1] == a[1]:
			return abs(a[0]-b[0]) * HVCost + diag

	elif b[0] < a[0] and b[1] > a[1]:
		while b[0] != a[0] and b[1] != a[1]:
			a[0] = a[0] -1
			a[1] = a[1] +1
			diag +=DCost
		if b[0] == a[0]:
			return abs(a[1]-b[1]) * HVCost + diag
		elif b[1] == a[1]:
			return abs(a[0]-b[0]) * HVCost + diag


	elif b[0] > a[0] and b[1] < a[1]:
		while b[0] != a[0] and b[1] != a[1]:
			a[0] = a[0] +1
			a[1] = a[1] -1
			diag +=DCost
		if b[0] == a[0]:
			return abs(a[1]-b[1]) * HVCost + diag
		elif b[1] == a[1]:
			return abs(a[0]-b[0]) * HVCost + diag


def cost(Cell, Start, End, GCostMult, HCostMult):#calculates cost based on distance
	GCost = distance(Start, Cell) * GCostMult
	HCost = distance(End, Cell) * HCostMult

	return GCost, HCost, GCost + HCost


def OpenDictionary(Open, OpenKey, Start, End, parent, Cells, Obstacle, Explored, source, GCostMult, HCostMult): #adds cell to Open dictionary
	if tuple(OpenKey) not in Open and ((OpenKey[0] > -1 and OpenKey[1] > -1) and (OpenKey[0] < len(Cells[0]) and OpenKey[1] < len(Cells[1]))) and (OpenKey not in Obstacle) and (OpenKey != Start) and (tuple(OpenKey) not in Explored):
		
		Open[tuple(OpenKey)] = list(cost(OpenKey, Start, End, GCostMult, HCostMult)) + [parent]
		drawCell(Cells[0][OpenKey[0]], Cells[1][OpenKey[1]], (0,0,255), source)

	return Open

def drawFrame(source, Cells, Obstacle, Start, End, Parent, Open, Explored, GCostMult, HCostMult):
	

	OpenDictionary(Open, [Parent[0]+1, Parent[1]], Start, End, Parent, Cells, Obstacle, Explored, source, GCostMult, HCostMult)
	OpenDictionary(Open, [Parent[0], Parent[1]+1], Start, End, Parent, Cells, Obstacle, Explored, source, GCostMult, HCostMult)
	OpenDictionary(Open, [Parent[0]+1, Parent[1]+1], Start, End, Parent, Cells, Obstacle, Explored, source,GCostMult, HCostMult)
	OpenDictionary(Open, [Parent[0]-1, Parent[1]], Start, End, Parent, Cells, Obstacle, Explored, source, GCostMult, HCostMult)
	OpenDictionary(Open, [Parent[0], Parent[1]-1], Start, End, Parent, Cells, Obstacle, Explored, source, GCostMult, HCostMult)
	OpenDictionary(Open, [Parent[0]-1, Parent[1]-1], Start, End, Parent, Cells, Obstacle, Explored, source, GCostMult, HCostMult)
	OpenDictionary(Open, [Parent[0]-1, Parent[1]+1], Start, End, Parent, Cells, Obstacle, Explored, source, GCostMult, HCostMult)
	OpenDictionary(Open, [Parent[0]+1, Parent[1]-1], Start, End, Parent, Cells, Obstacle, Explored, source, GCostMult, HCostMult)
	

	minFCost = 99999999
	nextCell = 0
	for item in Open.items():  #finds next cell based on lowest F Cost

		if item[1][2] < minFCost:
			minFCost = item[1][2]
			nextCell = item
		elif item[1][2] == minFCost and item[1][1] < nextCell[1][1]:
			nextCell = item


	Explored[nextCell[0]] = list(nextCell[1])
	drawCell(Cells[0][nextCell[0][0]], Cells[1][nextCell[0][1]], (255,0,255), source)
	del Open[nextCell[0]]
	return nextCell

def drawPath(source, Cells, Explored, End): #retraces path through parents 
	if tuple(End) in Explored:
		drawCell(Cells[0][Explored[tuple(End)][3][0]], Cells[1][Explored[tuple(End)][3][1]], (0,255,0), source)
		
		return list(Explored[tuple(End)][3])






