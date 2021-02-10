from math import sqrt

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




def cost(HWeight, Eucl, Manh, Cheby, ParentGCost, NewGCost, End, OpenKey):#calculates cost based on distance
	GCost = ParentGCost + NewGCost 
	HCost = ((max(abs(OpenKey[0]-End[0]), abs(OpenKey[1]-End[1]))*Cheby) + sqrt((OpenKey[0]-End[0])**2 + (OpenKey[1]-End[1])**2)*Eucl + (abs(OpenKey[0]-End[0])+abs(OpenKey[1]-End[1]))*Manh) * 10 * HWeight
	return GCost, HCost, GCost + HCost


def OpenDictionary(Open, Start, End, Explored, OpenKey, parent, Cells, Obstacle, draw, HWeight, OpenColor, Eucl, Manh, Cheby, ParentGCost, NewGCost): #adds cell to Open dictionary
	if ((OpenKey[0] > -1 and OpenKey[1] > -1) and (OpenKey[0] < len(Cells[0]) and OpenKey[1] < len(Cells[1]))) and (OpenKey not in Obstacle) and (OpenKey != Start) and (tuple(OpenKey) not in Explored):
		costs = list(cost(HWeight, Eucl, Manh, Cheby, ParentGCost, NewGCost, End, OpenKey)) + [parent]
		if tuple(OpenKey) in Open and Open[tuple(OpenKey)][0] > costs[0]: #looks if a current parent cell gives a shorter path for existing open cell, gets updated if yes.
			Open[tuple(OpenKey)] = costs
		elif tuple(OpenKey) not in Open:
			Open[tuple(OpenKey)] = costs
		drawCell(Cells[0][OpenKey[0]], Cells[1][OpenKey[1]], OpenColor, draw)
	return Open

def drawFrame(draw, Start,  End, Cells, Obstacle, Parent, Open, Explored, HWeight, OpenColor, ExpColor, Eucl, Manh,Cheby, ParentGCost):
	OpenDictionary(Open, Start, End, Explored, [Parent[0]+1, Parent[1]],  Parent, Cells, Obstacle,  draw, HWeight, OpenColor, Eucl, Manh, Cheby, ParentGCost, 10)
	OpenDictionary(Open,Start,  End, Explored,  [Parent[0], Parent[1]+1],  Parent, Cells, Obstacle, draw, HWeight, OpenColor, Eucl, Manh,Cheby,ParentGCost, 10)
	OpenDictionary(Open, Start, End, Explored, [Parent[0]+1, Parent[1]+1],  Parent, Cells, Obstacle,  draw,HWeight, OpenColor, Eucl, Manh,Cheby,ParentGCost, 14)
	OpenDictionary(Open, Start, End, Explored, [Parent[0]-1, Parent[1]],  Parent, Cells, Obstacle,  draw, HWeight, OpenColor, Eucl, Manh, Cheby,ParentGCost, 10)
	OpenDictionary(Open, Start, End, Explored, [Parent[0], Parent[1]-1],  Parent, Cells, Obstacle,  draw, HWeight, OpenColor, Eucl, Manh,Cheby,ParentGCost, 10)
	OpenDictionary(Open, Start, End, Explored, [Parent[0]-1, Parent[1]-1],  Parent, Cells, Obstacle,  draw, HWeight, OpenColor, Eucl, Manh,Cheby,ParentGCost, 14)
	OpenDictionary(Open, Start, End, Explored, [Parent[0]-1, Parent[1]+1],  Parent, Cells, Obstacle,  draw, HWeight, OpenColor, Eucl, Manh,Cheby,ParentGCost, 14)
	OpenDictionary(Open, Start, End, Explored, [Parent[0]+1, Parent[1]-1],  Parent, Cells, Obstacle,  draw, HWeight, OpenColor,Eucl, Manh,Cheby,ParentGCost, 14)
	
	minFCost = float('inf')
	nextCell = 0
	for item in Open.items():  #finds next cell based on lowest F Cost
		if item[1][2] < minFCost:
			minFCost = item[1][2]
			nextCell = item
		elif item[1][2] == minFCost and item[1][1] < nextCell[1][1]:
			nextCell = item
	Explored[nextCell[0]] = list(nextCell[1])
	drawCell(Cells[0][nextCell[0][0]], Cells[1][nextCell[0][1]], ExpColor, draw)
	del Open[nextCell[0]]
	
	return nextCell

def drawPath(draw, Cells, Explored, End, color): #retraces path through parents 
	if tuple(End) in Explored:
		drawCell(Cells[0][Explored[tuple(End)][3][0]], Cells[1][Explored[tuple(End)][3][1]], color, draw)
		
		return list(Explored[tuple(End)][3])