from PySide.QtCore import *
from PySide.QtGui import *
from dedalus import Resource
from dedalus.ui import icons

class ResourceLabel(QLabel):
	
	def setResource(self,res):
		resType=res.getType()
		
		if resType==Resource.FILE or resType==Resource.DIR:
			text=res.filePath()
			self.showingPath=True
		else:
			text=res.url
			self.showingPath=False
		if res.exists():
			self.setText(text)
		else:
			self.setText('<font color="red">'+text+'</font>')
			
			

	def isFilePath(self):
		return self.showingPath

