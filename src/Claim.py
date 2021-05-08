import sys

if sys.version_info[0] >= 3:
    unicode = str

class Claim:

	def __init__(self):
		self.source=""
		self.claim=unicode("")
		self.body=unicode("")
		self.conclusion=unicode("")
		self.related_posts={}
		self.title=unicode("")
		self.date=""
		self.url=""
		self.rubrique=""
		self.verdictTompo=""
		self.idClaim=1
		self.keyWordsRP={}
		self.liens_revue=""



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

	def setRelated_posts(self, cle, valeur):
		self.related_posts[cle]=valeur
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

	def setIdClaim(self, n):
		self.idClaim = n
		return self

	def setKeyWordsRP(self, cle, valeur):
		self.keyWordsRP[cle]=valeur
		return self

	def setLiensRevue(self, str_):
		self.liens_revue = unicode(str_)
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

	
	#creation d'un dictionnaire d'objets claim 
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
		dict_['valeur_de_véracité']=self.verdictTompo
		dict_['idClaim']=self.idClaim
		dict_['related_posts']=self.related_posts
		dict_['keywords']=self.keyWordsRP
		dict_['liens_revue']=self.liens_revue
		return dict_