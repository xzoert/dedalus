from PySide.QtCore import *
from PySide.QtGui import *
from dedalus import *
from dedalus.ui import icons


class TagFilterModel(QAbstractTableModel,TagFilter):
	
	COL_DELETE=2
	COL_TOGGLE=0
	COL_TAG=1
	
	NotBrush=QBrush(QColor(140,140,140,255))
	
	changed=Signal()
	
	def __init__(self,view):
		QAbstractTableModel.__init__(self)
		TagFilter.__init__(self)
		self.view=view
		self.view.setModel(self)
		hh=self.view.horizontalHeader()
		hh.setResizeMode(self.COL_TAG,QHeaderView.Stretch)
		hh.setResizeMode(self.COL_DELETE,QHeaderView.Fixed)
		hh.setResizeMode(self.COL_TOGGLE,QHeaderView.Fixed)
		self.view.setColumnWidth(self.COL_DELETE,24)
		self.view.setColumnWidth(self.COL_TOGGLE,24)
		self.view.setSelectionMode(QAbstractItemView.NoSelection);
		self.view.clicked.connect(self.itemClicked)
		
		
	def clear(self):
		TagFilter.clear(self)
		
	def itemClicked(self,idx):
		if idx.column()==self.COL_DELETE:
			self.removeTag(self.tags[idx.row()])
		elif idx.column()==self.COL_TOGGLE:
			self.toggleTag(self.tags[idx.row()])
	
	def toggleTag(self,tag):
		if self.tagValue(tag):
			self.setTag(tag,False)
		else:
			self.setTag(tag,True)
	
	def rowCount(self,parent):
		return len(self.getTags())
	
	def columnCount(self,parent):
		return 3
	
	def data(self, index, role):
		if not index.isValid():
			return 
		tag=self.tags[index.row()]
		if index.column()==self.COL_DELETE:
			if role==Qt.DecorationRole:
				return icons.pixmap("delete",16,16)
		elif index.column()==self.COL_TOGGLE:
			if role==Qt.DecorationRole:
				if self.tagValue(tag):
					return icons.pixmap("assigned",16,16)
				else:
					return icons.pixmap("not-assigned",16,16)
					
		elif index.column()==self.COL_TAG:
			if role==Qt.DisplayRole:
				if not self.tagValue(tag):
					return tag.name
				else:
					return tag.name
			
	def refresh(self):
		self.layoutAboutToBeChanged.emit()
		self.layoutChanged.emit()

	def changedEvent(self):
		self.refresh()
		self.changed.emit()

