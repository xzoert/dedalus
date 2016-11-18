from .Tag import Tag
from .utils import *

class Tagging:

	

	def __init__(self,resource,tag=None,comment=None,serverData=None,state=Tag.ASSIGNED):
		
		
		if not resource:
			raise Exception('No resource.')
		
		if tag:
			self.tag=tag
			self.resource=resource
			self.inheritedFrom=None
			self.state=state
			self.comment=comment
		elif serverData:
			data=serverData
			self.tag=Tag(data['name'])
			inh=pathFromUrl(data['inheritedFrom'])
			if inh==resource.path:
				self.inheritedFrom=None
				self.state=Tag.ASSIGNED
			else:
				self.inheritedFrom=data['inheritedFrom']
				self.state=Tag.INHERITED
			if 'comment' in data:
				self.comment=data['comment']
			
			
	def assign(self):
		if self.state!=Tag.ASSIGNED:
			self.state=Tag.ASSIGNED
			return True
		
	def unassign(self):
		if self.state==Tag.ASSIGNED:
			if self.inheritedFrom:
				self.state=Tag.INHERITED
			else:
				self.state=Tag.NOT_ASSIGNED
			return True
		
	

