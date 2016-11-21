from .Tag import Tag

class TagFilter:
	
	def __init__(self):
		self.idx={}
		self.tags=[]
		
	def clear(self):
		if len(self.tags):
			self.idx={}
			self.tags=[]
			self.changedEvent()
	
	def addTag(self,tag,value=True):
		return self.setTag(tag,value)
		
	def setTag(self,tag,value=True):
		if isinstance(tag, str):
			tag=Tag(tag)
		if tag.key not in self.idx:
			self.idx[tag.key]=FilterEntry(len(self.tags))
			self.tags.append(tag)
		if value!=self.idx[tag.key].value:
			self.idx[tag.key].value=value
			self.changedEvent()
	
	def getServerData(self):
		filt={}
		for key in self.idx:
			if self.idx[key].value:
				filt[key]=1
			else:
				filt[key]=-1
		return filt
		
	def tagValue(self,tag):
		if isinstance(tag, str):
			tag=Tag(tag)
		if tag.key in self.idx:
			return self.idx[tag.key].value
			
	def getTags(self):
		return self.tags

		
	def removeTag(self,tag):
		if isinstance(tag, str):
			tag=Tag(tag)
		if tag.key in self.idx:
			item=self.idx[tag.key]
			del self.tags[item.idx]
			del self.idx[tag.key]
			for key in self.idx:
				if self.idx[key].idx>=item.idx:
					self.idx[key].idx-=1
			self.changedEvent()
		
	def changedEvent(self):
		pass
	
	
class FilterEntry:
	
	def __init__(self,idx):
		self.value=None
		self.idx=idx
	


