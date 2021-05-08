import sys
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import dateparser
import Claim as claim_obj
import fullfact
import socket


#Fonction qui récupère les URI des claims se trouvant dans la section "Related Posts" et qui les parcourt un à un pour en extraire le titre ainsi que le texte de la conclusion 
def getRelatedPosts(soup):
    relPosts = soup.find('div', {"class": "related-posts"})
    related_posts = []
    if relPosts:
        for link in relPosts.findAll('a', href=True):
            if link :                
                url= "http://fullfact.org" + link['href'].replace("?utm_source=content_page&utm_medium=related_content","")
                page = urlopen(url).read()
                s = BeautifulSoup(page,"lxml")
                s.prettify()
                claim = s.find('div', {"class": "col-xs-12 col-sm-6 col-left"})
                if claim :
                    rlp=[]
                    rlp.append((url))                            
                    rlp.append(link['title'])         
                    c1= claim.get_text().replace("\nClaim\n","")
                    c=c1.replace("\n","")
                    rlp.append(c) 
                    related_posts.append(rlp)
            
    return related_posts







                   