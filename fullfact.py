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
import conc

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

def get_all_claims(criteria):
	

	#performing a search by each letter, and adding each article to a urls_ var.

	#alfab="bc"
	urls_=[]
	u=[]

	page = urlopen("http://fullfact.org").read()

	#soup = browser.execute_script("return document.body.innerHTML")
	soup = BeautifulSoup(page,"lxml")
	#print (soup)
	#links = soup.getElementByTagName("a")
	soup.prettify()
	links = soup.findAll('a', href=True)
	sn = soup.findAll('a', {"class": "container no-padding"})

	if len(sn) != 0:
		for anchor in sn:
			if (not(str(anchor['href']) in u ) ):
				u.append(anchor['href'])
	

	if len(links) != 0:
		for anchor in links:
			if (not(str(anchor['href']) in urls_ ) ):
				urls_.append(anchor['href'])
				print ("adding "+str(anchor['href']))
			
	else:
	    print ("break!")
	    	
	claims=[]
	index=0
	# visiting each article's dictionary and extract the content.
	for url in urls_:
		if (not(url in u)):
			if(index < 200):
				print("je suis la \n")
				print (str(index) + "/" + str(len(urls_))+ " extracting "+str(url))
				url_complete="http://fullfact.org"+url
				try :
					page = urlopen(url_complete).read()
				except :
					continue
				index+=1
				claim_ =  claim_obj.Claim()
	

		
				print("url récupérée "+ url_complete)
				soup = BeautifulSoup(page,"lxml")
				soup.prettify()

		

		#claim
				claim = soup.find('div', {"class": "col-xs-12 col-sm-6 col-left"})
				if claim :
					claim_.setSource("fullfact")
					claim_.setUrl(url_complete)
					claim_.setClaim(claim.get_text().replace("\nClaim\n",""))

					conclusion = soup.find('div', {"class": "col-xs-12 col-sm-6 col-right"})
					if conclusion :
						claim_.setConclusion(conclusion.get_text().replace("\nConclusion\n",""))
						c=conclusion.get_text().replace("\nConclusion\n","")
						claim_.setVerdictTompo(conc.exactractionDirect(synoP, synoN, c, ponctuation))
		    
		    
		#title
					#title=soup.find("div", {"class": "header col-xs-12 no-padding"})
					#t=title.find("h1")
					#if title :
					#	claim_.setTitle(t.string.strip())mon


		#date
					date=soup.find("p", {"class": "visible-xs visible-sm date updated"})
					if date :
						claim_.setDate(dateparser.parse(date.get_text().replace("Published:","")).strftime("%Y-%m-%d"))
						print("je suis dans date"+claim_.date)

		
			#body
					body = soup.find("div", {"class": "article-post-content"})
					if body :
						claim_.setBody(body.get_text())


		#related links
					divTag = soup.find("div", {"class": "row"})
					related_links=[]
					if divTag :
						for link in divTag.findAll('a', href=True):
							if link :
								related_links.append(link['href'])
						if related_links :
							claim_.setRefered_links(related_links)



					claims.append(claim_.getDict())
				else :
					ls = soup.findAll('a', href=True)
					if len(ls) != 0:
		
						for anchor in ls:
							if (not(str(anchor['href']) in urls_ ) ):
								urls_.append(anchor['href'])
								print ("adding "+str(anchor['href']))

    
    #creating a pandas dataframe
	pdf=pd.DataFrame(claims)
	return pdf