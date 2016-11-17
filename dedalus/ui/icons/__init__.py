from . import icons_rc
from PySide.QtGui import QIcon
from PySide.QtCore import QSize

pixmaps={}

def pixmap(name,width,height):
	global pixmaps
	key=name+'_'+str(width)+str(height)
	if key in pixmaps:
		return pixmaps[key]
	else:
		pixmap=QIcon(":/dedalus/"+name+".svg").pixmap(QSize(width,height))
		pixmaps[key]=pixmap
		return pixmap
	
	
