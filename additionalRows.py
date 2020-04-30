import sys
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import dateparser
import Claim as claim_obj
from selenium import webdriver
from nltk import word_tokenize
import nltk
from nltk.corpus import wordnet as wn
from py_thesaurus import Thesaurus
import TraitementConclusion




def briefAdditionalRows(soup, result, url, idClaim, listeURL, rubri, motsCles, t, liensRevue):

	claim_ =  claim_obj.Claim()	
	claim = soup.find('div', {"class": "col-xs-12 col-sm-6 col-left"})
	if claim :
		claim_.setSource("fullfact")
		claim_.setUrl(url)
		claim_.setClaim(claim.get_text().replace("\nClaim\n",""))
		claim_.setIdClaim(idClaim)
		claim_.setRubrique(rubri)
		claim_.setKeyWordsRP(motsCles)
		#claim_.setTitle(t)


		conclusion = soup.find('div', {"class": "col-xs-12 col-sm-6 col-right"})
		if conclusion :
			claim_.setConclusion(conclusion.get_text().replace("\nConclusion\n",""))
			c=conclusion.get_text().replace("\nConclusion\n","")
			claim_.setVerdictTompo(TraitementConclusion.fonctionPrincipale(c))

		
		claim_.setBody(result)
		claim_.setRelated_posts(listeURL) 
		claim_.setLiensRevue(liensRevue)
		return claim_
	else:
		return "empty"