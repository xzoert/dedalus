from PySide.QtCore import *
from PySide.QtGui import *
from dedalus.ui import icons
from dedalus import Resource
import datetime

class ResourceListModel(QAbstractTableModel):

	COL_RESOURCE=0
	COL_CREATED=1
	COL_MODIFIED=2

	NotExistsBrush=QBrush(QColor(255,0,0,255))
	NormalBrush=QBrush(QColor(0,0,0,255))
	DateFont=QFont()
	DateFont.setPointSizeF(DateFont.pointSizeF()*0.6)
	
	selectionChanged=Signal(list)
	resourceDoubleClicked=Signal(object)

	def __init__(self,view):
		QAbstractTableModel.__init__(self)
		#self.doubleClicked.connect(self.tableDoubleClicked)
		self.view=view
		self.resources=[]
		self.headers=['label','created','modified']
		self.view.setModel(self)
		hh=self.view.horizontalHeader()
		hh.setResizeMode(self.COL_RESOURCE,QHeaderView.Stretch)
		hh.setResizeMode(self.COL_CREATED,QHeaderView.Fixed)
		hh.setResizeMode(self.COL_MODIFIED,QHeaderView.Fixed)
		hh.setVisible(False)
		self.view.setColumnWidth(self.COL_CREATED,80)
		self.view.setColumnWidth(self.COL_MODIFIED,80)
		self.view.verticalHeader().setVisible(False)
		self.selectionModel=self.view.selectionModel()
		self.selectionModel.selectionChanged.connect(self.selectionChangedHandler)
		self.view.doubleClicked.connect(self.doubleClickHandler)
		
	def doubleClickHandler(self,index):
		res=self.resources[index.row()]
		self.resourceDoubleClicked.emit(res)
		
		
	def selectionChangedHandler(self):
		r=[]
		for index in self.selectionModel.selectedIndexes():
			r.append(self.resources[index.row()])
		self.selectionChanged.emit(r)

	def headerData(self, col, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return self.headers[col]

	def clear(self):
		self.resources=[]
		self.layoutAboutToBeChanged.emit()
		self.layoutChanged.emit()
		self.selectionModel.clear()
		
	def rowCount(self,parent):
		return len(self.resources)
	
	def columnCount(self,parent):
		return 1
		
	def addResources(self,resList):
		count=len(self.resources)
		self.beginInsertRows(QModelIndex(),count,count+len(resList)-1)
		for res in resList:
			self.resources.append(res)
		self.endInsertRows()
		
		
	def addResource(self,res):
		count=len(self.resources)
		self.beginInsertRows(QModelIndex(),count,count)
		self.resources.append(res)
		self.endInsertRows()
			
	def data(self, index, role):
		if not index.isValid():
			return 
		res=self.resources[index.row()]
		if index.column()==self.COL_RESOURCE:
			if role==Qt.DecorationRole:
				type=res.getType()
				if type==Resource.FILE:
					return icons.pixmap('typefile',16,16)
				elif type==Resource.DIR:
					return icons.pixmap('typedir',16,16)
				elif type==Resource.WEB:
					return icons.pixmap('typeweb',16,16)
				else:
					return
			elif role==Qt.DisplayRole:
				return res.forcedLabel()
			elif role == Qt.ForegroundRole: 
				if res.exists():
					return self.NormalBrush
				else:
					return self.NotExistsBrush
			elif role == Qt.ToolTipRole:
				return res.url
		elif index.column()==self.COL_CREATED:
			if role==Qt.DisplayRole:
				return datetime.datetime.fromtimestamp(res.createdAt).strftime('%Y-%m-%d %H:%M:%S')
			elif role == Qt.FontRole: 
				return self.DateFont
		elif index.column()==self.COL_MODIFIED:
			if role==Qt.DisplayRole:
				return datetime.datetime.fromtimestamp(res.modifiedAt).strftime('%Y-%m-%d %H:%M:%S')
			elif role == Qt.FontRole: 
				return self.DateFont
			
		
'''
		
		
	def deleteResource(self,res):
		self.app.deleteResource(res)
		
	def reset(self,resources):
		self.resources=resources
		self.reinit()
		
	def openResource(self,res):
		filename=res['_url']
		self.launchFile(filename)
		
	def launchFile(self,filename):
		if sys.platform == "win32":
			os.startfile(filename)
		else:
			opener ="open" if sys.platform == "darwin" else "xdg-open"
			subprocess.call([opener, filename])

	def tableDoubleClicked(self,idx):
		if idx.column()==self.COL_RESOURCE:
			res=self.resources[idx.row()]
			if self.fileExists(res):
				self.openResource(res)
			else:
				self.app.relocateResource(res,self.getDirectory(res))

		

	def getDirectory(self,res):
		if res['_url'][:7]=='file://':
			steps=urllib.parse.unquote(res['_url'][7:]).split('/')
			if steps[-1]=='':
				steps=steps[:-2]
			else:
				steps=steps[:-1]
			d='/'.join(steps)
			if os.path.exists(d):
				return d
	
	def fileExists(self,res):
		if res['_url'][:7]=='file://':
			fpath=urllib.parse.unquote(res['_url'][7:])
			return os.path.exists(fpath)
		else:
			return True
	
			
	def reinit(self):
		self.view.clear()
		self.view.setColumnCount(5)
		self.view.setRowCount(len(self.resources))
		self.view.setColumnWidth(self.COL_DIRECTORY,40)
		self.view.setColumnWidth(self.COL_TAGME,40)
		self.view.setColumnWidth(self.COL_DELETE,40)
		self.view.setColumnWidth(self.COL_TYPE,24)
		hh=self.view.horizontalHeader()
		hh.setResizeMode(self.COL_RESOURCE,QHeaderView.Stretch)
		hh.setResizeMode(self.COL_DIRECTORY,QHeaderView.Fixed)
		hh.setResizeMode(self.COL_TAGME,QHeaderView.Fixed)
		hh.setResizeMode(self.COL_DELETE,QHeaderView.Fixed)
		i=0
		for res in self.resources:
			rlabel=res['label']
			if not rlabel:
				rlabel=urllib.parse.unquote(res['_url'].split('/')[-1])
			
			label=QLabel(rlabel)
			if i%2:
				style='background-color: #FFFFDD; '
			else:
				style='background-color: #FFFFFF; '
			style=style+'padding-left: 5px; '
			label.setToolTip(res['_url'])
			if not self.fileExists(res):
				style=style+'color: #FF0000;'
			label.setStyleSheet(style)
			label.setCursor(Qt.PointingHandCursor)
			self.view.setCellWidget(i,self.COL_RESOURCE,label)
			
			d=self.getDirectory(res)
			if d:
				self.view.setCellWidget(i,self.COL_DIRECTORY,DirectoryButton(self,res))

			self.view.setCellWidget(i,self.COL_TAGME,TaggerButton(self,res))

			self.view.setCellWidget(i,self.COL_DELETE,DeleteButton(self,res))
			
			if res['_url'][:7]=='file://':
				fpath=urllib.parse.unquote(res['_url'][7:])
				if res['isdir']==1:
					ico=QPixmap(":/dedalus/typedir.png")
				elif res['isdir']==0:
					ico=QPixmap(":/dedalus/typefile.png")
				elif os.path.isfile(fpath):
					ico=QPixmap(":/dedalus/typefile.png")
				elif os.path.isdir(fpath):
					ico=QPixmap(":/dedalus/typedir.png")
				else:
					ico=None
						
			else:
				ico=QPixmap(":/dedalus/typeweb.png")
			
			if ico:
				label=QLabel()
				label.setPixmap(ico)
				label.setAlignment(Qt.AlignCenter)
				self.view.setCellWidget(i,self.COL_TYPE,label)
					

			i=i+1
			
		#self.view.setAlternatingRowColors(True)
		#self.view.setStyleSheet('alternate-background-color: yellow; background-color: white;')

	def openDirectory(self,res):
		d=self.getDirectory(res)
		if d:
			self.launchFile(d)
'''
