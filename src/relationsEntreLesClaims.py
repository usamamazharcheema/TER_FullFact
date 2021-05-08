import sys
#import import_ipynb
import pandas as pd
import Claim as claim_obj
from nltk import word_tokenize , sent_tokenize 
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import TraitementConclusion
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import numpy as np
from sklearn.decomposition import PCA
import pickle
from yellowbrick.cluster.elbow import kelbow_visualizer
from sklearn.pipeline import Pipeline
from yellowbrick.cluster import KElbowVisualizer


ponctuation=[".",",","!",";","?", "'", "â€˜", "â€™"]
#Mots qui se repêtent beaucoup et qui figure en premier lieu dan le résultat de la classification
mots=["people", "new", "list", "years", "days", "show", "call", "claim"]
stop_words = stopwords.words('english')
#Les part_of_speech_tagging qu'on garde suite au prétraitement
pos_tag=["JJ", "JJR", "JJS", "RBR", "RBS", "NN", "NNS"]



#Fonction qui prend en paramètre un claim et qui se charge de traiter les contractions, mettre les caractères en minuscule et eliminer les stopwords, 
#la ponctuation et les mots qui se repêtent beaucoup. Elle se charge également de lemmatiser les termes et d'appliquer un analyseur morpho-syntaxique 
#sur eux pour déterminer leur genre. 
def pretraitement_Texte(post):
    tempo=[]
    resultat=[]
    pos= TraitementConclusion.nettoyage(post)
    pos=TraitementConclusion.lemmatization(pos)
    result= TraitementConclusion.eliminationStopWords(pos)
    result= [word for word in result if word not in ponctuation and word not in mots]  
    for r in result:
        if ("-" in r):
            k=r.replace("-","")
            result.remove(r)
            if k not in result:
                result.append(k)
    #Pour vérifier que le mot existe et n'est pas une chaine de caractères vide            
    clean_sample_list = [word for word in result if word]
    tempo=nltk.pos_tag(clean_sample_list)
    i=0
    while i < len(tempo):
        if (tempo[i][1] in pos_tag):
            if tempo[i][0] not in resultat:
                resultat.append(tempo[i][0])
        i+=1       
    phrase= " ".join(resultat)  
    return phrase


#Fonction qui parcourt les claims et qui extrait le titre et le texte de chaque claim et les concatène. Elle appelle ensuite la fonction de prétraitement 
#sur le résultat de la concaténation.  
def extractionTexte(claims, RP=False):
    posts=[]

    for v in claims:
        if RP:
            post= v[1] + " " + v[2]
        else:
            post= v.getTitle() + " " + v.getClaim()

        post= post.replace(".", "")
        ph=pretraitement_Texte(post)
        posts.append(ph)
     
    return posts
 

#Fonction qui se charge de la clusterisation des claims
def classification_kmeans(posts, true_k, rubrique):
 

    #Application du TF-IDF sur les {claims+titres} prétraités
    vectorizer = TfidfVectorizer()
    df = pd.DataFrame(
    data=vectorizer.fit_transform(posts).toarray(),
    columns=vectorizer.get_feature_names()
    )
    res= vectorizer.fit_transform(posts)
  

    model = KMeans(n_clusters=true_k)
    model.fit(res.reshape(-1, 1))
    
    kmeans_indices = model.fit_predict(res)


   #Affichage des top mots clés par cluster
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    topMC=[]
    for i in range(true_k):
        topMC.append([])
        for ind in order_centroids[i, :5]:
            topMC[i].append(terms[ind])
   

    return topMC, kmeans_indices
  

#Fonction qui prend comme paramètres les résultats de K-means et qui retourne les mots clés reliant les claims d'une certaine rubrique.
def recuperationElementsPredits(topMC, indices, true_k, claims):

    
    cc=[]
    c={}
    for k in range(true_k):
        c[k]=[]
        r=0
        while r < len(indices) :
            if indices[r]==k:
                c[indices[r]].append(claims[r])
            r+=1
        c[k].append(topMC[k])
   
    for valeur in c.values(): 
        i=0
        while i < len(valeur)-1:
            valeur[i].setRelated_posts("ClaimsSimilaires", [w.getUrl() for w in valeur if w!=valeur[i] and w != valeur[len(valeur) -1]])
            valeur[i].setKeyWordsRP("ClaimsSimilaires",valeur[len(valeur)-1])
            cc.append(valeur[i].getDict())
            i+=1
    
 
    return cc


#Fonction qui prend comme paramètres les résultats de K-means et qui retourne les mots clés reliant les claims de la rubrique Related Posts.
def recuperationRelatedPosts(relp, topMC, indices, true_k):
    i=0
    groupe=[]
        
    for i in range(true_k):
        r=0
        while r < len(indices) :
            if indices[r]==i:
                groupe.append(relp[r][0])
            r+=1
        groupe.append(topMC[i])
    return groupe
   

#Fonction qui fait appel à l'ensemble des fonctions précédentes  
def relationClaims(true_k, rubrique, claims, RP=False):
    if RP:
        retour= extractionTexte(claims, RP=True)
        topMC, indices=classification_kmeans(retour, true_k, rubrique)
        results=recuperationRelatedPosts(claims, topMC, indices, true_k)  

    else:    
        retour= extractionTexte(claims)
        topMC, indices=classification_kmeans(retour, true_k, rubrique)
        results=recuperationElementsPredits(topMC, indices, true_k, claims)
   
    return results
