from .Tag import Tag

class TagFilter:
	
	def __init__(self):
		self.filter={}
		
	def addTag(self,tagName,value=True):
		tag=Tag(tagName)
		if value:
			self.filter[tag.key]=1
		else:
			self.filter[tag.key]=-1
	
	def getServerData(self):
		return self.filter
	


