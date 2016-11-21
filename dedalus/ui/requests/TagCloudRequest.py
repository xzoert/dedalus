from . import Request

class TagCloudRequest(Request):
	
	def start(self,client,tagFilter,limit,useOr,timeout,callback):
		self.client=client
		self.tagFilter=tagFilter
		self.limit=limit
		self.useOr=useOr
		self.timeout=timeout
		self.callback=callback
		self.schedule(callback,task=self.perform)
		
	def perform(self,state):
		r=self.client.getTagCloud(self.tagFilter,limit=self.limit,useOr=self.useOr,timeout=self.timeout)
		self._done()
		return r

