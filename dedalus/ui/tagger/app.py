from PySide.QtCore import *
from PySide.QtGui import *
from .taggerUi import Ui_MainWindow
import sys
from dedalus import *
from dedalus.ui import ApplicationWindow,AsyncReceiver,background,requests
import threading



class AppMainWindow(ApplicationWindow,ResourceCollection):
	
	done=Signal(object)
	
	def __init__(self,ui,urlList=None):
		ApplicationWindow.__init__(self,ui,'tagger')
		ResourceCollection.__init__(self,Client())
		self.currentResource=None
		self.tagsSorted=False
		self.allTask=None
		self.firstShow=True
		self.tagCloudRequest=None
		self.urlList=urlList


	def addTag(self,tag,isNew=False):
		tag=ResourceCollection.addTag(self,tag,isNew)
		self.refreshTagCloud()
		return tag
		
	def assign(self,res,tag,refresh=True):
		ResourceCollection.assign(self,res,tag)
		if refresh:
			self.refreshTagCloud()
			

	def assignToAll(self,tag):
		if self.allTask:
			return
		if isinstance(tag,str):
			tag=Tag(tag)
		if self.getOccurrences(tag)<self.getResourceCount():
			self.allTask=AllTask(self,tag,1)
			self.allTask.done.connect(self.allTaskDone)
			self.allTask.start()
	
	

	def unassign(self,res,tag,refresh=True):
		ResourceCollection.unassign(self,res,tag)
		if refresh:
			self.refreshTagCloud()
		
	def unassignToAll(self,tag):
		if self.allTask:
			return
		if isinstance(tag,str):
			tag=Tag(tag)
		if self.getOccurrences(tag)>0:
			self.allTask=AllTask(self,tag,-1)
			self.allTask.done.connect(self.allTaskDone)
			self.allTask.start()
		
	def allTaskDone(self):
		self.allTask=None
		self.refreshTagCloud()
		self.ui.tableView.refresh()
		
	def addResources(self,urlList):
		requests.urlList(self.client,urlList,donef=self.resourceListLoaded,pagef=self.addResourcePage)
		
	def addResourcePage(self,resList):
		for res in resList:
			self.addResource(res)
			

	def isAssignedToAll(self,tag):
		if self.allTask and self.allTask.tag.name==tag.name:
			return None
		return ResourceCollection.isAssignedToAll(self,tag)
		
	def isUnassignedToAll(self,tag):
		if self.allTask and self.allTask.tag.name==tag.name:
			return None
		return ResourceCollection.isUnassignedToAll(self,tag)

	def resourceListLoaded(self):
		if not self.ui.resourceList.currentItem():
			self.ui.resourceList.setCurrentRow(0)

	def addResource(self,res):
		ResourceCollection.addResource(self,res)
		self.ui.resourceList.addResource(res)
		self.tagsSorted=False
		if self.getResourceCount()==1:
			self.ui.splitter.setSizes((0,1000))
			self.ui.tableView.hideAllColumn()
		elif self.getResourceCount()==2:
			if 'splitter' in self.prefs:
				splitterSizes=self.prefs['splitter']
				self.ui.splitter.setSizes((splitterSizes[0],splitterSizes[1]))
			else:
				self.ui.splitter.setSizes((140,1000))
			self.ui.tableView.showAllColumn()
			
		self.ui.fileLabel.setText('Files ('+str(self.getResourceCount())+')')
		return res
		
	def renameTag(self,tag,newTag):
		ResourceCollection.renameTag(self,tag,newTag)
		self.refreshTagCloud()

	def showEvent(self,e):
		if self.firstShow:
			self.firstShow=False
			self.init()

	def init(self):
		self.ui.splitter.setStretchFactor(0,0)
		self.ui.splitter.setStretchFactor(1,1)
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
		
		self.ui.urlLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
		
		if self.urlList:
			l=self.urlList
			self.urlList=None
			self.addResources(l)


	def okClicked(self):
		self.ui.okButton.setText('Saving...')
		background.schedule(self.saved,task=self.doSave)
		
	def doSave(self,state):
		self.save()
		
	def saved(self,response):
		self.close()

	def cancelClicked(self):
		self.close()
		
		
	def closeEvent(self,e):
		self.saveInnerGeometry()
		self.done.emit(self)
		
	def saveInnerGeometry(self):
		ssizes=self.ui.splitter.sizes()
		if ssizes[0]!=0:
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
			
		if self.tagCloudRequest:
			self.tagCloudRequest.abort()
		self.tagCloudRequest=requests.tagCloud(self.client,f,limit=20,useOr=True,callback=self.tagCloudReceived)

	def tagCloudReceived(self,response):
		self.tagCloudRequest=None
		if response.result:
			self.ui.tagCloudView.resetTagCloud(response.result)
		
		
class AllTask(QObject):
	
	done=Signal()
	
	def __init__(self,collection,tag,direction):
		QObject.__init__(self)
		self.resources=[]
		for path in collection.resources:
			self.resources.append(collection.resources[path])
		self.collection=collection
		self.idx=0
		self.tag=tag
		self.direction=direction
		
		
	def start(self):
		background.schedule(self.step)
		
	def step(self):
		count=len(self.resources)
		endidx=self.idx+10
		if endidx>count:
			endidx=count
		
		while self.idx<endidx:
			res=self.resources[self.idx]
			if self.direction>0:
				self.collection.assign(res,self.tag,False)
			else:
				self.collection.unassign(res,self.tag,False)
			
			self.idx+=1
		if self.idx<count:
			background.schedule(self.step)
		else:
			self.done.emit()
			
		
def open(urls):
	if len(urls)<1:
		print('No url provided, exiting.')
		return
	ui = Ui_MainWindow()
	mainWindow = AppMainWindow(ui)
	ui.setupUi(mainWindow)
	mainWindow.show()
	mainWindow.addResources(urls)
	return mainWindow
	

def run():
	if len(sys.argv)<2:
		print('No url provided, exiting.')
		return
	app = QApplication(sys.argv)
	background.setApp(app)
	ui = Ui_MainWindow()
	mainWindow = AppMainWindow(ui,sys.argv[1:])
	ui.setupUi(mainWindow)
	mainWindow.show()
	
	app.exec_()
	sys.exit()

if __name__ == "__main__":
	run()


