import time 
from .. import background

class Request:
	
	def __init__(self):
		self._doneTime=None
		self._action=None
		
	def _done(self):
		self._doneTime=time.time()
		self._action=None

	def abort(self):
		self._done()
		if self._action:
			self._action.abort()
		
	def schedule(self,callback,task=None,state=None):
		if self._doneTime is None:
			self._action=background.schedule(callback,task=task,state=state)


