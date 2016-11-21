from . import Request

class RemoveListRequest(Request):
	
	
	def start(self,client,urlList,timeout,pageSize,doneFunction,pageFunction):
		self.client=client
		self.urlList=urlList
		self.pageSize=pageSize
		self.timeout=timeout
		self.doneFunction=doneFunction
		self.pageFunction=pageFunction
		self.idx=0
		self.schedule(self.dispatchResources,task=self.removeResources)
		
		
	def removeResources(self,state):
		count=len(self.urlList)
		endidx=self.idx+self.pageSize
		if endidx>count:
			endidx=count
		r=self.client.removeUrlList(self.urlList[self.idx:endidx])
		self.idx=endidx
		
		return r

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
			self.schedule(self.dispatchResources,task=self.removeResources)
			

