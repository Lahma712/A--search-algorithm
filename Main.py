import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image as Bg
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import time
from Grid import Grid
from Algorithm import Cells, drawFrame, drawPath, drawMultCell
import os
import PIL
import getpass
import math
import random
from PIL import Image, ImageDraw
from kivy.uix.textinput import TextInput
host = getpass.getuser()
kivy.require("2.0.0")
from io import BytesIO
from kivy.core.image import Image as CoreImage


class Drw(Widget):
	Width = 800 #int(input("\n\nWindow width (in pixels): "))
	Height = 800 #int(input("\nWindow height (in pixels): "))
	GCostMult = 1
	HCostMult = 1
	time.sleep(1)
	Window.size = (Width, Height)
	GWidth = int(Width) 
	GHeight = int(Height * 0.9) #grid height is a little bit shorter than the full window size because of the buttons 
	Obstacle = [] #holds obstacel cells of the frame in form of columns/rows. 2D list e.g [[0,0], [4,5], .... , [column, row]]
	Explored = {}
	Open = {}
	Start = [5,5]
	End = [10,10]
	Parent = Start #first cell is equal to start
	StartCheck = True #checks if there is a start cell
	EndCheck = True #checks if there is an end cell
	Im = Image.new("RGB", (GWidth, GHeight), (200,200,200))
	byte_io = BytesIO()
	Im.save(byte_io, 'PNG')
	
	def __init__(self,**kwargs):
		super(Drw, self).__init__(**kwargs)
		self.CellCount = 50
		with self.canvas:
			self.check = False
			self.y = 0
			
			self.bg = Bg(texture = self.ImageByte(self, self.byte_io.getvalue()).texture  , pos=(0, self.Height * 0.1), size = (self.GWidth, self.GHeight))
			self.updateCanvas(self, 1)
			
            
			self.add = Button(text = "-", font_size =self.Height*0.05, size= (self.Width * 0.25, self.Height*0.05), pos = (self.Width - 0.75*self.Width, 0))
			self.sub = Button(text="+", font_size=self.Height*0.05, size= (self.Width * 0.25, self.Height*0.05), pos=(self.Width - 0.75*self.Width, self.Height * 0.05))
            
			self.add.bind(on_press= self.AddClock)
			self.add.bind(on_release = self.ClockCancel)
			self.sub.bind(on_press = self.SubClock)
			self.sub.bind(on_release = self.ClockCancel)
			self.add_widget(self.sub)
			self.add_widget(self.add)

			self.start = Button(text="start", font_size=self.Height*0.05, size = (self.Width * 0.25, self.Height*0.10), pos=(self.Width - 0.50*self.Width, 0))
			self.start.bind(on_press = self.StartClock)
			self.add_widget(self.start)

			self.clear = Button(text="clear", font_size=self.Height*0.05, size = (self.Width *0.25, self.Height*0.10), pos =(self.Width - 0.25*self.Width, 0))
			self.clear.bind(on_press = self.Clear)
			self.add_widget(self.clear)

			self.GCostInput = TextInput(text = "G Cost Mult.: 1", font_size = self.Height * 0.025, size = (self.Width * 0.25, self.Height*0.05), pos = (0,0), multiline = False)
			self.HCostInput = TextInput(text = "H Cost Mult.: 1", font_size = self.Height * 0.025, size = (self.Width * 0.25, self.Height*0.05), pos = (0,self.Height*0.05), multiline = False)

			self.add_widget(self.GCostInput)
			self.add_widget(self.HCostInput)

			self.GCostInput.bind(text = self.GCostText)
			self.HCostInput.bind(text = self.HCostText)

	def ImageByte(self, instance, ImageByte):
		self.buf = BytesIO(ImageByte)
		self.Cim = CoreImage(self.buf, ext= 'png')
		
		return self.Cim

	def GCostText(self,instance, text):
		try:
			self.GCostMult = int(''.join(filter(str.isdigit, self.GCostInput.text)))
			
		except:
			pass
		

	def HCostText(self,instance, text):
		try:
			self.HCostMult = int(''.join(filter(str.isdigit, self.HCostInput.text)))
		except:
			pass
	
	def Add(self, instance):
		self.Im = Image.new("RGB", (self.GWidth, self.GHeight), (200,200,200))
		self.byte_io = BytesIO()
		self.Im.save(self.byte_io, 'PNG')
		self.CellCount += 1
		self.updateCanvas(self,1)
		

	def Sub(self, instance):
		self.Im = Image.new("RGB", (self.GWidth, self.GHeight), (200,200,200))
		self.byte_io = BytesIO()
		self.Im.save(self.byte_io, 'PNG')
		self.CellCount -= 1
		self.updateCanvas(self,1)
		

	def AddClock(self, instance):
		self.event = Clock.schedule_interval(self.Add, 0.01) #starts clock to continually zoom out
		self.event()

	
	def SubClock(self, instance):
		self.event = Clock.schedule_interval(self.Sub, 0.01)#starts clock to continually zoom in
		self.event()

	
	def ClockCancel(self, instance):
		self.event.cancel()#cancels clock when you release the button


	def StartClock(self, instance):
		self.x = 0
		if self.y != 0:
			self.Startevent.cancel()
			self.y = 0
			self.Parent = self.Start
			self.updateCanvas(self, 2)

		self.Startevent = Clock.schedule_interval(self.StartFrame, 0.0001)
			
		self.Startevent()
			

	def StartFrame(self, instance): 
		self.y = 1
		self.Frame = drawFrame(self.draw, self.Cells, self.Obstacle, self.Start, self.End, self.Parent, self.Open, self.Explored, self.GCostMult, self.HCostMult) #creates cells
		self.Parent = list(self.Frame[0])

		self.byte_io = BytesIO()
		self.Im.save(self.byte_io, 'PNG')
		with self.canvas:
			self.bg.texture = self.ImageByte(self, self.byte_io.getvalue()).texture

			
		if self.Parent == self.End:
			self.Im = Image.open(self.byte_io)
			self.draw = ImageDraw.Draw(self.Im)
			
			
			while self.Parent != self.Start:
				self.Parent = drawPath(self.draw, self.Cells, self.Explored, self.Parent)
				self.check = False
			drawMultCell(self.Cells[0][self.End[0]],self.Cells[1][self.End[1]], (0,255,0), self.draw)
			self.byte_io = BytesIO()
			self.Im.save(self.byte_io, 'PNG')
			with self.canvas:
				self.bg.texture = self.ImageByte(self, self.byte_io.getvalue()).texture
			self.Startevent.cancel()

		

	def Clear(self, instance):
		try:
			self.Startevent.cancel()
			self.y = 0
			self.Parent = self.Start
		except:
			pass

		if self.x == 0:
			self.updateCanvas(self, 2)
			
			self.x +=1
		elif self.x == 1:
			self.updateCanvas(self,3)
			
		self.Parent = self.Start
		return


	def updateCanvas(self, instance, X):
		self.Im = Image.open(self.byte_io)
		self.draw = ImageDraw.Draw(self.Im)
		if X==1:
		 
			self.Grids = Grid(self.CellCount, self.GWidth, self.GHeight, self.draw) #2D list of grid pixel coordinates eg [[0, 50, 100], [0, 100, 200]]. 1 List for x coordinates and 1 for y coordinates
			self.Cells = Cells(self.Grids[0], self.Grids[1]) #3D list of all the cell coordinates eg [ [[0,1,2,3], [5, 6, 7]....], [[0,1,2,3,4], [6,7,8,9]....] . 1st list holds x coordinate lists and 2nd list y coordinate lists
			drawMultCell(self.Cells[0][self.Start[0]], self.Cells[1][self.Start[1]], (255,0,0), self.draw)
			drawMultCell(self.Cells[0][self.End[0]], self.Cells[1][self.End[1]], (0,255,0) , self.draw)
			
		elif X == 2:
			for cell in self.Explored:
				drawMultCell(self.Cells[0][cell[0]], self.Cells[1][cell[1]], (200,200,200), self.draw)
			for cell in self.Open:
				drawMultCell(self.Cells[0][cell[0]], self.Cells[1][cell[1]], (200,200,200), self.draw)
			drawMultCell(self.Cells[0][self.Start[0]], self.Cells[1][self.Start[1]], (255,0,0), self.draw)
			drawMultCell(self.Cells[0][self.End[0]], self.Cells[1][self.End[1]], (0,255,0) , self.draw)

			self.Open = {}
			self.Explored = {}

		elif X == 3:
			for cell in self.Obstacle:
				drawMultCell(self.Cells[0][cell[0]], self.Cells[1][cell[1]], (200,200,200), self.draw)
			self.Obstacle = []

		try:
			self.byte_io = BytesIO()
			self.Im.save(self.byte_io, 'PNG')
			with self.canvas:
				self.bg.texture = self.ImageByte(self, self.byte_io.getvalue()).texture
				
		except:
			pass

	



	def Draw(self, instance, X):
		self.XcellList = [x for x in self.Cells[0] if self.Xtouch+X in x][0] #finds the pixel X coordinates list containing the X coordinate you clicked with the mouse 
		self.YcellList = [x for x in self.Cells[1] if self.Ytouch+X in x][0] #finds the pixel Y coordinates list containing the Y coordinate you clicked with the mouse 
		self.cellIndexList = [self.Cells[0].index(self.XcellList), self.Cells[1].index(self.YcellList)] # produces a column/row list [column, row] of the cell you clicked with the mouse

		if self.Start == [] or self.End == []:
			if self.Start == []:
				self.Start = self.cellIndexList
				self.color = (255,0,0)
				self.StartCheck = True
				self.Parent = self.cellIndexList

			if self.End == []:
				self.End = self.cellIndexList
				self.color = (0,255,0)
				self.EndCheck = True

		elif self.checkSingleClick == True and (self.cellIndexList == self.Start or self.cellIndexList == self.End):
			if self.cellIndexList == self.Start:
				self.color = (200, 200,200)
				self.Start = []
				self.StartCheck = False

			if self.cellIndexList == self.End:
				self.color = (200, 200 ,200)
				self.End = []
				self.EndCheck = False


		elif self.cellIndexList not in self.Obstacle: #checks if the cell you clicked is already clicked, if not the [column, pair] gets added to CurrentCells and the cell gets colored
			self.Obstacle.append(self.cellIndexList)
			self.color = (0,0,0)

		elif self.checkSingleClick == True and self.cellIndexList in self.Obstacle: #if you only clicked once, and on a cell that is already clicked/activated, it gets erased again
			self.Obstacle.remove(self.cellIndexList)
			self.color = (200, 200, 200)

		drawMultCell(self.XcellList,self.YcellList, self.color, self.draw) #function that draws (or erases, based on the previous conditions) the cell you clicked
		self.byte_io = BytesIO()
		self.Im.save(self.byte_io, 'PNG')
		with self.canvas:
			self.bg.texture = self.ImageByte(self, self.byte_io.getvalue()).texture
        

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
	