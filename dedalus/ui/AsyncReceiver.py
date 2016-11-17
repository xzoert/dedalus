from PySide.QtCore import QObject, Signal


class AsyncReceiver(QObject):
	
	received=Signal(dict)
	
	def callback(self,err,data):
		self.received.emit({'data':data,'err':err})

