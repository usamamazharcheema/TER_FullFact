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


vocabulary={"true": ["correct", "right", "true", "evidence", "accurate","exact"],
            "false": ["incorrect", "false", "fake", "wrong", "inaccurate", "untrue"],
            "mixture": ["uncertain", "ambiguous", "unclear", "unsure", "undetermined"],
            "opposition_words": ["but", "however"],
            "negation": ["no", "not","neither", "nor"],
            "mix_with_neg": ["quite", "necessarily", "sure","clear"]}


stop_words = stopwords.words('english')
stop_words = [w for w in stop_words if not w in vocabulary["negation"]]

ponctuation=[".",",","!",";","?", "'", "\""]

tag_verbs=["MD", "VB", "VBP"]

#Fonction qui traite les contractions dans les phrases puis les découpe et met leurs termes en minuscule 
def nettoyage(conclusion):
    phrase=sent_tokenize(conclusion)
    phrase[0] =contractions.fix(phrase[0])
    tokens=word_tokenize(phrase[0])
    tokens = [w.lower() for w in tokens]

    return tokens


#Fonction qui réduit les mots à leurs racines (mett les verbes à l'infinitif, supprime le "s" du pluriel, etc)
def lemmatization(tempo):
    wordnet_lemmatizer = WordNetLemmatizer()
    tempo = [wordnet_lemmatizer.lemmatize(word, pos='v') for word in tempo]
    return tempo



def eliminationStopWords(tempo):
    tempo = [w for w in tempo if not w in stop_words]
    return tempo


#Fonction qui détecte les cas tels que (it's correct...however)
def detectionOpposition(indice, tempo, n=False):
    
    newTempo=tempo[indice+1:]
    if n:
        sentence="".join([" "+i for i in newTempo])
    else:
        sentence="".join([" "+i[0] for i in newTempo])
    
    for m in vocabulary["opposition_words"]:
        if m in sentence:
            return True
    return False

def exactractionDirect(words):
    words = [t for t in words if not t in ponctuation]
  
    tempo=nltk.pos_tag(words)
    tempoLematise=lemmatization(words)
    tempoL=nltk.pos_tag(tempoLematise)
    i=0
    if tempoL[-1][0]=="not" and (tempoL[-2][1] in tag_verbs):
        return "False"

    while i < len(tempo):
       
        if (tempo[i][0] in vocabulary["true"] or tempo[i][0] in vocabulary["false"]) and i + 1 != len(tempo) and detectionOpposition(i, tempo):
            return "Mixture"
        
        if tempo[i][0] in vocabulary["false"]:
            return "False"

        if tempo[i][0] in vocabulary["true"]:
            return "True"

        if tempo[i][0] in vocabulary["mixture"]:
            return "Mixture"
    			
        i+=1
    return "Other"
 
		

def negationIndirecte(tempo):
    words=mark_negation(tempo)
    neg = [w.replace("_NEG","") for w in words if w.endswith("_NEG")]
    i=0
    for n in neg:
        if (n in vocabulary["true"] or n in vocabulary["false"]) and i + 1 != len(neg) and detectionOpposition(i, neg, n=True):
            return "Mixture"

        if n in vocabulary["mix_with_neg"]:
            return "Mixture"

        if n in vocabulary["true"]:
            return "False"
    
        if n in vocabulary["false"]:
            return "True"
    
        
        i+=1
           
    return "Other"


def fonctionPrincipale(conclusion):
    words=[]
    words=nettoyage(conclusion)

   
    result=negationIndirecte(words)
    if result=="Other":
        result=exactractionDirect(words)
    return result
        
