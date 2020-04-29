import sys
import pandas as pd
#import import_ipynb
from urllib.request import urlopen
from bs4 import BeautifulSoup
import dateparser
import Claim as claim_obj
from selenium import webdriver
from nltk import word_tokenize , sent_tokenize 
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from py_thesaurus import Thesaurus
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
import inflect
from nltk.corpus import stopwords
from nltk.sentiment.util import *
import unicodedata
import re
import contractions

'''
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

'''
synoP=["correct", "right", "true", "evidence", "quite", "accurate", "necessarily"]
synoN=["incorrect", "false", "fake", "wrong", "uncertain"]

ponctuation=[".",",","!",";","?"]
conclusion="It’s not clear how long the virus can ‘survive’ on hands, but hand sanitiser with at least 60% alcohol is a good second choice to washing your hands with soap and water."
conclusion1="That is correct, but that doesn’t mean that Dettol spray can kill the new coronavirus identified in Wuhan. Coronavirus is a category of viruses that includes the common cold, and it is likely this the label is referring to."
conclusion2="While it is true that China has over 100,000 towers, it is unclear if it was the first place to pass this number."
conclusion3="This claim hasn’t been substantiated and we’ve not seen wider evidence for this. In 2016, 85% of goods which left Belfast port went to the UK, measured by their weight. 56% of all Northern Irish goods sold beyond its borders went to Great Britain, based on the value of those goods."
mixture_words=["but", "however"]
negation=["no", "not","neither", "nor"]




def nettoyage(conclusion):
    phrase=sent_tokenize(conclusion)
    phrase[0] =contractions.fix(phrase[0])
    tokens=word_tokenize(phrase[0])

    tokens = [w.lower() for w in tokens]


    return tokens

def lemmatization(tempo):
    wordnet_lemmatizer = WordNetLemmatizer()
    tempo = [wordnet_lemmatizer.lemmatize(word, pos='v') for word in tempo]
    return tempo


stop_words = stopwords.words('english')
stop_words = [w for w in stop_words if not w in negation]

def eliminationStopWords(tempo):
    tempo = [w for w in tempo if not w in stop_words]
    return tempo


def detectionNegationDirect(tempo):
    t=0
    while t < len(tempo) :
        if tempo[t] in negation and t + 1 != len(tempo):
            if tempo[t+1] in synoP:
                return "False"
            else:
                if tempo[t+1] in synoN:
                    return "True"
        t +=1
    return "Untreated"




def exactractionDirect(words):
    words = [t for t in words if not t in ponctuation]
    tempo=nltk.pos_tag(words)

    i=0
    if tempo[len(tempo)-1][0]=="not" and (tempo[len(tempo)-2][1]=="MD" or tempo[len(tempo)-2][1]=="VBP"):
    	return "False"

    while i < len(tempo):
    	if (tempo[i][0] in synoP or tempo[i][0] in synoN) and i + 1 != len(tempo) and tempo[i+1][0] in mixture_words:
    		return "Mixture"	
    	else:
    		if tempo[i][0] in synoN:
    			return "False"
    		else:
    			if tempo[i][0] in synoP:
    				return "True"
    			
    	i+=1
    return "Untreated"
 
		

def negationIndirecte(tempo):
    words=mark_negation(tempo)
    neg = [w.replace("_NEG","") for w in words if w.endswith("_NEG")]
    for n in neg:
        if n in synoP:
            return "False"
        else:
            if n in synoN:
                return "True"
           
    return "untreated"


def fonctionPrincipale(conclusion):
    words=[]
    words=nettoyage(conclusion)
  
    words=lemmatization(words)

    result=detectionNegationDirect(words)
    
    if result=="Untreated":
        #words=eliminationStopWords(words)
        result=negationIndirecte(words)
        if result=="untreated":
            result=exactractionDirect(words)
    return result
         




print(fonctionPrincipale(conclusion1))









'''print(exactractionDirect(conclusion, ponctuation))
print("\n")
print(exactractionDirect(conclusion1, ponctuation))
print("\n")

ph1="It has not."
ph2="No it won't."

phrase =contractions.fix(conclusion3)
tokens = word_tokenize(phrase)
wordnet_lemmatizer = WordNetLemmatizer()
lstemmed = [wordnet_lemmatizer.lemmatize(word, pos='v') for word in tokens]
tempo=nltk.pos_tag(lstemmed)
print("Lemmatization : \n", tempo)

phrase =contractions.fix(ph1)
tokens = word_tokenize(phrase)
wordnet_lemmatizer = WordNetLemmatizer()
lstemmed = [wordnet_lemmatizer.lemmatize(word, pos='v') for word in tokens]
tempo1=nltk.pos_tag(lstemmed)
print("Lemmatization1 : \n", tempo1)


phrase =contractions.fix(ph2)
tokens = word_tokenize(phrase)
wordnet_lemmatizer = WordNetLemmatizer()
lstemmed = [wordnet_lemmatizer.lemmatize(word, pos='v') for word in tokens]
tempo2=nltk.pos_tag(lstemmed)
print("Lemmatization2 : \n", tempo2)


print(exactractionDirect(conclusion2, ponctuation))
print("\n")
'''

