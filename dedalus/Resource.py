from .Tagging import Tagging
from .Tag import Tag
from .TagFilter import TagFilter
from .utils import *
import urllib.parse, os



class Resource:
	
	DIR=1
	FILE=2
	WEB=3
	UNKNOWN=4
	
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
			self.url='file://'+urllib.parse.quote(url)
		else:
			self.url=url
		self.path=pathFromUrl(self.url)
		
	def setLabel(self,v):
		if self.label!=v:
			self.label=v
			self._saved=False
		
	def setDescription(self,v):
		if self.description!=v:
			self.description=v
			self._saved=False
		
	def assign(self,tag):
		if isinstance(tag, str):
			tag=Tag(tag)
		if tag.key in self.taggings:
			if self.taggings[tag.key].assign():
				self._saved=False
		else:
			self.taggings[tag.key]=Tagging(self,tag)
			self._saved=False

	
	def unassign(self,tag):
		if isinstance(tag, str):
			tag=Tag(tag)
		if tag.key in self.taggings:
			if self.taggings[tag.key].unassign():
				self._saved=False


	def getType(self):
		if self.url[:7]=='file://':
			if self.isdir is None:
				fp=self.filePath()
				if fp and os.path.isdir(fp):
					return self.DIR
				else:
					return self.FILE
			elif self.isdir:
				return self.DIR
			else:
				return self.FILE
		elif self.url[:7]=='http://' or self.url[:8]=='https://':
			return self.WEB
		else:
			return self.UNKNOWN
				
	def setComment(self,tag,comment):
		self.getTagging(tag).comment=comment

	def getTagging(self,tag):
		if isinstance(tag, str):
			tag=Tag(tag)
		if tag.key in self.taggings:
			return self.taggings[tag.key]
		else:
			return Tagging(self,tag,state=Tag.NOT_ASSIGNED)
	
	def renameTag(self,tag,newTag):
		if isinstance(tag,str):
			tag=Tag(tag)
		if isinstance(newTag,str):
			newTag=Tag(newTag)
		if tag.name==newTag.name:
			return
		if newTag.key in self.taggings:
			raise Exception('Merge not yet supported')
		if tag.key in self.taggings:
			t=self.taggings[tag.key]
			del self.taggings[tag.key]
			t.tag=newTag
			self.taggings[newTag.key]=t
			self._saved=False
	
	def getTags(self):
		tags=[]
		for key in self.taggings:
			t=self.taggings[key]
			if t.state==Tag.ASSIGNED or t.state==Tag.INHERITED:
				tags.append(t.tag.name)
		return tags
	
		
		
		


	def setServerData(self,data):
		self.url=data['_url']
		self.path=pathFromUrl(self.url)
		if 'label' in data: self.label=data['label']
		if 'description' in data: self.description=data['description'] 
		if '_modified_at' in data: self.modifiedAt=data['_modified_at']/1000.0
		if '_created_at' in data: self.createdAt=data['_created_at']/1000.0
		if 'isdir' in data: self.isdir=data['isdir']
		if '_tags' in data:
			for tagData in data['_tags']:
				tagging=Tagging(self,serverData=tagData)
				self.taggings[tagging.tag.key]=tagging
		if '_template' in data and data['_template']:
			self._saved=False
		else:
			self._saved=True
		
	def isSaved(self):
		return self._saved
		
	def filePath(self):
		if self.url[:7]=='file://':
			return urllib.parse.unquote(self.url[7:])
			
	def fileName(self):
		return urllib.parse.unquote(self.path.split('/')[-2])

	def parentDirectory(self):
		if self.url[:7]=='file://':
			steps=urllib.parse.unquote(self.url[7:]).split('/')
			if steps[-1]=='':
				steps=steps[:-2]
			else:
				steps=steps[:-1]
			d='/'.join(steps)
			return d

	def exists(self):
		fp=self.filePath()
		if fp and not os.path.exists(fp):
			return False
		return True
		
	def getTaggings(self):
		res=[]
		for key in self.taggings:
			t=self.taggings[key]
			if t.state!=Tag.NOT_ASSIGNED:
				res.append(t)
		return res
		
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
			return self.fileName()
		else:
			return self.label

	def __str__(self):
		return 'dedalus.Resource ('+self.url+')'
		
		
