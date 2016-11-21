from . import Request
from dedalus import Resource

class RenameRequest(Request):
	
	def start(self,client,url,newUrl,timeout,callback):
		self.client=client
		self.url=url
		self.newUrl=newUrl
		self.timeout=timeout
		self.callback=callback
		self.schedule(callback,task=self.perform)
		
	def perform(self,state):
		res=Resource(self.url)
		fileName=res.fileName()
		dummy=Resource(self.newUrl)
		newRes=self.client.renameResource(res.url,dummy.url)
		if newRes.label==fileName:
			newRes.setLabel(newRes.fileName())
			self.client.saveResource(newRes)

