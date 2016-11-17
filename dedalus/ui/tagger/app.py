from PySide.QtCore import *
from PySide.QtGui import *
from .taggerUi import Ui_MainWindow
import sys
from dedalus import *
from dedalus.ui import ApplicationWindow



class AppMainWindow(ApplicationWindow,ResourceCollection):
	
	def __init__(self,ui):
		ApplicationWindow.__init__(self,ui,'tagger')
		ResourceCollection.__init__(self,Client())
		self.currentResource=None
		self.tagsSorted=False


	def addTag(self,tag,isNew=False):
		tag=ResourceCollection.addTag(self,tag,isNew)
		self.refreshTagCloud()
		return tag
		
	def assign(self,res,tag):
		ResourceCollection.assign(self,res,tag)
		self.refreshTagCloud()
			

	def assignToAll(self,tag):
		ResourceCollection.assignToAll(self,tag)
		self.refreshTagCloud()
	

	def unassign(self,res,tag):
		ResourceCollection.unassign(self,res,tag)
		self.refreshTagCloud()
		
	def unassignToAll(self,tag):
		ResourceCollection.unassignToAll(self,tag)
		self.refreshTagCloud()
		
		
	def addResources(self,urlList):
		for url in urlList:
			self.addResource(url)
			
	def addResource(self,url):
		res=ResourceCollection.addResource(self,url)
		self.ui.resourceList.addResource(res)
		self.tagsSorted=False
		return res
		
	def renameTag(self,tag,newTag):
		ResourceCollection.renameTag(self,tag,newTag)
		self.refreshTagCloud()


	def showEvent(self,e):
		
		self.ui.splitter.setStretchFactor(0,0)
		self.ui.splitter.setStretchFactor(1,1)
		if 'splitter' in self.prefs:
			splitterSizes=self.prefs['splitter']
			self.ui.splitter.setSizes((splitterSizes[0],splitterSizes[1]))
		if 'tagWidth' in self.prefs:
			self.ui.tableView.setTagColumnWidth(self.prefs['tagWidth'])
		else:
			self.ui.tableView.setTagColumnWidth(140)
		
		self.ui.resourceList.resourceChanged.connect(self.resourceChanged)
		
		self.ui.tableView.setCollection(self)
		self.ui.tagCloudView.setMaxScale(1)
		self.ui.tagCloudView.tagClicked.connect(self.tagClicked)
		self.ui.labelEdit.textEdited.connect(self.labelChanged)
		self.ui.labelEdit.returnPressed.connect(self.labelReturn)
		self.ui.cancelButton.clicked.connect(self.cancelClicked)
		self.ui.okButton.clicked.connect(self.okClicked)


	def okClicked(self):
		self.save()
		self.saveInnerGeometry()
		self.close()

	def cancelClicked(self):
		self.saveInnerGeometry()
		self.close()
		
		
	def closeEvent(self,e):
		self.saveInnerGeometry()
		
	def saveInnerGeometry(self):
		self.prefs['splitter']=self.ui.splitter.sizes()
		self.prefs['tagWidth']=self.ui.tableView.getTagColumnWidth()
		self.savePrefs()


	def labelReturn(self):
		self.ui.labelEdit.clearFocus()

	def labelChanged(self,s):
		if self.currentResource:
			self.currentResource.setLabel(s)
			self.ui.resourceList.relabel(self.currentResource)

		
	def tagClicked(self,tag):
		self.assign(self.currentResource,tag)
		self.ui.tableView.refresh()
		
	
	def resourceChanged(self,res):
		if not self.tagsSorted:
			self.sortTags()
			self.tagsSorted=True
		self.ui.resourceList.selectResource(res)
		self.ui.urlLabel.setResource(res)
		if self.ui.urlLabel.isFilePath():
			self.ui.urlCaption.setText('Path')
		else:
			self.ui.urlCaption.setText('Url')
		self.ui.tableView.setResource(res)
		
		self.ui.labelEdit.setText(res.forcedLabel())
		
		self.currentResource=res
		self.refreshTagCloud()
		

	def refreshTagCloud(self):
		if not self.currentResource:
			return
		f=TagFilter()
		for tag in self.currentResource.getTags():
			f.addTag(tag)
		arec=AsyncReceiver()
		arec.received.connect(self.tagCloudReceived)
		self.client.getTagCloud(f,limit=20,useOr=True,async=True,callback=arec.callback)

	def tagCloudReceived(self,msg):
		if msg['data']:
			self.ui.tagCloudView.resetTagCloud(msg['data'])
		
		
class AsyncReceiver(QObject):
	
	received=Signal(dict)
	
	def callback(self,err,data):
		self.received.emit({'data':data,'err':err})

def run():
	app = QApplication(sys.argv)
	ui = Ui_MainWindow()
	mainWindow = AppMainWindow(ui)
	ui.setupUi(mainWindow)
	mainWindow.show()
	mainWindow.addResources(sys.argv[1:])
	
	app.exec_()
	sys.exit()

if __name__ == "__main__":
	run()


