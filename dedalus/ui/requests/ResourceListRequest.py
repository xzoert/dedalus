from . import Request

class ResourceListRequest(Request):
	
	
	def start(self,client,tagFilter,limit,timeout,pageSize,doneFunction,pageFunction):
		self.client=client
		self.tagFilter=tagFilter
		self.pageSize=pageSize
		self.limit=limit
		self.timeout=timeout
		self.resources=None
		self.doneFunction=doneFunction
		self.pageFunction=pageFunction
		self.idx=0
		self.schedule(self.gotResources,task=self.getResources)
		
		
	def getResources(self,state):
		self.resources=self.client.getResources(self.tagFilter,limit=self.limit,timeout=self.timeout)
		self.idx=0
	
	def gotResources(self,response):
		if len(self.resources)>0:
			self.schedule(self.step)
		else:
			self._done()
			if self.doneFunction:
				self.doneFunction()
		
	def step(self,state):
		count=len(self.resources)
		endidx=self.idx+self.pageSize
		if endidx>count:
			endidx=count
		if self.pageFunction:
			try:
				self.pageFunction(self.resources[self.idx:endidx])
			except Exception as err:
				self._done()
				raise err
		self.idx=endidx
		if self.idx<count:
			self.schedule(self.step)
		else:
			self._done()
			if self.doneFunction:
				self.doneFunction()
			

