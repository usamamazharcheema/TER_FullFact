class Criteria:
	
	def __init__(self):
		self.maxClaims = 500
		self.output = "output.csv"
		self.website="fullfact"
		
	def setMaxClaims(self, maxClaims):
		self.maxClaims = maxClaims
		return self

	def getMaxClaims(self):
		return self. maxClaims

	def setOutput(self, output):
		self.output = output
		return self

	def setWebsite(self, website):
		self.website = website
		return self

