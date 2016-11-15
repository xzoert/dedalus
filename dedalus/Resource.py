from .Tagging import Tagging
from .Tag import Tag
from .utils import *
import urllib.parse, os



class Resource:
	
	def __init__(self,url=None,serverData=None):
		
		self.url=None
		self.path=None
		self.label=None
		self.decsription=None
		self.createdAt=None
		self.modifiedAt=None
		self.isdir=None
		self._saved=False
		self.taggings={}
		
		if not url and not serverData:
			raise Exception('No url and no server data')
		elif url:
			self.setUrl(url)
		elif serverData:
			self.setServerData(serverData)
			

			
	def setUrl(self,url):
		if not url:
			raise Exception('Empty URL.')
		if url[0]=='/':
			self.url='file://'+urllib.parse.quote(self.url)
		else:
			self.url=url
		self.path=pathFromUrl(self.url)
		
	def setLabel(self,v):
		if label!=v:
			self.label=v
			self._saved=False
		
	def setDescription(self,v):
		if self.description!=v:
			self.description=v
			self._saved=False
		
	def addTag(self,tagName):
		tag=Tag(tagName)
		if tag.key in self.taggings:
			self.taggings[tag.key].assign()
		else:
			self.taggings[tag.key]=Tagging(self,tag)
			
	def removeTag(self,tag):
		if tag.key in self.taggings:
			self.taggings[tag.key].unassign()
		
	def setServerData(self,data):
		self.url=data['_url']
		self.path=pathFromUrl(self.url)
		if 'label' in data: self.label=data['label']
		if 'description' in data: self.description=data['description'] 
		if 'modified_at' in data: self.modifiedAt=data['modified_at']/1000.0
		if 'created_at' in data: self.createdAt=data['created_at']/1000.0
		if 'isdir' in data: self.isdir=data['isdir']
		if '_tags' in data:
			for tagData in data['_tags']:
				tagging=Tagging(self,serverData=tagData)
				self.taggings[tagging.tag.key]=tagging
		self._saved=True
		
		
	def filePath(self):
		if self.url[:7]=='file://':
			return urllib.parse.unquote(self.url[7:])
		
		
		
		
	def getServerData(self):
		if self.isdir is None:
			fp=self.filePath()
			if fp and os.path.isdir(fp):
				isDir=1
			else:
				isDir=0
		else:
			isDir=self.isdir
		
		tags=[]
		for key in self.taggings:
			t=self.taggings[key]
			if t.state==Tag.ASSIGNED:
				tags.append([t.tag.name,t.comment])
		return {'url':self.url,'tags':tags,'data':{'label':self.forcedLabel(),'isdir':isDir}}
		
		
	def autolabel(self):
		if self.url:
			if self.url[:4]=='http':
				try:
					conn=urllib.request.urlopen(self.url,None,timeout=3.0)
					content=conn.read(10000).decode('utf-8')
					m=re.search('<title>([^<]+)',content,re.IGNORECASE)
					if m:
						label=html.unescape(m.group(1))
						label=re.sub('\s+',' ',label).strip()
						return label
				except:
					pass
					
			return self.forcedLabel()

	def forcedLabel(self):
		if not self.label:
			return urllib.parse.unquote(self.path.split('/')[-2])
		else:
			return self.label

	def __str__(self):
		return 'dedalus.Resource ('+self.url+')'
		
		
