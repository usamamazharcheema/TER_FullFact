import sys
import pandas as pd
#import urllib2
from urllib.request import urlopen
from bs4 import BeautifulSoup
import dateparser
import Claim as claim_obj
from selenium import webdriver
from nltk import word_tokenize
import nltk
#nltk.download('punkt')
from nltk.corpus import wordnet as wn
from py_thesaurus import Thesaurus
import TraitementConclusion




def briefAdditionalRows(soup, result,url, idClaim, relp, rubri, l, t, liensRevue):

	claim_ =  claim_obj.Claim()	
	claim = soup.find('div', {"class": "col-xs-12 col-sm-6 col-left"})
	if claim :
		claim_.setSource("fullfact")
		claim_.setUrl("http://fullfact.org"+url.replace("?utm_source=content_page&utm_medium=related_content",""))
		claim_.setClaim(claim.get_text().replace("\nClaim\n",""))
		claim_.setIdClaim(idClaim)
		claim_.setRubrique(rubri)
		claim_.setKeyWordsRP(l)
		claim_.setTitle(t)
		

		conclusion = soup.find('div', {"class": "col-xs-12 col-sm-6 col-right"})
		if conclusion :
			claim_.setConclusion(conclusion.get_text().replace("\nConclusion\n",""))
			c=conclusion.get_text().replace("\nConclusion\n","")
			claim_.setVerdictTompo(brouillon.fonctionPrincipale(c))

		claim_.setBody(result)
		claim_.setRelated_posts(relp) 
		claim_.setLiensRevue(liensRevue)
		return claim_
	else:
		return "empty"