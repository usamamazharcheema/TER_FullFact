import sys
if sys.version_info[0] >= 3:
    unicode = str
class Claim:

	def __init__(self):
		self.source=""
		self.claim=unicode("")
		self.body=unicode("")
		self.conclusion=unicode("")
		self.related_posts=[]
		self.title=unicode("")
		self.date=""
		self.url=""
		self.rubrique=""
		self.verdictTompo=""
		self.html=False
		self.idClaim=1
		self.keyWordsRP=[]



	def setSource(self, str_):
		self.source = str_
		return self

	def setClaim(self, str_):
		self.claim = unicode(str_)
		return self

	def setBody(self, str_):
		self.body = unicode(str_)
		return self

	def setConclusion(self, str_):
		self.conclusion = unicode(str_)
		return self

	def setRelated_posts(self, str_):
		self.related_posts.append(str_)
		return self

	def setTitle(self, str_):
		self.title = unicode(str_)
		return self

	def setVerdictTompo(self, str_):
		self.verdictTompo= unicode(str_)
		return self

	def setDate(self, str_):
		self.date = str_
		return self

	def setUrl(self, str_):
		self.url = unicode(str_)
		return self

	def setRubrique(self, str_):
		self.rubrique = unicode(str_)

	def setHtml(self, str_):
		self.html = str_

	def setIdClaim(self, n):
		self.idClaim = n
		return self

	def setKeyWordsRP(self, str_):
		self.keyWordsRP.append(str_)
		return self

	def getClaim(self):
		return self.claim

	def getTitle(self):
		return self.title

	def getUrl(self):
		return self.url


	def getIdClaim(self):
		return self.idClaim

	def getRubrique(self):
		return self.rubrique

	



	def getDict(self):
		dict_={}
		dict_['source']=self.source
		dict_['claim']=self.claim
		dict_['body']=self.body.replace("\n","")
		dict_['conclusion']=self.conclusion
		dict_['title']=self.title
		dict_['date']=self.date
		dict_['url']=self.url
		dict_['rubrique']=self.rubrique
		dict_['verdictTompo']=self.verdictTompo
		dict_['idClaim']=self.idClaim
		dict_['related_posts']=self.related_posts
		dict_['keyWordsRP']=self.keyWordsRP
		#dict_['id']=self.composedClaim
		if (self.html):
			dict_['html']=self.html
		return dict_