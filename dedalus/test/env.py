from dedalus import *

import random

def getClient(verbose=False):
	try:
		c=Client('http://localhost:4540')
	except:
		if verbose: print('Launching the test server...')
		os.system('dedalus-server --port 4540 --database /tmp/dedalus-test.sql&')
		time.sleep(2)
		if verbose: print('...launched')
		c=Client('http://localhost:4540')
	return c

def rndString(n=8):
	s=''
	for i in range(n):
		r=int(random.random()*26)
		s=s+chr(r+97)
	return s
	
def rndInt(n):
	return int(random.random()*n)
	
def rndUrl():
	if rndInt(4)==0:
		s='http:/'
	else:
		s='file://'
	for i in range(rndInt(4+1)):
		s=s+'/'+rndString(2)
	return s

def fillRandom(client,resN=1000,avgTagN=5,tagN=100,verbose=False):
	
	tags=[]
	resources=[]
	for i in range(tagN):
		tags.append(rndString(rndInt(4)+4))
	
	tagsMin=avgTagN-int(avgTagN/2)
	tagsMax=avgTagN+int(avgTagN/2)
	for i in range(resN):
		res=Resource(rndUrl())
		for j in range(rndInt(tagsMin-tagsMax)+tagsMin):
			res.addTag(Tag(tags[rndInt(tagN)]))
		resources.append(res)
		if len(resources)>=100:
			if verbose: print('Saving resources ',i-99,'to',i+1,'of',resN,'... ',end='')
			client.saveResources(resources)
			if verbose: print('done.')
			resources=[]
		
	if len(resources)>0:
		if verbose: print('Saving resources ',i-len(resources)+1,'to',i+1,'of',resN,'... ',end='')
		client.saveResources(resources)
		if verbose: print('done.')
		
def transferUserDb(client,verbose=False):
	userClient=Client()
	resources=[]
	source=userClient.getResources()
	resN=len(source)
	for i in range(resN):
		res=userClient.getResource(source[i].url)
		res._saved=False
		resources.append(res)
		if len(resources)>=100:
			if verbose: print('Saving resources ',i-99,'to',i+1,'of',resN,'... ',end='')
			client.saveResources(resources)
			if verbose: print('done.')
			resources=[]
	if len(resources)>0:
		if verbose: print('Saving resources ',i-len(resources)+1,'to',i+1,'of',resN,'... ',end='')
		client.saveResources(resources)
		if verbose: print('done.')
		


