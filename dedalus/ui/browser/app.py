from PySide.QtCore import *
from PySide.QtGui import *
from .browserUi import Ui_MainWindow
import sys
from dedalus import *
from dedalus.ui import ApplicationWindow,AsyncReceiver



class AppMainWindow(ApplicationWindow):
	
	def __init__(self,ui):
		ApplicationWindow.__init__(self,ui,'browser')

	def showEvent(self,e):
		pass


	def closeEvent(self,e):
		self.saveInnerGeometry()
		
	def saveInnerGeometry(self):
		pass

		
		

def run():
	app = QApplication(sys.argv)
	ui = Ui_MainWindow()
	mainWindow = AppMainWindow(ui)
	ui.setupUi(mainWindow)
	mainWindow.show()
	
	app.exec_()
	sys.exit()

if __name__ == "__main__":
	run()


