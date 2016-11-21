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
	
	
	def getSuggestions(self,prefix,limit=20,exclude=[],minWeight=0,timeout=5.0,callback=None,async=False):
		data={'prefix':prefix,'limit':limit,'exclude':exclude}
		return self.call('/suggestions/',data,timeout,async,callback,SuggestionDelegate)
		
	
	def removeResource(self,url):
		return self.post('/remove/',{'url':url},2.0)
		
	def removeUrlList(self,urlList):
		return self.post('/removeList/',urlList,2.0)
	
	def getResource(self,url,timeout=5.0,async=False,callback=None):
		res=Resource(url)
		data={'url':res.url}
		return self.call('/resource/',data,timeout,async,callback,ResourceDelegate)
		
	def getUrlList(self,urlList,timeout=5.0):
		result=self.post('/urls/',urlList,timeout)
		resList=[]
		for data in result:
			resList.append(Resource(serverData=data))
		return resList
		
	
	def getTagCloud(self,tagFilter=None,limit=40,useOr=False,timeout=5.0,async=False,callback=None):
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
		
	def renameResource(self,url,newUrl,renameDescendants=True,timeout=2.0):
		data=self.post('/rename/',{'url':url,'newUrl':newUrl,'renameDescendants':renameDescendants})
		return Resource(serverData=data)
    
	def getResources(self,tagFilter=None,limit=100000,orderBy='label',offset=0,timeout=5.0,async=False,callback=None):
		data={}
		if tagFilter:
			data['tags']=tagFilter.getServerData()
		data['tagCloud']=False
		data['resourceList']=True
		data['limit']=limit
		data['offset']=offset
		data['orderBy']=orderBy
		return self.call('/find/',data,timeout,async,callback,ResourceListDelegate)
    
	def post(self,addr,data,to=5.0):
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
		
class ResourceDelegate(CallDelegate):
	
	def process(self,data):
		return Resource(serverData=data)
		
