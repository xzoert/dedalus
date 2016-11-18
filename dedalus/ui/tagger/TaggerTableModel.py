from PySide.QtCore import *
from PySide.QtGui import *
from dedalus import *
import dedalus.ui.icons as icons
from .CompleterDelegate import CompleterDelegate


class TaggerTableModel(QAbstractTableModel):
	
	NotAssignedBrush=QBrush(QColor(140,140,140,255))
	AssignedBrush=QBrush(QColor(0,0,0,255))
	NotAssignedBrushNew=QBrush(QColor(140,140,140,180))
	AssignedBrushNew=QBrush(QColor(200,0,0,255))
	InheritedFont=QFont()
	InheritedFont.setItalic(True)
	NormalFont=QFont()
	AllFont=QFont()
	AllFont.setPointSizeF(AllFont.pointSizeF()*0.6)
	
	COL_TAG=2
	COL_COMMENT=3
	COL_STATE=1
	COL_ALL=0
	
	def __init__(self,view):
		QAbstractTableModel.__init__(self)
		self.headers=['','','Tag','Comment']
		self.view=view
		self.collection=None
		self.lastSuggestions=None
		self.res=None
		self.indexToEdit=None
		self.view.clicked.connect(self.itemClicked)
		
	
	
	def itemClicked(self,index):
		self.view.selectionModel().select(index, QItemSelectionModel.Deselect)
		if index.column()==self.COL_STATE:
			tags=self.collection.getTags()
			if index.row()<len(tags):
				tag=tags[index.row()]
				tagging=self.res.getTagging(tag)
				if tagging.state==Tag.ASSIGNED:
					# UNASSIGN
					self.collection.unassign(self.res,tag)
					self.refresh()
				elif tagging.state==Tag.NOT_ASSIGNED or tagging.state==Tag.INHERITED:
					# ASSIGN
					self.collection.assign(self.res,tag)
					self.refresh()
		elif index.column()==self.COL_TAG or index.column()==self.COL_COMMENT:
			self.view.edit(index)
		elif index.column()==self.COL_ALL:
			tags=self.collection.getTags()
			if index.row()<len(tags):
				tag=tags[index.row()]
				tagging=self.res.getTagging(tag)
				if tagging.state==Tag.ASSIGNED:
					self.collection.assignToAll(tag)
				else:
					self.collection.unassignToAll(tag)
			self.refresh()
			self.view.selectionModel().select(QModelIndex(), QItemSelectionModel.Clear)
			
	
	
	def setLastSuggestions(self,l):
		self.lastSuggestions=l
		
		
	def setCollection(self,collection):
		self.collection=collection
		self.completerDelegate=CompleterDelegate(self.collection,self.view)
		self.view.setItemDelegateForColumn(self.COL_TAG, self.completerDelegate)
		#self.view.setItemDelegateForColumn(self.COL_COMMENT, self.completerDelegate)
		self.completerDelegate.gotSuggestions.connect(self.setLastSuggestions)
		self.completerDelegate.suggestionChosen.connect(self.suggestionChosen)
		
	def suggestionChosen(self):
		pass
		
	def setResource(self,res):
		self.res=res
		self.refresh()
		
	def refresh(self):
		self.layoutAboutToBeChanged.emit()
		self.layoutChanged.emit()

	def data(self, index, role):
		if not index.isValid():
			return 
		if not self.collection or not self.res:
			return
		tags=self.collection.getTags()
		if index.row()==len(tags):
			# insert row
			return 
		col=index.column()
		tag=tags[index.row()]
		tagging=self.res.getTagging(tag)
		if col==self.COL_TAG:
			if tagging.state==Tag.INHERITED:
				if role == Qt.ForegroundRole: 
					if self.collection.tagIsNew(tag):
						return self.AssignedBrushNew
					else:
						return self.AssignedBrush
				elif role == Qt.FontRole: 
					return self.InheritedFont
				if role==Qt.ToolTipRole:
					return 'From: '+tagging.inheritedFrom
			elif tagging.state==Tag.ASSIGNED:
				if role == Qt.ForegroundRole: 
					if self.collection.tagIsNew(tag):
						return self.AssignedBrushNew
					else:
						return self.AssignedBrush
				elif role == Qt.FontRole: 
					if tagging.inheritedFrom:
						return self.InheritedFont
					else:
						return self.NormalFont
			elif tagging.state==Tag.NOT_ASSIGNED:
				if role == Qt.ForegroundRole: 
					if self.collection.tagIsNew(tag):
						return self.NotAssignedBrushNew
					else:
						return self.NotAssignedBrush
				elif role == Qt.FontRole: 
					return self.NormalFont
			if role==Qt.DisplayRole or role==Qt.EditRole:
				return tag.name
			if role==Qt.SizeHintRole:
				return QSize(300,20)
		elif col==self.COL_COMMENT:
			if tagging.state==Tag.INHERITED:
				if role == Qt.ForegroundRole: return self.AssignedBrush
				elif role == Qt.FontRole: return self.InheritedFont
			elif tagging.state==Tag.ASSIGNED:
				if role == Qt.ForegroundRole: return self.AssignedBrush
				elif role == Qt.FontRole: return self.NormalFont
			elif tagging.state==Tag.NOT_ASSIGNED:
				if role == Qt.ForegroundRole: return self.NotAssignedBrush
				elif role == Qt.FontRole: return self.NormalFont
			if role==Qt.DisplayRole or role==Qt.EditRole:
				return tagging.comment
			if role==Qt.SizeHintRole:
				return QSize(3000,20)
		elif col==self.COL_STATE:
			if role==Qt.DecorationRole:
				if tagging.state==Tag.ASSIGNED:
					return icons.pixmap('assigned',16,16)
				elif tagging.state==Tag.NOT_ASSIGNED:
					return icons.pixmap('not-assigned',16,16)
				elif tagging.state==Tag.INHERITED:
					return icons.pixmap('inherited',16,16)
			elif role==Qt.TextAlignmentRole:
				return Qt.AlignCenter
			if tagging.state==Tag.INHERITED and role==Qt.ToolTipRole:
				return 'From: '+tagging.inheritedFrom
		elif col==self.COL_ALL:
			if role == Qt.DisplayRole:
				tags=self.collection.getTags()
				if col>=len(tags): 
					return ''
				else: 
					tagging=self.res.getTagging(tag)
					if tagging.state==Tag.ASSIGNED:
						if self.collection.getOccurrences(tag)==self.collection.getResourceCount():
							return '*'
						else:
							return 'TO\nALL'
					else:
						if self.collection.getOccurrences(tag)==0:
							return '*'
						else:
							return 'TO\nALL'
			elif role==Qt.TextAlignmentRole:
				return Qt.AlignCenter
			elif role == Qt.FontRole: 
				return self.AllFont


	def editLastRow(self):
		tags=self.collection.getTags()
		idx=self.index(len(tags),self.COL_TAG)
		self.view.edit(idx)
		self.view.scrollTo(idx)
		
	def deferredEdit(self):
		if self.indexToEdit:
			self.view.edit(self.indexToEdit)
			self.indexToEdit=None

	def setData(self,index,value,role):
		if role==Qt.EditRole:
			if index.column()==self.COL_TAG:
				value=value.strip()
				tags=self.collection.getTags()
				if value=='':
					return False
				if index.row()==len(tags):
					#self.beginInsertRows(QModelIndex(),len(tags),len(tags))
					isNew=True
					if self.lastSuggestions and value in self.lastSuggestions:
						isNew=False
					self.collection.addTag(value,isNew)
					self.collection.assign(self.res,value)
					self.refresh()
					#self.endInsertRows()
					QTimer.singleShot(100,self.editLastRow)
					#self.view.edit(self.index(len(tags),self.COL_TAG))
				else:
					if self.collection.hasTag(value):
						self.indexToEdit=index
						QTimer.singleShot(100,self.deferredEdit)
						return False
					self.collection.renameTag(tags[index.row()],value)
					self.refresh()
			elif index.column()==self.COL_COMMENT:
				tags=self.collection.getTags()
				tag=tags[index.row()]
				self.res.setComment(tag,value)
			'''
				if index.column()==0:
					self._data[index.row()]['name']=value
				elif index.column()==1:
					self._data[index.row()]['comment']=value
				self.dataChanged.emit(index,index)
			'''
			return True
		return False
		
		
	def headerData(self, col, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return self.headers[col]
		
	'''
	def appendRow(self,parent=QModelIndex()):
		return
		count=self.getRowCount()
		self.beginInsertRows(parent,count,count)
		self._data.append({'name':'','comment':'','inheritedFrom':self._url})
		self.endInsertRows()
	'''

	def rowCount(self, parent):
		if not self.collection:
			return 0
		return len(self.collection.getTags())+1
	
	def columnCount(self, parent):
		return 4

	
	def flags(self,idx):
		tags=self.collection.getTags()
		if idx.column()==self.COL_TAG:
			tagging=None
			if idx.row()<len(tags):
				tagging=self.res.getTagging(tags[idx.row()])
			if not tagging or not tagging.inheritedFrom:
				return QAbstractTableModel.flags(self,idx) | Qt.ItemIsEditable
		elif idx.column()==self.COL_COMMENT:
			tagging=None
			if idx.row()<len(tags):
				tagging=self.res.getTagging(tags[idx.row()])
			if tagging and tagging.state==Tag.ASSIGNED:
				return QAbstractTableModel.flags(self,idx) | Qt.ItemIsEditable
			
		return QAbstractTableModel.flags(self,idx)
	

