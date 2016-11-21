from PySide.QtCore import QObject, Signal

'''
for making asychronous calls being thread safe in Qt.
it exploits Qt's signal system.
usage:

	myClient.someCall(...,async=True,callback=AsyncReceiver(myCallback).callback)
	
the async receiver will call 'myCallback' on its own thread gently merged in the 
event loop. 
myCallback will receive a dictionary with the entries 'data' (the response) and 'err',
for error handling.
example:

	def myCallback(msg):
	
		if msg['err']:  # error!
			raise Exception(msg['err']) 
			
		data=msg['data']
		# ...do something with the data received
		
'''

registry={}

class AsyncReceiver(QObject):
	
	received=Signal(dict)
	
	def __init__(self,f):
		QObject.__init__(self)
		global registry
		registry[id(self)]=self
		self.received.connect(f)
	
	def callback(self,err,data):
		self.received.emit({'data':data,'err':err})
		global registry
		del registry[id(self)]

