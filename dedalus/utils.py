import json,os

def pathFromUrl(url):
	if url[-1]=='/': return url;
	else: return url+'/'



def getPrefs(name):
	confDir=os.path.expanduser("~/.dedalus")
	confFile=os.path.expanduser("~/.dedalus/"+name+".json")
	if not os.path.exists(confFile):
		prefs={}
	else:
		try:
			with open(confFile) as jsonFile:
				prefs=json.load(jsonFile)
		except:
			prefs={}
	return prefs
	
def savePrefs(name,data):
	confDir=os.path.expanduser("~/.dedalus")
	if not os.path.exists(confDir):
		os.makedirs(confDir)
	confFile=os.path.expanduser("~/.dedalus/"+name+".json")
	with open(confFile, 'w') as outfile:
		json.dump(data, outfile)
	

