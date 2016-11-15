from PySide.QtCore import *
from PySide.QtGui import *
from .tagCloudTestWindow import Ui_MainWindow
import sys
from dedalus.ui import TagCloudView
from dedalus import TagFilter, Tag, Client
import dedalus.test.env as env


class AppMainWindow(QMainWindow):
	pass
	

def tagClicked(n,v):
	print('Tag clicked',n,v)

app = QApplication(sys.argv)
ui = Ui_MainWindow()
mainWindow = AppMainWindow()
ui.setupUi(mainWindow)



mainWindow.show()

c=Client()
ui.tagCloudView.reset(c.getTagCloud())
ui.tagCloudView.tagClicked.connect(tagClicked)

app.exec_()
sys.exit()



