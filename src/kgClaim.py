import sys

if sys.version_info[0] >= 3:
    unicode = str

class kgClaim:

	def __init__(self):
		self.claimReview_author=unicode("")
		self.claimReview_author_name = unicode("")
		self.claimReview_author_url = unicode("")
		self.claim = unicode("")
		self.claimReview_datePublished=unicode("")
		self.claimReview_source=unicode("")
		self.claimReview_url=unicode("")
		self.creativeWork_author_name = unicode("")
		self.creativeWork_author_sameAs=unicode("")
		self.creativeWork_datePublished=unicode("")
		self.extra_body=unicode("")
		self.extra_entities_author=unicode("")
		self.extra_entities_body=unicode("")
		self.extra_entities_claimReview_claimReviewed=unicode("")
		self.extra_entities_keywords=unicode("")
		self.extra_refered_links=unicode("")
		self.extra_tags=unicode("")
		self.title = unicode("")
		self.rating_alternateName = unicode("")
		self.rating_bestRating=unicode("")
		self.rating_ratingValue=unicode("")
		self.rating_worstRating=unicode("")

		# self.idClaim=1
	def setClaimReviewAuthor(self, str_):
		self.claimReview_author = unicode(str_)
		return self
	def setClaimReviewAuthorName(self, str_):
		self.claimReview_author_name = unicode(str_)
		return self
	def setClaimReviewAuthorUrl(self, str_):
		self.claimReview_author_url = unicode(str_)
		return self

	def setClaim(self, str_):
		self.claim = unicode(str_)
		return self
	def setClaimReviewDatePublished(self, str_):
		self.claimReview_datePublished = unicode(str_)
		return self
	def setClaimReviewSource(self, str_):
		self.claimReview_source = unicode(str_)
		return self
	def setClaimReviewUrl(self,str_):
		self.claimReview_url=unicode(str_)
		return self
	def setCreativeWorkName(self, str_):
		self.creativeWork_author_name = unicode(str_)
		return self

	def setCreativeWorkAuthorSameAs(self,str_):
		self.creativeWork_author_sameAs=unicode(str_)
		return self
	def setCreativeWorkDatePublished(self,str_):
		self.creativeWork_datePublished=unicode(str_)
		return self
	def setExtraBody(self,str_):
		self.extra_body=unicode(str_)
		return self
	def setExtraEntitiesAuthor(self,str_):
		self.extra_entities_author=unicode(str_)
		return self
	def setExtraEntitiesBody(self,str_):
		self.extra_entities_body=unicode(str_)
		return self
	def setExtraEntitiesClaimReviewClaimReviewed(self,str_):
		self.extra_entities_claimReview_claimReviewed=unicode(str_)
		return self
	def setExtraEntitiesKeywords(self,str_):
		self.extra_entities_keywords=unicode(str_)
		return self
	def setExtraReferedLinks(self,str_):
		self.extra_refered_links=unicode(str_)
		return self
	def setExtraTags(self,str_):
		self.extra_tags=unicode(str_)
		return self
	def setTitle(self, str_):
		self.title = unicode(str_)
		return self
	def setRating_alternateName(self, str_):
		self.rating_alternateName = unicode(str_)
		return self
	def setRatingBestRating(self, str_):
		self.rating_bestRating = unicode(str_)
		return self
	def setRatingRatingValue(self, str_):
		self.rating_ratingValue = unicode(str_)
		return self
	def setRatingWorstRating(self, str_):
		self.rating_worstRating = unicode(str_)
		return self


	# def setIdClaim(self, n):
	# 	self.idClaim = n
	# 	return self

	def getClaim(self):
		return self.claim

	def getTitle(self):
		return self.title

	def getclaimReviewAuthorUrl(self):
		return self.claimReview_author_url

	# def getIdClaim(self):
	# 	return self.idClaim

	#
	#creation d'un dictionnaire d'objets claim
	def getDict(self):
		dict_={}
		dict_['claimReview_author'] = self.claimReview_author
		dict_['claimReview_author_name'] = self.claimReview_author_name
		dict_['claimReview_author_url'] = self.claimReview_author_url
		dict_['claimReview_claimReviewed']=self.claim
		dict_['claimReview_datePublished']=self.claimReview_datePublished
		dict_['claimReview_source']= self.claimReview_source
		dict_['claimReview_url']=self.claimReview_url
		dict_['creativeWork_author_name'] = self.creativeWork_author_name
		dict_['creativeWork_author_sameAs'] = self.creativeWork_author_sameAs
		dict_['creativeWork_datePublished'] = self.creativeWork_datePublished
		dict_['extra_body']=self.extra_body
		dict_['extra_entities_author']=self.extra_entities_author
		dict_['extra_entities_body']=self.extra_entities_body
		dict_['extra_entities_claimReview_claimReviewed'] = self.extra_entities_claimReview_claimReviewed
		dict_['extra_entities_keywords'] = self.extra_entities_keywords
		dict_['extra_refered_links']=self.extra_refered_links
		dict_['extra_tags']=self.extra_tags
		dict_['extra_title'] = self.title
		dict_['rating_alternateName'] = self.rating_alternateName
		dict_['rating_bestRating']= self.rating_bestRating
		dict_['rating_ratingValue']=self.rating_ratingValue
		dict_['rating_worstRating']=self.rating_worstRating
		# dict_['idClaim'] = self.idClaim

		return dict_