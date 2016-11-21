from .Request import Request
from .RequestPool import RequestPool
from .TagCloudRequest import TagCloudRequest
from .ResourceListRequest import ResourceListRequest
from .UrlListRequest import UrlListRequest
from .RemoveListRequest import RemoveListRequest
from .RenameRequest import RenameRequest

tagCloudRequestPool=RequestPool(TagCloudRequest)
def tagCloud(client,tagFilter=None,limit=40,useOr=False,timeout=5.0,callback=None):
	global tagCloudRequestPool
	req=tagCloudRequestPool.get()
	req.start(client,tagFilter,limit,useOr,timeout,callback)
	return req

resourceListRequestPool=RequestPool(ResourceListRequest)
def resourceList(client,tagFilter=None,limit=None,pageSize=100,timeout=5.0,donef=None,pagef=None):
	global resourceListRequestPool
	req=resourceListRequestPool.get()
	req.start(client,tagFilter,limit,timeout,pageSize,donef,pagef)
	return req


urlListRequestPool=RequestPool(UrlListRequest)
def urlList(client,urlList,pageSize=100,timeout=5.0,donef=None,pagef=None):
	global urlListRequestPool
	req=urlListRequestPool.get()
	req.start(client,urlList,timeout,pageSize,donef,pagef)
	return req

removeListRequestPool=RequestPool(RemoveListRequest)
def removeList(client,urlList,pageSize=100,timeout=5.0,donef=None,pagef=None):
	global removeListRequestPool
	req=removeListRequestPool.get()
	req.start(client,urlList,timeout,pageSize,donef,pagef)
	return req

renameRequestPool=RequestPool(RenameRequest)
def rename(client,url,newUrl,timeout=5.0,callback=None):
	global renameRequestPool
	req=renameRequestPool.get()
	req.start(client,url,newUrl,timeout,callback)
	return req

