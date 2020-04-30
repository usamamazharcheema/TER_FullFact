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
import fullfact
import socket
import TraitementConclusion


"""def getRelatedPosts(soup, claim_):
    relPosts = soup.find('div', {"class": "related-posts"})
    related_posts = []
    if relPosts:       
        for link in relPosts.findAll('a', href=True):
            url=link['href'].replace("?utm_source=content_page&utm_medium=related_content","")
            related_posts.append(url)
    return related_posts"""




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
                    lien = s.find('ol', {"class": "breadcrumb"})  
                    u=[]   
                    for l in lien.findAll('a', href=True):
                        u.append(l['href'])
                    rubrique=u[-1].split('/')
                    #print(rubrique[-2])
                    rlp=[]
                    rlp.append(rubrique[-2]) 
                    rlp.append((url))                            
                    rlp.append(link['title'])         
                    c1= claim.get_text().replace("\nClaim\n","")
                    c=c1.replace("\n","")
                    rlp.append(c) 
                    related_posts.append(rlp)
            
    return related_posts







                   