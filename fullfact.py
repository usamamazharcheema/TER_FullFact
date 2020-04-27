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
import brouillon
import getPosts
import additionalRows
import lienPosts
import string
#vP = ["true", "correct"]
#vN = ["false", "incorrect"]

synoP=["correct", "right", "true", "evidence","quite", "accurate"]
synoN=["incorrect", "false"]
'''
for p in vP:
	for syn in wn.synsets(p):
		for l in syn.lemmas():
			synoP.append(l.name())

for n in vN:
	for syn in wn.synsets(n):
		for l in syn.lemmas():
			synoN.append(l.name())
'''

ponctuation=[".",",","!"]

claims=[]
urlTraite=[]
urls_=[]
idClaim=1

fichier= open("conclusion.txt", "a")

rubriquesClaim=["economy", "health", "online", "europe"]
rubEconomy= []
rubHealth=[]
rubOnline=[]
rubEurope=[]


def triClaimsParRubrique(rubri, uri, claim, title):
	global rubEconomy, rubHealth, rubOnline, rubEurope
	cl=[]
	cl.append(rubri)
	cl.append(uri)
	c=(claim.replace("\n", "")).replace(".", "")
	cl.append(c)
	cl.append(title)
	#print(cl)
	
	if rubri == "economy":
	 	rubEconomy.append(cl)
	else:
		if rubri == "health":
			rubHealth.append(cl)
		else:
	 		if rubri == "online":
	 			rubOnline.append(cl)
	 		else:
	 			if rubri == "europe":
	 				rubEurope.append(cl)



def exactractionClaim(page,url):
	global urlTraite, urls_, claims, idClaim
	print("url  "+ url)
	soup = BeautifulSoup(page,"lxml")
	soup.prettify()
	claim_ =  claim_obj.Claim()

	
	
	claim = soup.find('div', {"class": "col-xs-12 col-sm-6 col-left"})
	if claim :
		claim_.setSource("fullfact")
		claim_.setUrl("http://fullfact.org"+url)
		claim_.setClaim(claim.get_text().replace("\nClaim\n",""))
		claim_.setIdClaim(idClaim)
			
		
		conclusion = soup.find('div', {"class": "col-xs-12 col-sm-6 col-right"})
		if conclusion :
			claim_.setConclusion(conclusion.get_text().replace("\nConclusion\n",""))
			c=conclusion.get_text().replace("\nConclusion\n","")
			#fichier.write("\n" + c)
			claim_.setVerdictTompo(brouillon.fonctionPrincipale(c))
	
		
		title = soup.find("div", {"class": "header col-xs-12 no-padding"})
		if title:
			t=title.find("h1").get_text()
			claim_.setTitle(t)


  	
		body = soup.find("div", {"class": "article-post-content"})
		if body :
			liensRevue=[]
			text=[]
			bod=body.find("div", {"class": "col-xs-12 no-padding"})
			for b in bod.findAll("p"):
				for link in b.findAll('a', href=True):
					liensRevue.append(link['href'])
				text.append(b.get_text())
			result= " ".join(text) 
			print(liensRevue)
			claim_.setLiensRevue(liensRevue)
			claim_.setBody(result)


		categories = soup.find('ol', {"class": "breadcrumb"}) 
		if categories:
			rub=[]
			for c in categories.findAll('a', href=True):
				rub.append(c['href'])
			rubrique=rub[-1].split('/') 
			rubri=rubrique[1]
			claim_.setRubrique(rubri)
			triClaimsParRubrique(rubri, "http://fullfact.org"+url, claim.get_text().replace("\nClaim\n",""), title.find("h1").get_text())


		relp = getPosts.getRelatedPosts(soup)
		claim_.setRelated_posts(relp) 
		l=lienPosts.fonctionPRelatedPosts(relp, 1)
		print("sujets en commun: " + str(l))
		claim_.setKeyWordsRP(l)

		
		autresClaims=soup.find_all('div', {"class": "briefAdditionalRows"})
		if autresClaims:
			for row in autresClaims:
				c=additionalRows.briefAdditionalRows(row, result, url, idClaim, relp, rubri, l, t, liensRevue)
				if c != "empty":
					claims.append(c.getDict())
		idClaim+=1


			
		if len(relp)!=0 :
			for r in relp:
				if not (r[1] in urlTraite):
					try:
						page = urlopen("http://fullfact.org"+r[1]).read()
						urlTraite.append(r[1])
						print("url de related posts\n")
						exactractionClaim(page, r[1])
					except:
						continue

		claims.append(claim_.getDict())


	else :
		ls = soup.findAll('a', href=True)
		if len(ls) != 0:
			for anchor in ls:
				if (not(anchor['href'] in urls_ ) and not(anchor['href'] in urlTraite) ):
					urls_.append(anchor['href'])
					print ("page sans claim ! "+str(anchor['href']))








def get_all_claims(criteria):
	
	global urls_, urlTraite, idClaim, rubEconomy, rubHealth, rubOnline, rubEurope



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
			if (not(anchor['href'] in urls_ ) ):
				urls_.append(anchor['href'])
				print ("adding "+str(anchor['href']))
			
	else:
	    print ("break!")
	    	

	index=0
	# visiting each article's dictionary and extract the content.
	for url in urls_:
		if (not(url in u) and not (url in urlTraite)):
			if(index < 60):
				print (str(index) + "/" + str(len(urls_))+ " extracting http://fullfact.org" +str(url))
				url_complete="http://fullfact.org"+url
	
				try :

					page = urlopen(url_complete).read()
					urlTraite.append(url)
					exactractionClaim(page,url)
					index+=1
				except :
					print("try \n")
					continue

		else: 
			continue

				
	print(rubHealth)
	#print(rubEconomy)
	#print(rubEurope)
	#print(rubOnline)

	pp=lienPosts.fonctionPRelatedPosts(rubHealth, 3)
	print(pp)

		



	pdf=pd.DataFrame(claims)

	'''print("\n")
	print(urls_)
	print("\n")	
	print(urlTraite)'''
	return pdf
    