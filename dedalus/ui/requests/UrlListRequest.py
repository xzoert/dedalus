from . import Request
from dedalus import Resource

class UrlListRequest(Request):
	
	
	def start(self,client,urlList,timeout,pageSize,doneFunction,pageFunction):
		self.client=client
		self.urlList=urlList
		self.pageSize=pageSize
		self.timeout=timeout
		self.doneFunction=doneFunction
		self.pageFunction=pageFunction
		self.idx=0
		self.schedule(self.dispatchResources,task=self.loadResources)
		
		
	def loadResources(self,state):
		count=len(self.urlList)
		endidx=self.idx+self.pageSize
		if endidx>count:
			endidx=count
		urlList=[]
		while self.idx<count:
			urlList.append(Resource(self.urlList[self.idx]).url)
			self.idx+=1
		resources=self.client.getUrlList(urlList)
		return resources

	def dispatchResources(self,response):
		if response.err:
			self._done()
			raise response.err
		if self.pageFunction:
			try:
				self.pageFunction(response.result)
			except:
				self._done()
				raise
		if self.idx>=len(self.urlList):
			self._done()
			if self.doneFunction:
				self.doneFunction()
		else:
			self.schedule(self.dispatchResources,task=self.loadResources)
			

