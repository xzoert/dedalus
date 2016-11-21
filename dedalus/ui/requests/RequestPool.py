import time

class RequestPool:
	
	def __init__(self,type):
		self.pool=[]
		self.type=type
		
	def get(self):
		t=time.time()
		for o in self.pool:
			if o._doneTime and t-o._doneTime>1:
				o._doneTime=None
				return o
		o=self.type()
		self.pool.append(o)
		return o
		

