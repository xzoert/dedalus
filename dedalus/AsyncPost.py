import urllib.request
import threading
import json

class AsyncPost(threading.Thread):
	
	
	def __init__(self,addr,data,callback,timeout=10):
		threading.Thread.__init__(self)
		self.data=data
		self.callback=callback
		self.addr=addr
		self.aborted=False
		self.timeout=timeout
		
	def abort(self):
		self.aborted=True
		
	def run(self):
		r=None
		try:
			body=json.dumps(self.data).encode('utf-8')
			conn = urllib.request.urlopen(self.addr,body,timeout=self.timeout)
			r=conn.read().decode('utf-8')
			conn.close()
			if not self.aborted:
				r=json.loads(r)
		except Exception as e:
			self.callback(e,None)
			return
		self.callback(None,r)


