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


vP = ["true", "correct"]
vN = ["false", "incorrect"]

synoP=[]
synoN=[]

for p in vP:
	for syn in wn.synsets(p):
		for l in syn.lemmas():
			synoP.append(l.name())

for n in vN:
	for syn in wn.synsets(n):
		for l in syn.lemmas():
			synoN.append(l.name())



ponctuation=[".",",","!"]
conclusion="Incorrect, a number of European countries have higher income tax rates than Scotland."


def exactractionDirect(vP, vN, conclusion, ponctuation):
	verd=""
	flag=False
	tempo=word_tokenize(conclusion)
	 #print(tempo)
	i=0
	while i < len(tempo)-1:
	 	if tempo[i].lower() in synoP and tempo [i+1] in ponctuation:
	 		return "True"
	 		
	 	else:
	 		if tempo[i].lower() in synoN and tempo [i+1] in ponctuation:
	 			return "False"
	 		else:
	 			return "Other"
	 					
	 	i=+1






print(exactractionDirect(synoP, synoN, conclusion, ponctuation))
