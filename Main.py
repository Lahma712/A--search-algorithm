import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.core.image import Image as CImage
from kivy.uix.image import Image as BgImage
from kivy.clock import Clock
from Grid import Grid
from Algorithm import Cells, drawFrame, drawPath, drawCell
import math
from PIL import Image, ImageDraw
from io import BytesIO
kivy.require("2.0.0")

class Drw(Widget):
	Width = 500 
	Height = 500 
	GCostMult = 1 #G Cost multiplier
	HCostMult = 1 #H Cost multiplier
	Window.size = (Width, Height)
	GWidth = int(Width) 
	GHeight = int(Height * 0.9) #grid height is a little bit shorter than the full window size because of the buttons 
	Obstacle = [] #holds obstacle cells of the frame in form of columns/rows. 2D list e.g [[0,0], [4,5], .... , [column, row]]
	Explored = {} #holds explored cells of the frame in form of 2D list (same as Obstacle)
	Open = {} #holds dictionary of open cells with their GCost, HCost, FCost and parent e.g. {(0,0): [GCost, HCost, FCost, [parent]], (1,0): ...}
	Start = [5,5] #starting cell/node
	End = [10,10] #ending cell/node
	Current = Start #algorithm starts at the start node
	StartCheck = True #is later used for checking if there is a start cell
	EndCheck = True 

	BgColor = (0,0,0)
	StartColor = (255,0,0)
	EndColor = (0,255,0)
	PathColor = (0,255,255)
	GridColor = (20,20,20)
	ObsColor = (210,210, 0)
	ExpColor = (255,0,255)
	OpenColor = (100, 0, 100)
	HVCost = 10 #horizontal/vertical cost from square to square
	DCost = 14 #diagonal cost
	ParentGCost=0

	Im = Image.new("RGB", (GWidth, GHeight), BgColor)
	byte_io = BytesIO() #buffer for saving images in memory
	Im.save(byte_io, 'PNG')
	
	def __init__(self,**kwargs):
		super(Drw, self).__init__(**kwargs)
		self.CellCount = 50
		with self.canvas:
			self.check = False
			self.Bg = BgImage(pos=(0, self.Height * 0.1), size = (self.GWidth, self.GHeight)) #background image 
			self.updateFrame(self, 1)
			
			self.add = Button(text = "-", font_size =self.Height*0.05, size= (self.Width * 0.25, self.Height*0.05), pos = (self.Width *0.5, 0))
			self.sub = Button(text="+", font_size=self.Height*0.05, size= (self.Width * 0.25, self.Height*0.05), pos=(self.Width *0.5, self.Height * 0.05))
			self.add.bind(on_press= self.AddClock)
			self.add.bind(on_release = self.ClockCancel)
			self.sub.bind(on_press = self.SubClock)
			self.sub.bind(on_release = self.ClockCancel)
			self.add_widget(self.sub)
			self.add_widget(self.add)

			self.start = Button(text="start", font_size=self.Height*0.05, size = (self.Width * 0.125, self.Height*0.10), pos=(self.Width*0.875, 0))
			self.start.bind(on_press = self.StartClock)
			self.add_widget(self.start)

			self.clear = Button(text="clear", font_size=self.Height*0.05, size = (self.Width *0.125, self.Height*0.10), pos =(self.Width*0.75, 0))
			self.clear.bind(on_press = self.Clear)
			self.add_widget(self.clear)

			self.GCostInput = TextInput(text = "G Cost Mult.: 1", font_size = self.Height * 0.020, size = (self.Width * 0.25, self.Height*0.05), pos = (self.Width * 0.25,0), multiline = False)
			self.HCostInput = TextInput(text = "H Cost Mult.: 1", font_size = self.Height * 0.020, size = (self.Width * 0.25, self.Height*0.05), pos = (self.Width * 0.25,self.Height*0.05), multiline = False)
			self.HVCostInput = TextInput(text = "Hor. Cost: 10", font_size = self.Height * 0.020, size = (self.Width * 0.25, self.Height*0.05), pos = (0,0), multiline = False)
			self.DCostInput = TextInput(text = "Diag. Cost: 14", font_size = self.Height * 0.020, size = (self.Width * 0.25, self.Height*0.05), pos = (0,self.Height*0.05), multiline = False)
			self.add_widget(self.GCostInput)
			self.add_widget(self.HCostInput)
			self.add_widget(self.HVCostInput)
			self.add_widget(self.DCostInput)
			
	def ImageByte(self, instance, ImageByte): #used to store image in memory buffer
		self.Buffer = BytesIO(ImageByte)
		self.BgIm = CImage(self.Buffer, ext= 'png')
		return self.BgIm

	
	def save(self, instance):
		self.byte_io = BytesIO()
		self.Im.save(self.byte_io, 'PNG')
		with self.canvas:
			self.Bg.texture = self.ImageByte(self, self.byte_io.getvalue()).texture

	

	def AddSub(self, instance):
		self.Im = Image.new("RGB", (self.GWidth, self.GHeight), self.BgColor)  #Function that creates a new frame/Background with more cells
		self.byte_io = BytesIO()
		self.Im.save(self.byte_io, 'PNG')
		try:
			self.updateFrame(self,1)
		except:
			return
	
	def Add(self, instance):
		self.CellCount += 1
		self.AddSub(self)
		
	def Sub(self, instance):
		self.CellCount -= 1
		self.AddSub(self)
		
	def AddClock(self, instance):
		self.event = Clock.schedule_interval(self.Add, 0.01) #starts clock to continually zoom out
		self.event()

	
	def SubClock(self, instance):
		self.event = Clock.schedule_interval(self.Sub, 0.01)#starts clock to continually zoom in
		self.event()

	
	def ClockCancel(self, instance):
		self.event.cancel()#cancels clock when you release the button

	
	def StartClock(self, instance):
		self.x = 0 #variable used for clearing frame in two steps: first time clears the path (leaves obstacles), second time clears the obstacles.
		try:
			self.Startevent.cancel()
			self.Current = self.Start
			self.updateFrame(self, 2)
			self.GCostMult = int(''.join(filter(str.isdigit, self.GCostInput.text)))
			self.HCostMult = int(''.join(filter(str.isdigit, self.HCostInput.text)))
			self.HVCost = int(''.join(filter(str.isdigit, self.HVCostInput.text)))
			self.DCost = int(''.join(filter(str.isdigit, self.DCostInput.text)))
		except:
			pass
		self.ParentGCost=0
		self.Startevent = Clock.schedule_interval(self.StartFrame, 0.001)
		self.Startevent()
			

	def StartFrame(self, instance): #is called every frame, draws frames
		self.Frame = drawFrame(self.draw, self.Cells, self.Obstacle, self.Start, self.End, self.Current, self.Open, self.Explored, self.GCostMult, self.HCostMult, self.OpenColor, self.ExpColor, self.HVCost, self.DCost, self.ParentGCost) #creates cells
		self.Current = list(self.Frame[0]) #current cell 
		self.ParentGCost = self.Frame[1][0]  
		self.save(self)
		
		if self.Current == self.End: #when the algorithm has found the End node, draw the path
			self.Im = Image.open(self.byte_io)
			self.draw = ImageDraw.Draw(self.Im)
			
			while self.Current != self.Start: #retraces the path back to the start node
				self.Current = drawPath(self.draw, self.Cells, self.Explored, self.Current, self.PathColor)
				self.check = False

			drawCell(self.Cells[0][self.End[0]],self.Cells[1][self.End[1]], self.PathColor, self.draw)

			self.save(self)
			self.Startevent.cancel()

	
	def Clear(self, instance): #clears the background/frame, in two steps
		try:
			self.Startevent.cancel()
		except:
			pass

		if self.x == 0:
			self.updateFrame(self, 2)
			self.x +=1

		elif self.x == 1:
			self.updateFrame(self,3)
			
		self.Current = self.Start #reset node to start node
		return


	def updateFrame(self, instance, X): #function that is called when frame is updated, has 3 options on how to update the frame (via X)
		self.Im = Image.open(self.byte_io)
		self.draw = ImageDraw.Draw(self.Im)
		if X==1: #draws empty grid
			try:
				self.Grids = Grid(self.CellCount, self.GWidth, self.GHeight, self.draw, self.GridColor) #2D list of grid pixel coordinates eg [[0, 50, 100], [0, 100, 200]]. 1 List for x coordinates and 1 for y coordinates
				self.Cells = Cells(self.Grids[0], self.Grids[1]) #3D list of all the cell coordinates eg [ [[0,1,2,3], [5, 6, 7]....], [[0,1,2,3,4], [6,7,8,9]....] . 1st list holds x coordinate lists and 2nd list y coordinate lists
			
				drawCell(self.Cells[0][self.Start[0]], self.Cells[1][self.Start[1]], self.StartColor, self.draw)
				drawCell(self.Cells[0][self.End[0]], self.Cells[1][self.End[1]], self.EndColor , self.draw)
				for cell in self.Obstacle:
					drawCell(self.Cells[0][cell[0]], self.Cells[1][cell[1]], self.ObsColor, self.draw)
			except:
				pass

		elif X == 2: #deletes algorithm path, leaves obstacles
			for cell in self.Explored:
				drawCell(self.Cells[0][cell[0]], self.Cells[1][cell[1]], self.BgColor, self.draw)
			for cell in self.Open:
				drawCell(self.Cells[0][cell[0]], self.Cells[1][cell[1]], self.BgColor, self.draw)
			for cell in self.Obstacle:
				drawCell(self.Cells[0][cell[0]], self.Cells[1][cell[1]], self.ObsColor, self.draw)
			drawCell(self.Cells[0][self.Start[0]], self.Cells[1][self.Start[1]], self.StartColor, self.draw)
			drawCell(self.Cells[0][self.End[0]], self.Cells[1][self.End[1]], self.EndColor , self.draw)
			self.Open = {}
			self.Explored = {}

		elif X == 3: #deletes obstacles
			for cell in self.Obstacle:
				drawCell(self.Cells[0][cell[0]], self.Cells[1][cell[1]], self.BgColor, self.draw)
			self.Obstacle = []

		try:
			self.save(self)
		except:
			pass

	def Draw(self, instance, X): #draws a cell when you click on it
		self.XcellList = [x for x in self.Cells[0] if self.Xtouch+X in x][0] #finds the pixel X coordinates list containing the X coordinate you clicked with the mouse 
		self.YcellList = [x for x in self.Cells[1] if self.Ytouch+X in x][0] #finds the pixel Y coordinates list containing the Y coordinate you clicked with the mouse 
		self.cellIndexList = [self.Cells[0].index(self.XcellList), self.Cells[1].index(self.YcellList)] # produces a column/row list [column, row] of the cell you clicked with the mouse
		#3 If conditions that handle when you click on a start/end node
		if (self.Start == [] and self.cellIndexList == self.End) or (self.End ==[] and self.cellIndexList == self.Start) or (self.checkSingleClick == False and self.cellIndexList in [self.Start, self.End]):
			return
		
		elif self.Start == [] or self.End == []:
			if self.Start == []:
				self.Start = self.cellIndexList
				self.color = self.StartColor
				self.StartCheck = True
				self.Current = self.cellIndexList
				if self.Start in self.Obstacle:
					self.Obstacle.remove(self.Start)

			if self.End == []:
				self.End = self.cellIndexList
				self.color = self.EndColor
				self.EndCheck = True
				if self.End in self.Obstacle:
					self.Obstacle.remove(self.End)

		elif self.checkSingleClick == True and (self.cellIndexList == self.Start or self.cellIndexList == self.End):
			if self.cellIndexList == self.Start:
				self.color = self.BgColor
				self.Start = []
				self.StartCheck = False

			if self.cellIndexList == self.End:
				self.color = self.BgColor
				self.End = []
				self.EndCheck = False

		elif self.cellIndexList not in self.Obstacle and (self.cellIndexList != self.Start and self.cellIndexList != self.End): #checks if the cell you clicked is already clicked, if not the [column, pair] gets added to Obstacles and the cell gets colored
			
			self.Obstacle.append(self.cellIndexList)
			self.color = self.ObsColor

		elif self.checkSingleClick == True and self.cellIndexList in self.Obstacle: #if you only clicked once, and on a cell that is already clicked/activated, it gets erased again
			self.Obstacle.remove(self.cellIndexList)
			self.color = self.BgColor

		drawCell(self.XcellList,self.YcellList, self.color, self.draw) #function that draws (or erases, based on the previous conditions) the cell you clicked
		self.save(self)
		

	def onTouchFunctions(self, touch):
		self.touchpos = touch.pos #tuple that contains the X/Y coords of your mouse click
		self.Xtouch = math.floor(self.touchpos[0]) #rounds the coords down
		self.Ytouch = math.floor(abs(self.touchpos[1]-self.Height)) #inverts the Y coord. In kivy the origin (0,0) is bottom left, in PIL it is top left
		try: 
			self.Draw(self, 0) 
			super(Drw, self).on_touch_down(touch) 

		except(IndexError): #if you press exactly on a grid pixel (in between 2 cells), you would get an Index error. In that case, just move your mouseclick 1 pixel up and left
			try:
				self.Draw(self, -1)
				super(Drw, self).on_touch_down(touch) 
			except(IndexError): #if you press on a grid pixel at the border of the window, just do nothing
				super(Drw, self).on_touch_down(touch)

	def on_touch_down(self, touch): #function if you only click once
		self.checkSingleClick = True
		self.onTouchFunctions(touch)

	def on_touch_move(self, touch): #function if you click once and then start moving (with button still pressed). Is used for drawing lines
		if (self.StartCheck and self.EndCheck) == True:
			self.checkSingleClick = False
			self.onTouchFunctions(touch)


class AStar(App):
	def build(self):
		return Drw()

if __name__ == "__main__":
	AStar().run()
	