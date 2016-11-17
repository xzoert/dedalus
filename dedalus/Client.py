import urllib.request
import json
from .AsyncPost import AsyncPost
from .Resource import Resource
from .TagCloud import TagCloud

class Client:

	def __init__(self,url='http://localhost:4541'):
		self.baseUrl=url
		conn = urllib.request.urlopen(self.baseUrl)
		conn.close()
		
	
	def call(self,addr,data,timeout=2.0,async=False,callback=None,delegate=None):
		if async:
			if delegate:
				d=delegate(callback)
				callback=d.call
			asyncPost=AsyncPost(self.baseUrl+addr,data,callback,timeout)
			asyncPost.start()
			return asyncPost
		else:
			res=self.post(addr,data,timeout)
			if delegate:
				return delegate().process(res)
			else:
				return res
			
	
	def clearDatabase(self):
		return self.post('/clear/',{})
	
	
	def getSuggestions(self,prefix,limit=20,exclude=[],minWeight=0,timeout=2.0,callback=None,async=False):
		data={'prefix':prefix,'limit':limit,'exclude':exclude}
		return self.call('/suggestions/',data,timeout,async,callback,SuggestionDelegate)
		
	
	def getResource(self,url,timeout=2.0):
		res=Resource(url)
		data=self.post('/resource/',{'url':res.url},timeout)
		if not data:
			return res
		return Resource(serverData=data)
		
	
	def getTagCloud(self,tagFilter=None,limit=40,useOr=False,timeout=2.0,async=False,callback=None):
		data={}
		if tagFilter:
			data['tags']=tagFilter.getServerData()
		data['tagCloud']=True
		data['resourceList']=False
		data['tagCloudLimit']=limit
		data['tagCloudUseOr']=useOr
		
		return self.call('/find/',data,timeout,async,callback,TagCloudDelegate)
		
	def saveResources(self,resList,timeout=5.0,async=False,callback=None):
		data=[]
		for res in resList:
			if res._saved:
				continue
			resData=res.getServerData()
			data.append(resData)
			res._saved=True
			res.isdir=resData['data']['isdir']
		if len(data)>0:
			return self.call('/load/',data,timeout,async,callback)

	def saveResource(self,res,timeout=2.0,async=False,callback=None):
		return self.saveResources([res],timeout,async,callback)
    
	def getResources(self,tagFilter=None,limit=100000,orderBy='label',offset=0,timeout=2.0,async=False,callback=None):
		data={}
		if tagFilter:
			data['tags']=tagFilter.getServerData()
		data['tagCloud']=False
		data['resourceList']=True
		data['limit']=limit
		data['offset']=offset
		data['orderBy']=orderBy
		return self.call('/find/',data,timeout,async,callback,ResourceListDelegate)
    
	def post(self,addr,data,to=2.0):
		body=json.dumps(data).encode('utf-8')
		addr=self.baseUrl+addr
		conn = urllib.request.urlopen(addr,body,timeout=to)
		r=conn.read().decode('utf-8')
		conn.close()
		r=json.loads(r)
		return r

class CallDelegate:
	
	def __init__(self,callback=None):
		self.callback=callback
		
	def call(self,err,res):
		if self.callback:
			self.callback(err,self.process(res))
	
	def process(self,res):
		return res


class TagCloudDelegate(CallDelegate):
		
	def process(self,res):
		return TagCloud(res['tagCloud'])

class ResourceListDelegate(CallDelegate):
		
	def process(self,res):
		out=[]
		for data in res['resources']:
			out.append(Resource(serverData=data))
		return out

class SuggestionDelegate(CallDelegate):
	
	def process(self,data):
		r=[]
		for item in data:
			r.append(item[0])
		return r
