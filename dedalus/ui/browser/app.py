from PySide.QtCore import *
from PySide.QtGui import *
from .browserUi import Ui_MainWindow
import sys,time
from dedalus import *
from dedalus.ui import ApplicationWindow,AsyncReceiver,background,TagFilterModel,ResourceListModel,requests
import dedalus.ui.tagger.app
import subprocess,os.path



class AppMainWindow(ApplicationWindow):
	
	def __init__(self,ui):
		ApplicationWindow.__init__(self,ui,'browser')
		self.client=Client()
		self.openTaggers={}
		self.tagFilterModel=None
		self.lsitModel=None
		self.resourceListRequest=None
		self.firstShow=True
		self.tagCloudRequest=None
		self.selection=None

	def showEvent(self,e):
		if self.firstShow:
			self.firstShow=False
			self.init()
	
	def init(self):
		self.ui.tagCloudView.setColored(True)
		self.ui.tagCloudView.setMaxScale(1.2)
		self.ui.tagCloudView.setShowWeight(True)
		self.ui.tagCloudView.tagClicked.connect(self.tagClicked)
		
		
		self.tagFilterModel=TagFilterModel(self.ui.queryTable)
		self.tagFilterModel.changed.connect(self.tagFilterChanged)
		
		self.ui.searchBox.setClient(self.client)
		self.ui.searchBox.returnPressed.connect(self.searchEntered)
		
		self.listModel=ResourceListModel(self.ui.resourceTable)
		self.listModel.selectionChanged.connect(self.resourceSelectionChanged)
		self.listModel.resourceDoubleClicked.connect(self.resourceDoubleClicked)
		
		self.ui.frame.setVisible(False)
		
		self.ui.refreshButton.clicked.connect(self.refresh)
		self.ui.taggerButton.clicked.connect(self.openSelectionInTagger)
		self.ui.directoryButton.clicked.connect(self.openSelectionParent)
		self.ui.deleteButton.clicked.connect(self.deleteSelection)
		self.ui.homeButton.clicked.connect(self.tagFilterModel.clear)
		
		
		self.refresh()
		

	def deleteSelection(self):
		if not self.selection:
			return
		count=len(self.selection)
		if not count:
			return
		
		msgBox = QMessageBox()
		if count==1:
			res=self.selection[0]
			msgBox.setText('<h3>Delete '+res.forcedLabel()+' from Dedalus?</h3>')
		else:
			msgBox.setText('<h3>Delete '+str(len(self.selection))+' resources from Dedalus?</h3>')
		msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		msgBox.setDefaultButton(QMessageBox.No)
		msgBox.setIcon(QMessageBox.Warning)
		ret = msgBox.exec_()
		if ret==QMessageBox.Yes:
			urlList=[]
			for res in self.selection:
				urlList.append(res.url)
			requests.removeList(self.client,urlList,donef=self.removeDone)
		
	def relocateResource(self,res):
		dir=res.parentDirectory()
		if dir is None or not os.path.exists(dir):
			dir=QDir.homePath()
		fileName=res.fileName()
		if res.isdir:
			newPath = QFileDialog.getExistingDirectory(self,self.tr('Relocate '+fileName),dir)
		else:
			(newPath,flt) = QFileDialog.getOpenFileName(self,self.tr("Relocate "+fileName), dir, "Any file (*)")
		if newPath:
			requests.rename(self.client,res.url,newPath,callback=self.resourceRelocated)
			
	def resourceRelocated(self):
		self.refresh()

	def removeDone(self):
		self.refresh()
		

	def resourceDoubleClicked(self,res):
		if res.exists():
			self.launchFile(res.url)
		else:
			self.relocateResource(res)

	def launchFile(self,filename):
		if sys.platform == "win32":
			os.startfile(filename)
		else:
			opener ="open" if sys.platform == "darwin" else "xdg-open"
			subprocess.call([opener, filename])
		
		
	def resourceSelectionChanged(self,resList):
		self.selection=resList
		if not self.selection or len(self.selection)==0:
			self.ui.frame.setVisible(False)
		elif len(self.selection)==1:
			self.ui.frame.setVisible(True)
			res=self.selection[0]
			directory=res.parentDirectory()
			if directory and os.path.exists(directory):
				self.ui.directoryButton.setDisabled(False)
				self.ui.directoryButton.setToolTip(directory)
			else:
				self.ui.directoryButton.setDisabled(True)
				self.ui.directoryButton.setToolTip(directory)
		else:
			self.ui.frame.setVisible(True)
			self.ui.directoryButton.setDisabled(True)
		
	def openSelectionInTagger(self):
		urlList=[]
		for res in self.selection:
			urlList.append(res.url)
		tagger=dedalus.ui.tagger.app.open(urlList)
		self.openTaggers[id(tagger)]=tagger
		tagger.done.connect(self.taggerDone)
		
	def openSelectionParent(self):
		if self.selection and len(self.selection)==1:
			res=self.selection[0]
			d=res.parentDirectory()
			if d:
				self.launchFile(d)
		
	def searchEntered(self):
		self.tagFilterModel.addTag(self.ui.searchBox.text())
		QTimer.singleShot(200,self.ui.searchBox.clear)
		
		
	def tagClicked(self,tag,v):
		self.tagFilterModel.setTag(tag,v)
		
	def refresh(self):
		self.refreshTagCloud()
		self.refreshList()
		
	def tagFilterChanged(self):
		self.refresh()
		
	def refreshList(self):
		if self.resourceListRequest:
			self.resourceListRequest.abort()
		self.listModel.clear()
		self.resourceListRequest=requests.resourceList(self.client,self.tagFilterModel,donef=self.listComplete,pagef=self.addResources)
	
	
	def addResource(self,res):
		self.listModel.addResource(res)
		self.ui.resourceLabel.setText('Resources ('+str(self.listModel.rowCount(None))+')')
		
	def addResources(self,res):
		self.listModel.addResources(res)
		self.ui.resourceLabel.setText('Resources ('+str(self.listModel.rowCount(None))+')')
		
	
		
	def listComplete(self):
		self.resourceListRequest=None
		pass
		
	def refreshTagCloud(self):
		if self.tagCloudRequest:
			self.tagCloudRequest.abort()
		self.tagCloudRequest=requests.tagCloud(self.client,self.tagFilterModel,limit=50,useOr=False,callback=self.tagCloudReceived)
		
		
	def taggerDone(self,tagger):
		del self.openTaggers[id(tagger)]
		#self.refresh()



	def tagCloudReceived(self,response):
		self.tagCloudRequest=None
		if response.result:
			self.ui.tagCloudView.resetTagCloud(response.result)


	def closeEvent(self,e):
		self.saveInnerGeometry()
		
	def saveInnerGeometry(self):
		pass


		
		

def run():
	app = QApplication(sys.argv)
	background.setApp(app)
	ui = Ui_MainWindow()
	mainWindow = AppMainWindow(ui)
	ui.setupUi(mainWindow)
	mainWindow.show()
	
	app.exec_()
	sys.exit()

if __name__ == "__main__":
	run()


