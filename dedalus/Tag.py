class Tag:
	
	ASSIGNED=1
	NOT_ASSIGNED=0
	INHERITED=2
	
	
	def __init__(self,name):
		self.name=name.strip()
		self.key=name
		

	def __hash__(self):
		return hash(self.name)
	
	def __eq__(self, other):
		return self.name == other.name
	
	def __ne__(self, other):
		return not(self == other)

