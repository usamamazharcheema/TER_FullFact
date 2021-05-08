import sys
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import dateparser
import Claim as claim_obj
from nltk import word_tokenize
import nltk
import TraitementConclusion



#Fonction qui récupère les claims (ainsi que leurs métadonnées) additionnelles se trouvant sur la même page et ayant été traités par la même revue.
def briefAdditionalRows(soup, result, url, idClaim, listeURL, rubri, motsCles, t, liensRevue, d):
	
	claim = soup.find('div', {"class": "col-xs-12 col-sm-6 col-left"})
	if claim :
		claim_ =  claim_obj.Claim()	
		claim_.setSource("fullfact")
		claim_.setUrl(url)
		claim_.setClaim(claim.get_text().replace("\nClaim\n",""))
		claim_.setIdClaim(idClaim)
		claim_.setRubrique(rubri)
		claim_.setKeyWordsRP("RelatedPosts", motsCles)
		claim_.setTitle(t)
		claim_.setDate(d)


		conclusion = soup.find('div', {"class": "col-xs-12 col-sm-6 col-right"})
		if conclusion :
			claim_.setConclusion(conclusion.get_text().replace("\nConclusion\n",""))
			c=conclusion.get_text().replace("\nConclusion\n","")
			claim_.setVerdictTompo(TraitementConclusion.fonctionPrincipale(c))


		
		claim_.setBody(result)
		
		claim_.setRelated_posts("RelatedPosts", listeURL) 
		
		claim_.setLiensRevue(liensRevue)
		
		return claim_
	else:
		return "empty"