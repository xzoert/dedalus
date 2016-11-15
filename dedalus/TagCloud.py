from .Tag import Tag

class TagCloud:

	def __init__(self,cloudData):
		self.tags=[]
		minw=None
		maxw=None
		for tagData in cloudData:
			tag=TagCloudTag(self,tagData)
			self.tags.append(tag)
			if minw is None or tag.weight<minw:
				minw=tag.weight
			if maxw is None or tag.weight>maxw:
				maxw=tag.weight
		self.maxw=maxw+0.5
		self.minw=minw-0.5

	def getTags(self):
		return self.tags

class TagCloudTag(Tag):
	
	def __init__(self,cloud,data):
		Tag.__init__(self,data['name'])
		self.weight=data['weight']
		self.cloud=cloud
		
	def normWeight(self):
		return (self.weight-self.cloud.minw)/(self.cloud.maxw-self.cloud.minw)		


