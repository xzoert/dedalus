from .Tag import Tag

class TagFilter:
	
	def __init__(self):
		self.filter={}
		
	def addTag(self,tag,value=True):
		if isinstance(tag, str):
			tag=Tag(tag)
		if value:
			self.filter[tag.key]=1
		else:
			self.filter[tag.key]=-1
	
	def getServerData(self):
		return self.filter
	


