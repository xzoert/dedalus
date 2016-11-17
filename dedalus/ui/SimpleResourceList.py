from PySide.QtCore import *
from PySide.QtGui import *

class SimpleResourceList(QListWidget):

	resourceChanged=Signal(object)

	def __init__(self,parent):
		QListWidget.__init__(self,parent)
		self.items={}
		#self.itemClicked.connect(self.routeResourceClicked)
		self.setSortingEnabled(True)
		self.currentItemChanged.connect(self.routeResourceChanged)

	def routeResourceChanged(self,item):
		self.resourceChanged.emit(item.res)

	def relabel(self,res):
		if res.path in self.items:
			self.items[res.path].setResource(res)

	def addResource(self,res):
		if res.path not in self.items:
			item=self.Item(res)
			self.items[res.path]=item
			self.addItem(item)
			
	def removeResource(self,res):
		if res.path in self.items:
			self.removeItem(self.items[res.path])
			del self.items[res.path]
		
	def selectResource(self,res):
		if res.path in self.items:
			item=self.items[res.path]
			self.setCurrentItem(item)

	def resetResources(self,resList):
		self.clear()
		self.items={}
		for res in resList:
			self.addResource(res)

	class Item(QListWidgetItem):
	
		def __init__(self,res):
			QListWidgetItem.__init__(self)
			self.setResource(res)
		
		def setResource(self,res):
			self.res=res
			label=self.res.forcedLabel()
			self.setText(label)
			self.setText(label)
			if not res.exists():
				self.setForeground(QBrush(QColor(255,0,0,255)))
			else:
				self.setForeground(QBrush())
			
		def getResource(self):
			return self.res
			
	

