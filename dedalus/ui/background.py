from PySide.QtCore import QThread, QObject, QMutex, Signal
from PySide.QtGui import QApplication
import collections,time

theThread=None


def shutdown():
	global theThread
	if theThread:
		theThread.stop()
		while theThread.isRunning():
			QThread.msleep(1)

def schedule(callback,task=None,state=None):
	global theThread
	if not theThread:
		theThread=BackgroundThread()
		theThread.start()
	return theThread.schedule(callback,task,state)

def setApp(app):
	app.lastWindowClosed.connect(shutdown)
	

class BackgroundThread(QThread):
	
	def __init__(self):
		self.actions=collections.deque()
		self.mutex=QMutex()
		self.end=False
		self.pool=ActionPool()
		QThread.__init__(self)
		
	def schedule(self,callback,task=None,state=None):
		self.mutex.lock()
		a=self.pool.get(callback,task,state)
		self.actions.append(a)
		self.mutex.unlock()
		return a
		
	def stop(self):
		self.end=True
		while(self.isRunning()):
			self.msleep(1)
		
	def run(self):
		while not self.end:
			if len(self.actions):
				self.mutex.lock()
				action=self.actions.popleft()
				self.mutex.unlock()
				if action:
					action.perform()
			self.msleep(1)


class ActionPool:
	
	def __init__(self):
		self.actions=[]
		
	def get(self,callback,task,state):
		t=time.time()
		for a in self.actions:
			if a.doneTime and t-a.doneTime>1:
				a.init(callback,task,state)
				return a
		a=Action(callback,task,state)
		self.actions.append(a)
		return a
	

class Action(QObject):
	
	done=Signal(object)
	
	def __init__(self,callback,task,state):
		QObject.__init__(self)
		self.done.connect(self._done)
		self.callback=None
		self.init(callback,task,state)

	def init(self,callback,task,state):
		if self.callback:
			self.done.disconnect(self.callback)
		self.task=task
		self.state=state
		self.callback=callback
		self.done.connect(callback)
		self.doneTime=None
		self.aborted=False
		
	def abort(self):
		print('ABORTED',self.callback)
		self.aborted=True
		
	def _done(self):
		self.doneTime=time.time()

	def perform(self):
		if self.aborted:
			self._done()
			return
		response=Response()
		if self.task:
			try:
				response.result=self.task(self.state)
			except Exception as err:
				response.err=err
		response.state=self.state
		if self.aborted:
			self._done()
			return
		self.done.emit(response)
			
			
	
	
class Response:
	
	def __init__(self):
		self.err=None
		self.result=None
		self.state=None
			

