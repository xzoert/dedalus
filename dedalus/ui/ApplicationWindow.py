from PySide.QtCore import *
from PySide.QtGui import *

import dedalus.utils

class ApplicationWindow(QMainWindow):

	def __init__(self,ui,name):
		QMainWindow.__init__(self)
		self.ui=ui
		self.name=name
		self.geometryInitialized=0
		self.prefs=dedalus.utils.getPrefs(name)

	def savePrefs(self):
		dedalus.utils.savePrefs(self.name,self.prefs)

	def resizeEvent(self,e):
		if self.isMaximized():
			self.prefs['maximized']=True
		else:
			self.prefs['maximized']=False
			g=self.geometry()
			self.prefs['geometry']=g.getCoords()
		self.savePrefs()
		
	def moveEvent(self,e):
		if self.geometryInitialized<2:
			self.geometryInitialized=self.geometryInitialized+1
			self.restoreGeometry()
			return
		if not self.isMaximized():
			g=self.geometry()
			self.prefs['geometry']=g.getCoords()
		self.savePrefs()
	
	def restoreGeometry(self):
		if 'geometry' in self.prefs:
			geo=self.prefs['geometry']
			r=QRect()
			r.setCoords(geo[0],geo[1],geo[2],geo[3])
			self.setGeometry(r)

