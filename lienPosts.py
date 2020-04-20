import sys
#import import_ipynb
import pandas as pd
#import urllib2
from urllib.request import urlopen
from bs4 import BeautifulSoup
import dateparser
import Claim as claim_obj
from selenium import webdriver
from nltk import word_tokenize , sent_tokenize 
import nltk
from nltk.corpus import wordnet as wn
from py_thesaurus import Thesaurus
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import fullfact
import socket
import brouillon
import pickle


negation=["no", "not","neither", "nor"]
pays=["eu", "uk", "us"]
ponctuation=[".",",","!",";","?", "'", "â€˜", "â€™"]
mots=["people", "new", "list", "years", "days"]
categorie=["economy", "health", "europe", "online"]
stop_words = stopwords.words('english')

'''
rubHealth=[]
with open('health', 'rb') as fichier:
    mon_depickler = pickle.Unpickler(fichier)
    rubHealth=mon_depickler.load()
fichier.close()
print(rubHealth)
print("\n")
print(len(rubHealth))
'''
def traitementPosts(post):
    tempo=""
    resultat=[]
    pos= brouillon.nettoyage(post)
    result= brouillon.eliminationStopWords(pos)
    result= [word for word in result if word not in ponctuation and word not in mots]  
    for r in result:
        if ("-" in r):
            k=r.replace("-","")
            result.remove(r)
            if k not in result:
                result.append(k)

    tempo=nltk.pos_tag(result)
    #print(tempo)
    i=0
    while i < len(tempo):
        if (tempo[i][1] == 'NN' or tempo[i][1] == 'NNS'):
            if tempo[i][0] not in resultat:
                resultat.append(tempo[i][0])
        i+=1       
    phrase= " ".join(resultat)  
    return phrase



def traitementRelatedPosts(relp,keyWords, posts):
    
    for v in relp:
        if(v[0] not in categorie and v[0] not in keyWords):
            keyWords.append(v[0])
        post= v[2] + " " + v[3]
        post= post.replace(".", "")
        print(post)
        ph=traitementPosts(post)
        posts.append(ph)
     
    return posts
 


def getLiensPosts(posts, true_k):

    vectorizer = TfidfVectorizer()
    res= vectorizer.fit_transform(posts)


    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(res)

    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    print(terms)        
    return (terms[order_centroids[0][0]])

    
    

    """for i in range(true_k):
        for ind in order_centroids[i, :5]:
            print(terms[ind])
            resultat.append(terms[ind])"""


def fonctionPRelatedPosts(relp):
    posts=[]
    keyWords=[]
    true_k=1
    retour= traitementRelatedPosts(relp,keyWords, posts)
    f=getLiensPosts(retour, true_k)
    if f not in keyWords:
        keyWords.append(f)
    
    return keyWords
