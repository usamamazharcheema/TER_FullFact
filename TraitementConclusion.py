import sys
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import dateparser
import Claim as claim_obj
from nltk import word_tokenize , sent_tokenize 
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
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
synoP=["correct", "right", "true", "evidence" "accurate"]
synoN=["incorrect", "false", "fake", "wrong"]
synoMix=["uncertain", "quite", "necessarily"]

ponctuation=[".",",","!",";","?"]
conclusion="It’s not clear how long the virus can ‘survive’ on hands, but hand sanitiser with at least 60% alcohol is a good second choice to washing your hands with soap and water."
conclusion1="That is correct, that doesn’t mean that Dettol spray can kill the new coronavirus identified in Wuhan. Coronavirus is a category of viruses that includes the common cold, and it is likely this the label is referring to."
conclusion2="Not quite, the exact fall depends which currency you compare it to. It’s fallen by 12% against the Euro and 5% against the US Dollar since May 2016."
conclusion3="This is uncertain. When IMF said the pound was overvalued, they based their recommendations on the assumption that the UK would vote to remain in the EU. It's open to debate what value the pound should be at now that we've voted to leave."
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
    return "Other"




def exactractionDirect(words):
    words = [t for t in words if not t in ponctuation]
    tempo=nltk.pos_tag(words)
    tempoLematise=lemmatization(words)
    i=0
    if tempoLematise[len(tempo)-1][0]=="not" and (tempoLematise[len(tempoLematise)-2][1]=="MD" or tempoLematise[len(tempoLematise)-2][1]=="VBP"):
        return "False"

    while i < len(tempo):
        if (tempo[i][0] in synoP or tempo[i][0] in synoN) and i + 1 != len(tempo) and tempo[i+1][0] in mixture_words:
            return "Mixture"

        if tempo[i][0] in synoN:
            return "False"

        if tempo[i][0] in synoP:
            return "True"

        if tempo[i][0] in synoMix:
            return "Mixture"
    			
        i+=1
    return "Other"
 
		

def negationIndirecte(tempo):
    words=mark_negation(tempo)
    neg = [w.replace("_NEG","") for w in words if w.endswith("_NEG")]
    for n in neg:
        if n in synoP:
            return "False"
    
        if n in synoN:
            return "True"
    
        if n in synoMix:
            return "Mixture"
           
    return "Other"


def fonctionPrincipale(conclusion):
    words=[]
    words=nettoyage(conclusion)
  


    result=detectionNegationDirect(words)
    
    if result=="Other":
        #words=eliminationStopWords(words)
        result=negationIndirecte(words)
        if result=="Other":
            result=exactractionDirect(words)
    return result
         




#print(fonctionPrincipale(conclusion1))
#print(fonctionPrincipale(conclusion2))
#print(fonctionPrincipale(conclusion3))










