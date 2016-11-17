from .Tag import Tag

class ResourceCollection:


	def __init__(self,client):
		self.client=client
		self.resources={}
		self.tagMeta={}
		self.tags=[]

	def sortTags(self):
		self.tags.sort(key=lambda tag: tag.name)

	def getTags(self):
		return self.tags
		
	def getSuggestions(self,prefix,curTagIdx=None,limit=20):
		exclude=[]
		i=0
		for tag in self.tags:
			if i==curTagIdx:
				continue
			i=i+1
			exclude.append(tag.name)
		return self.client.getSuggestions(prefix, limit=limit, exclude=exclude)
		

	def save(self):
		tosave=[]
		for path in self.resources:
			res=self.resources[path]
			if not res._saved:
				tosave.append(res)
		if len(tosave):
			self.client.saveResources(tosave)

	def addResource(self,url):
		res=self.client.getResource(url)
		self.resources[res.path]=res
		tt=res.getTaggings()
		for t in tt:
			if t.tag.key not in self.tagMeta:
				tc=self.TagMeta(t.tag)
				self.tagMeta[t.tag.key]=tc
				tc.incr()
				self.tags.append(t.tag)
			else:
				self.tagMeta[t.tag.key].incr()
		return res
				
	def removeResource(res):
		if isinstance(res, str):
			res=Resource(res)
		if res.path in self.resources:
			res=self.resources[res.path]
			tt=res.getTaggings()
			for t in tt:
				self.tagCountes[t.tag.key].decr()
			del self.resources[res.path]
			self.resourceDeleted(res)
				
	def tagIsNew(self,tag):
		if isinstance(tag,str):
			tag=Tag(tag)
		if tag.key in self.tagMeta:
			return self.tagMeta[tag.key].isNew
		
		return False
			
	def renameTag(self,tag,newTag):
		if isinstance(tag,str):
			tag=Tag(tag)
		if isinstance(newTag,str):
			newTag=Tag(newTag)
		if tag.key in self.tagMeta:
			tmeta=self.tagMeta[tag.key]
			del self.tagMeta[tag.key]
			tmeta.tag=newTag
			self.tagMeta[newTag.key]=tmeta
			for path in self.resources:
				self.resources[path].renameTag(tag,newTag)
		for t in self.tags:
			if t.key==tag.key:
				t.name=newTag.name
				t.key=newTag.key
			
	def getOccurrences(self,tag):
		if tag.key not in self.tagMeta:
			return 0
		else:
			return self.tagMeta[tag.key].count
	
	def getResourceCount(self):
		return len(self.resources)

	def addTag(self,tag,isNew=False):
		if isinstance(tag,str):
			tag=Tag(tag)
		if tag.key not in self.tagMeta:
			self.tagMeta[tag.key]=self.TagMeta(tag,isNew)
			self.tags.append(tag)
			
	def assign(self,res,tag):
		if isinstance(tag,str):
			tag=Tag(tag)
		if tag.key not in self.tagMeta:
			self.addTag(tag)
		t=res.getTagging(tag)
		if t.state==Tag.NOT_ASSIGNED:
			self.tagMeta[tag.key].incr()
		res.assign(tag)
			

	def assignToAll(self,tag):
		if isinstance(tag,str):
			tag=Tag(tag)
		if self.getOccurrences(tag)<self.getResourceCount():
			for path in self.resources:
				res=self.resources[path]
				self.assign(res,tag)
	

	def unassign(self,res,tag):
		if isinstance(tag,str):
			tag=Tag(tag)
		t=res.getTagging(tag)
		if t.state==Tag.ASSIGNED:
			if tag.key in self.tagMeta:
				self.tagMeta[tag.key].decr()
			res.unassign(tag)
		
	def unassignToAll(self,tag):
		if isinstance(tag,str):
			tag=Tag(tag)
		if self.getOccurrences(tag)>0:
			for path in self.resources:
				res=self.resources[path]
				self.unassign(res,tag)
		
	
	class TagMeta:
		
		def __init__(self,tag,isNew=False):
			self.tag=tag
			self.count=0
			self.isNew=isNew
			
		def incr(self):
			self.count+=1
			
		def decr(self):
			self.count-=1
			


