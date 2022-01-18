import sys
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import dateparser
import Claim as claim_obj
import assigningIndToSummarizedClaims
from nltk import word_tokenize
import nltk
import TraitementConclusion



#Fonction qui récupère les claims (ainsi que leurs métadonnées) additionnelles se trouvant sur la même page et ayant été traités par la même revue.
def briefAdditionalRows(soup, result, url, t, liensRevue, d, individual_claim, individual_claim_source):

	claim = soup.find('div', {"class": "card-body card-claim-body"})
	if claim :
		claim_ =  claim_obj.Claim()
		claim_.setSource("fullfact")
		claim_.setUrl(url)
		summarized_claim=claim.get_text().replace("\nWhat was claimed\n","")
		claim_.setClaim(summarized_claim)
	#	claim_.setIdClaim(idClaim)
	#	claim_.setRubrique(rubri)
	#	claim_.setKeyWordsRP("RelatedPosts", motsCles)
		claim_.setTitle(t)
		claim_.setDate(d)
		claim_.setIndClaim(individual_claim)
		claim_.setIndClaimSource(individual_claim_source)





		conclusion = soup.find('div', {"class": "card-body accent card-conclusion-body"})
		if conclusion :
			claim_.setConclusion(conclusion.get_text().replace("\nOur verdict\n",""))
			c=conclusion.get_text().replace("\nOur verdict\n","")
			claim_.setVerdictTompo(c)



		claim_.setBody(result)

	#	claim_.setRelated_posts("RelatedPosts", listeURL)

		claim_.setLiensRevue(liensRevue)
		Jcard_similarity = assigningIndToSummarizedClaims.assigningIndToSummarizedClaims(summarized_claim,
																						 individual_claim)
		claim_.setSimilarity(Jcard_similarity)

		return claim_
	else:
		return "empty"