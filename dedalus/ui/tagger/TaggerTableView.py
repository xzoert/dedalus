from PySide.QtCore import *
from PySide.QtGui import *
from dedalus import *
from .TaggerTableModel import TaggerTableModel

class TaggerTableView(QTableView):
	
	def __init__(self,parent=None):
		QTableView.__init__(self,parent)
		self.tableModel=TaggerTableModel(self)
		self.setModel(self.tableModel)
		self.setColumnWidth(self.tableModel.COL_STATE,24)
		self.setColumnWidth(self.tableModel.COL_ALL,28)
		self.horizontalHeader().setStretchLastSection(True)
		
	def setCollection(self,collection):
		self.tableModel.setCollection(collection)
		
	def setTagColumnWidth(self,w):
		self.setColumnWidth(self.tableModel.COL_TAG,w)

	def getTagColumnWidth(self):
		return self.columnWidth(self.tableModel.COL_TAG)		

	def setResource(self,res):
		self.tableModel.setResource(res)
		
	def refresh(self):
		self.tableModel.refresh()
		
	def hideAllColumn(self):
		self.setColumnHidden(self.tableModel.COL_ALL,True)
		
	def showAllColumn(self):
		self.setColumnHidden(self.tableModel.COL_ALL,False)		

