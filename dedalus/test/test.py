import os
import subprocess
import dedalus.test.env as env
from dedalus import *

import time

def testCallback(err,res):
	
	if err:
		print('ERROR',err)
	else:
		print(res)



c=env.getClient()
	

	
c.clearDatabase()

#env.fillRandom(c,verbose=True)

env.transferUserDb(c,verbose=True)

for res in c.getResources():
	print(res)

cloud=c.getTagCloud()

for tag in cloud.getTags():
	print(tag.name,tag.weight,tag.normWeight())

#time.sleep(5)

