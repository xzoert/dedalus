from PySide.QtCore import *
from PySide.QtGui import *


class CompleterDelegate(QStyledItemDelegate):
	
	gotSuggestions=Signal(list)
	suggestionChosen=Signal()
	
	def __init__(self, collection, parent=None):
		self.collection=collection
		self.tagIdx=None
		QStyledItemDelegate.__init__(self,parent)
		
	def createEditor(self, parent, option, index):
		editor = QLineEdit(parent)
		editor.setStyleSheet('border: none;')
		editor.textEdited.connect(self.textEdited)
		self.tagIdx=index.row()
		self.currentIndex=index
		completer = QCompleter([], editor)
		completer.setCompletionColumn(0)
		completer.setMaxVisibleItems(20)
		completer.setCompletionRole(Qt.EditRole)
		completer.setCaseSensitivity(Qt.CaseInsensitive)
		completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
		editor.setCompleter(completer)
		editor.returnPressed.connect(self.returnPressed)
		self.currentEditor=editor
		return editor
	
	def returnPressed(self):
		self.suggestionChosen.emit()
	
	def setEditorData(self, editor, index):
		QStyledItemDelegate.setEditorData(self,editor, index)
	
	def closeEditor(self, editor, hint=None):
		QStyledItemDelegate.closeEditor(self,editor, hint)
	
	def commitData(self, editor):
		QStyledItemDelegate.commitData(self,editor)
		
	def textEdited(self,s):
		if not self.currentEditor:
			return
		
		l=self.collection.getSuggestions(s,self.tagIdx)
		c=self.currentEditor.completer()
		model=c.model()
		model.setStringList(l)
		self.gotSuggestions.emit(l)
		

