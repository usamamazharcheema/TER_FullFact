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
import getPosts
import additionalRows
import lienPosts
import string


synoP=["correct", "right", "true", "evidence","quite", "accurate"]
synoN=["incorrect", "false"]

ponctuation=[".",",","!"]

claims=[]
claimsEconomy=[]
claimsHealth=[]
claimsOnline=[]
claimsEurope=[]
urlTraite=[]
urls_=[]
idClaim=1



rubriquesClaim=["economy", "health", "online", "europe"]



def triClaimsParRubrique(rubri, claim):
	global claimsEconomy, claimsHealth, claimsOnline, claimsEurope
	print("*************** Fonction triClaimsParRubrique ******************************")
	print(rubri)
	if rubri == "economy":
		print("\n")
		print(claim.getDict())
		claimsEconomy.append(claim)
	else:
		if rubri == "health":
			claimsHealth.append(claim)
		else:
	 		if rubri == "online":
	 			claimsOnline.append(claim)
	 		else:
	 			if rubri == "europe":
	 				claimsEurope.append(claim)
	 			else:
	 				claims.append(claim.getDict())


#Fonction récursive qui extrait les entités qu'on stocke dans le csv.
def exactractionClaim(page,url):
	global urlTraite, urls_, claims, idClaim
	print("url  "+ url)
	soup = BeautifulSoup(page,"lxml")
	soup.prettify()
	claim_ =  claim_obj.Claim()

	
	claim = soup.find('div', {"class": "col-xs-12 col-sm-6 col-left"})
	#si la page contient une claim et une conclusion.
	if claim :
		claim_.setSource("fullfact")
		claim_.setUrl("http://fullfact.org"+url)
		claim_.setClaim(claim.get_text().replace("\nClaim\n",""))
		claim_.setIdClaim(idClaim)
			
		
		#texte de la conclusion.
		conclusion = soup.find('div', {"class": "col-xs-12 col-sm-6 col-right"})
		if conclusion :
			claim_.setConclusion(conclusion.get_text().replace("\nConclusion\n",""))
			c=conclusion.get_text().replace("\nConclusion\n","")
			claim_.setVerdictTompo(TraitementConclusion.fonctionPrincipale(c))
	
		#titre du claim
		#title = soup.find("div", {"class": "header col-xs-12 no-padding"})
		#if title:
		#	t=title.find("h1").get_text()
		#	claim_.setTitle(t)


  		#texte de la revue.
		body = soup.find("div", {"class": "article-post-content"})
		if body :
			claim_.setBody(body.get_text())

		#extraction du nom de la rubrique du claim.
		categories = soup.find('ol', {"class": "breadcrumb"}) 
		if categories:
		
			rub=[]
			for c in categories.findAll('a', href=True):
				rub.append(c.get_text())
			print(rub) 

			rubri=rub[1].lower()
			print(rubri)
			claim_.setRubrique(rubri)


		#extraction des claims contenus dans la rubrique "related posts" du claim courant.
		relp = getPosts.getRelatedPosts(soup)
		#appel du programme qui extrait les mots clés/thématique pour lesquels les claims ont été mis en ensemble dans "related posts".
		l=lienPosts.fonctionLiensRelatedPosts(relp, 1, "RelatedPosts")
		
		
		motsCles=l[-1]
		del l[-1]
		print("sujets en commun: " + str(motsCles))
		print("\n")
		print(l)
		#stockage des URL des claims de "related posts" et mots clés associés dans l'attribut relatesPosts du claim courant.
		for liste in l :
			claim_.setRelated_posts(liste) 
		claim_.setKeyWordsRP(motsCles)


		#Cas où il y a plusieurs claims/conclusions traitées par la même revue.
		autresClaims=soup.find_all('div', {"class": "briefAdditionalRows"})
		if autresClaims:
			for row in autresClaims:
				c=additionalRows.briefAdditionalRows(row, body, url, idClaim, relp, rubri, l, t)
				if c != "empty":
					claims.append(c.getDict())
		idClaim+=1

	
		#stockage du claim courant dans la rubrique associée (necéssaire dans l'étape de clustering pour déduire s'il y a une relation entre claims de même rubrique).
		triClaimsParRubrique(rubri, claim_)
		
		#appel récursif sur les claims de related posts.	
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


	

	#Si la page qu'on scrappe ne contient pas de claim/conclusion, juste une revue.
	else :
		print ("page :    http://fullfact.org"+url+"   sans claim !")
		ls = soup.findAll('a', href=True)
		if len(ls) != 0:
			for anchor in ls:
				if (not(anchor['href'] in urls_ ) and not(anchor['href'] in urlTraite) ):
					urls_.append(anchor['href'])
					





def get_all_claims(criteria):
	
	global urls_, urlTraite, idClaim, claims,claimsEconomy, claimsHealth, claimsOnline, claimsEurope
	rubriques=["/law/","/economy/", "/europe/", "/health", "/online", "/crime/", "/immigration/", "/education/"]

	

	index=0
	#scrapping du site catégorie par catégorie et rajout des uri trouvées dans "url_" pour les parcourir après.
	#à noter que qu'on garde que les uri commmençant par le nom d'une catégorie car les les autres ne correspondent pas aux pages de claims.
	for rub in rubriques:
		p = urlopen("http://fullfact.org"+rub).read()
		soup = BeautifulSoup(p,"lxml")
		links = soup.findAll('a', href=True)
		if len(links) != 0:
			for anchor in links:
				if (not(anchor['href'] in urls_ ) and anchor['href'].startswith(rub)):
					urls_.append(anchor['href'])
					print ("adding "+ anchor['href'])
			
		else:
			print ("break!")
	#parcourir des uri stockées et appel de la fonction "extractionClaim" pour l'extraction des entités des claims.
	for url in urls_:
		if (not (url in urlTraite)):
			if(index < 450):
				urlNettoye=url.replace("?utm_source=content_page&utm_medium=related_content","")
				print (str(index) + "/" + str(len(urls_))+ " extracting http://fullfact.org" +str(urlNettoye))
				url_complete="http://fullfact.org"+urlNettoye
	
				try :

					page = urlopen(url_complete).read()
				
					urlTraite.append(urlNettoye)
					exactractionClaim(page,urlNettoye)
					index+=1
				except :
					print("Impossible d'ouvrir cette page ! \n")
					continue

		else: 
			continue


	print(claimsEconomy)
	print(claimsHealth)
	print(claimsEurope)
	print(claimsOnline)
	cEconomy=lienPosts.fonctionLiensRubrique(3, "Economy", claimsEconomy)
	cHealth=lienPosts.fonctionLiensRubrique(3, "Health", claimsHealth)
	cEurope=lienPosts.fonctionLiensRubrique( 3, "Europe", claimsEurope)
	cOnline=lienPosts.fonctionLiensRubrique(3, "Online", claimsOnline)


	print("---------------fullfact------------")
	print(cHealth)
	pdf=pd.DataFrame(cHealth + cOnline + cEurope + cEconomy + claims)


	return pdf
    
