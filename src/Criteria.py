class Criteria:
	
	def __init__(self):
		self.maxClaims = 1500
		self.output = "output.csv"
		self.website="fullfact"
		self.websitekg="kgFullfact"
		self.websiteAssign="fullFactAssigning"

		
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
	def setWebsiteKg(self, website):
		self.websitekg = website
		return self
	def setWebsiteAssign(self, website):
		self.websiteAssign = website
		return self

