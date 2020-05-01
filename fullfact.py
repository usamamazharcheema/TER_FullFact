import sys
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import dateparser
import Claim as claim_obj
from nltk import word_tokenize
import nltk
import TraitementConclusion
import getPosts
import additionalRows
import relationsEntreLesClaims
import string


synoP=["correct", "right", "true", "evidence","quite", "accurate"]
synoN=["incorrect", "false"]

ponctuation=[".",",","!"]

claims=[]

urlTraite=[]
urls_=[]
idClaim=1
uriSansClaim=0

claimsParRubrique={}

rubriquesClaim=["economy", "health", "online", "europe"]






def triClaimsParRubrique(rubri, claim):
	global claimsParRubrique
	print(rubri)
	listeClaims=[]
	if (not(rubri in claimsParRubrique)):
		listeClaims.append(claim)
		claimsParRubrique[rubri]= listeClaims
	else:
		claimsParRubrique[rubri].append(claim)
	



#Fonction récursive qui extrait les entités qu'on stocke dans le csv.
def exactractionClaim(page,url):
	global urlTraite, urls_, claims, idClaim, uriSansClaim
	print("url  "+ url)
	soup = BeautifulSoup(page,"lxml")
	soup.prettify()
	claim_ =  claim_obj.Claim()

	
	claim = soup.find('div', {"class": "col-xs-12 col-sm-6 col-left"})
	#si la page contient une claim et une conclusion.
	if claim :
		claim_.setSource("fullfact")
		claim_.setUrl(url)
		claim_.setClaim(claim.get_text().replace("\nClaim\n",""))
		claim_.setIdClaim(idClaim)
			
		
		#texte de la conclusion.
		conclusion = soup.find('div', {"class": "col-xs-12 col-sm-6 col-right"})
		if conclusion :
			claim_.setConclusion(conclusion.get_text().replace("\nConclusion\n",""))
			c=conclusion.get_text().replace("\nConclusion\n","")
			claim_.setVerdictTompo(TraitementConclusion.fonctionPrincipale(c))
	
			
		title = soup.find("div", {"class": "header col-xs-12 no-padding"})
		if title:
			t=title.find("h1").get_text()
			claim_.setTitle(t)



		date = soup.find("p", {"class": "date"})
		if date:
			d=date.find("span").get_text()
			claim_.setDate(d)



  		#texte de la revue.
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
			claim_.setLiensRevue(liensRevue)
			claim_.setBody(result)
		

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

		#stockage des URL des claims de "related posts" et mots clés associés dans l'attribut relatesPosts du claim courant
		claim_.setRelated_posts("RelatedPosts", l) 
		claim_.setKeyWordsRP("RelatedPosts",motsCles)


		#Cas où il y a plusieurs claims/conclusions traitées par la même revue.
		autresClaims=soup.find_all('div', {"class": "briefAdditionalRows"})
		if autresClaims:
			for row in autresClaims:
				c=additionalRows.briefAdditionalRows(row, result, url, idClaim, l, rubri, motsCles, t, liensRevue, d)
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
						page = urlopen(r[1]).read()
						urlTraite.append(r[1])
						print("url de related posts")
						exactractionClaim(page, r[1])
					except:
						continue


	

	#Si la page qu'on scrappe ne contient pas de claim/conclusion, juste une revue.
	else :
		uriSansClaim+=1
		print ("page :  "+url+"   sans claim !")
		ls = soup.findAll('a', href=True)
		if len(ls) != 0:
			for anchor in ls:
				u="http://fullfact.org"+ anchor['href'].replace("?utm_source=content_page&utm_medium=related_content","")
				if (not(u in urls_ ) and not(u in urlTraite) ):
					urls_.append(u)
					





def get_all_claims(criteria):
	
	global urls_, urlTraite, idClaim, claims,claimsEconomy, claimsHealth, claimsOnline, claimsEurope
	rubriques=["/law/","/economy/", "/europe/", "/health", "/online", "/crime/", "/immigration/", "/education/"]

	#le nombre de claims qu'on veut récuperer à l'extraction.
	nbClaims=400


	#scrapping du site catégorie par catégorie et rajout des uri trouvées dans "url_" pour les parcourir après.
	#à noter que qu'on garde que les uri commmençant par le nom d'une catégorie car les les autres ne correspondent pas aux pages de claims.
	for rub in rubriques:
		p = urlopen("http://fullfact.org"+rub).read()
		soup = BeautifulSoup(p,"lxml")
		links = soup.findAll('a', href=True)
		if len(links) != 0:
			for anchor in links:
				if (not(anchor['href'] in urls_ ) and anchor['href'].startswith(rub)):
					url_complete="http://fullfact.org"+ anchor['href'].replace("?utm_source=content_page&utm_medium=related_content","")
					urls_.append(url_complete)
					print ("adding "+ anchor['href'])
			
		else:
			print ("break!")

	#parcourir des uri stockées et appel de la fonction "extractionClaim" pour l'extraction des entités des claims.
	for url in urls_:
		
		if (not (url in urlTraite)):
			if(len(urlTraite) < nbClaims):
				print (str(len(urlTraite)) + "/" + str(nbClaims)+ " extracting "+str(url))
			
	
				try :

					page = urlopen(url).read()				
					urlTraite.append(url)
					exactractionClaim(page,url)
					
				except :
					print("Impossible d'ouvrir cette page ! \n")
					continue

		else: 
			continue




	cRubriques=[]
	for cle, valeur in claimsParRubrique.items():
		cRubriques= cRubriques+ lienPosts.fonctionLiensRubrique(1, cle, valeur)




	print("---------------fullfact------------")

	print("URI sans claims :" +str(uriSansClaim) + "/"+str(nbClaims))
	pdf=pd.DataFrame(cRubriques+ claims)


	return pdf
    
