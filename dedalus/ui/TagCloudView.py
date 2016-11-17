from PySide.QtCore import *
from PySide.QtGui import *
from .TagCloudScene import TagCloudScene

class TagCloudView(QGraphicsView):

	tagClicked=Signal(str,int)

	def __init__(self,parent):
		QGraphicsView.__init__(self,parent)
		self.scene=TagCloudScene()
		self.setScene(self.scene)
		self.hscale=1.0
		self.vscale=1.0
		self.scene.tagClicked.connect(self.routeTagClicked)
		self.maxScale=None
		
	def setMaxScale(self,n):
		self.maxScale=n

	def routeTagClicked(self,tag,v):
		self.tagClicked.emit(tag,v)


	def resetTagCloud(self,tagCloud,resNum=None):
		self.scene.resetTagCloud(tagCloud,resNum)
		self.render()
		
	def resizeEvent(self,e):
		self.render()

	def render(self):
		self.scene.render(self.width(),self.height())
		rect=self.scene.itemsBoundingRect()
		if rect and rect.height() and rect.width():
			hscale=self.width()/rect.width()
			vscale=self.height()/rect.height()
			if vscale>hscale:
				scale=hscale
			else:
				scale=vscale
			if self.maxScale and scale>self.maxScale:
				scale=self.maxScale
			self.setScale(scale,scale)
			self.setSceneRect(rect)
		
	def setScale(self,h,v):
		self.scale(h/self.hscale,v/self.vscale)
		self.hscale=h
		self.vscale=v
