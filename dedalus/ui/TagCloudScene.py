from PySide.QtCore import *
from PySide.QtGui import *

from math import *


class TagCloudScene(QGraphicsScene):
	
	tagClicked=Signal(str,int)
	
	def __init__(self):
		QGraphicsScene.__init__(self)
		self.cloud=None
		self.resCount=None
	
	
	def mousePressEvent(self,e):
		i=self.itemAt(e.scenePos())
		if i:
			if e.modifiers()==Qt.CTRL:
				v=-1
			else:
				v=1
			self.tagClicked.emit(i.toPlainText(),v)

	def reset(self,tagCloud,resCount=None):
		self.cloud=tagCloud
		self.resCount=resCount
		

	def render(self,width,height):
		
		self.clear()
		
		if not self.cloud or not width or not height:
			return
		
		tags=self.cloud.getTags()
		if not len(tags):
			return
		
		
		
		tags.sort(key=lambda x: x.name.lower())
		
		ratio=height/width
		area=0
		maxwidth=0
		items=[]
		for tag in tags:
			text=QGraphicsTextItem()
			text.setPlainText(tag.name)
			rw=tag.normWeight()
			font=QFont('Sans',8.0+10.0*rw)
			text.setFont(font)
			text.setCursor(Qt.PointingHandCursor)
			text.setToolTip(str(tag.weight))
			if self.resCount is not None and tag.weight>=resCount:
				red=100
				green=100
				blue=100
			else:
				if rw<0.5:
					f=rw*2
					red=int(140+40*f)
					green=int(140+40*f)
					blue=int(140-140*f)
				else:
					f=(rw-0.5)*2
					red=int(180-180*f)
					green=int(180+20*f)
					blue=int(0+0*f)
			text.setDefaultTextColor(QColor(red,green,blue,255))
			items.append(text)
			rect=text.boundingRect()
			area=area+rect.width()*rect.height()
			if rect.width()>maxwidth:
				maxwidth=rect.width()
		
		
		
		refwidth=sqrt((area*1.0)/ratio)
		
		top=0.0
		left=0.0
		maxh=0.0
		lineitems=[]
		for text in items:
			rect=text.boundingRect()
			if left+rect.width()>refwidth:
				# new line
				for item in lineitems:
					item['i'].setPos(item['l'],top+(maxh-item['h'])/2.0)
					self.addItem(item['i'])
				lineitems=[]
				top=top+maxh*0.7
				maxh=0.0
				left=0.0
			lineitems.append({'i':text,'l':left,'h':rect.height()})
			left=left+rect.width()
			if rect.height()>maxh:
				maxh=rect.height()
		
		for item in lineitems:
			item['i'].setPos(item['l'],top+(maxh-item['h'])/2.0)
			self.addItem(item['i'])
		
		rect=self.itemsBoundingRect()
		

