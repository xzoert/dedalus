from PySide.QtCore import *
from PySide.QtGui import *
from dedalus import *

class TagEntry(QLineEdit):
	
	def __init__(self,parent=None):
		QLineEdit.__init__(self,parent)
		completer = QCompleter([], self)
		completer.setCompletionColumn(0)
		completer.setMaxVisibleItems(20)
		completer.setCompletionRole(Qt.EditRole)
		completer.setCaseSensitivity(Qt.CaseInsensitive)
		completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
		self.myCompleter=completer
		self.client=None
		self.setCompleter(completer)
		self.textEdited.connect(self.searchTextChanged)
		

	def setClient(self,client):
		self.client=client
		
		
	def searchTextChanged(self,s):
		if not self.client:
			return
		
		l=self.client.getSuggestions(s)
		model=self.myCompleter.model()
		model.setStringList(l)

