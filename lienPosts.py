import sys
#import import_ipynb
import pandas as pd
import Claim as claim_obj
from nltk import word_tokenize , sent_tokenize 
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import brouillon
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import numpy as np
from sklearn.decomposition import PCA
import pickle
from yellowbrick.cluster.elbow import kelbow_visualizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from yellowbrick.cluster import KElbowVisualizer


negation=["no", "not","neither", "nor"]
pays=["eu", "uk", "us"]
ponctuation=[".",",","!",";","?", "'", "â€˜", "â€™"]
mots=["people", "new", "list", "years", "days", "show"]
categorie=["economy", "health", "europe", "online"]
stop_words = stopwords.words('english')


def traitementPosts(post):
    tempo=[]
    resultat=[]
    pos= brouillon.nettoyage(post)
    pos=brouillon.lemmatization(pos)
    result= brouillon.eliminationStopWords(pos)
    result= [word for word in result if word not in ponctuation and word not in mots]  
    for r in result:
        if ("-" in r):
            k=r.replace("-","")
            result.remove(r)
            if k not in result:
                result.append(k)
    clean_sample_list = [word for word in result if word]
    tempo=nltk.pos_tag(clean_sample_list)
    #print(tempo)
    i=0
    while i < len(tempo):
        if (tempo[i][1] == 'NN' or tempo[i][1] == 'NNS'):
            if tempo[i][0] not in resultat:
                resultat.append(tempo[i][0])
        i+=1       
    phrase= " ".join(resultat)  
    return phrase



def traitementRelatedPosts(relp, keyWords, posts):
    
    for v in relp:
        if(v[0] not in categorie and v[0] not in keyWords):
            keyWords.append(v[0])
        post= v[2] + " " + v[3]
        post= post.replace(".", "")
        #print(post)
        ph=traitementPosts(post)
        posts.append(ph)
     
    return posts
 
def traitementPostsRubrique(keyWords, posts, claims):
    
    for c in claims:
        if(c.getRubrique() not in categorie and v[0] not in keyWords):
            keyWords.append(c.getRubrique())
        post= c.getTitle() + " " + c.getClaim()
        post= post.replace(".", "")
        #print(post)
        ph=traitementPosts(post)
        posts.append(ph)
     
    return posts
 


def getLiensPosts(posts, true_k, rubrique):
    
    vectorizer = TfidfVectorizer()
    res= vectorizer.fit_transform(posts)

    df = pd.DataFrame(
    data=vectorizer.fit_transform(posts).toarray(),
    columns=vectorizer.get_feature_names()
    )
   
  

    model = KMeans(n_clusters=true_k)
    model.fit(res)
    
    kmeans_indices = model.fit_predict(res)
    #print(posts)
    #print(len(posts))
    #print(model.labels_)
    #print(kmeans_indices)
    
    #affichage des points avec PCA
    '''
    pca = PCA(n_components=2).fit(res.todense())
    data2D = pca.transform(res.todense())
    centers = np.array(pca.transform(model.cluster_centers_))
    plt.title('Visualisation du résultat de Kmeans et de la distribution des données ( '+rubrique+' )')
    plt.scatter(data2D[:,0], data2D[:,1], c=kmeans_indices , cmap='rainbow')


    plt.scatter(centers[:,0], centers[:,1], marker="x", color='black')
    plt.figure(figsize=(16,8))
  
    plt.show()

'''
   #affichage des top mots clés par cluster
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
  

    #print("Top terms per cluster ( " +rubrique+" )")
    topMC=[]
    for i in range(true_k):
        topMC.append([])
        for ind in order_centroids[i, :5]:
            #print(terms[ind])
            topMC[i].append(terms[ind])
        #print("-----end cluster-----")
    #print (topMC)

    return topMC, kmeans_indices
  

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
        print(valeur)
        i=0
        while i < len(valeur)-1:
            valeur[i].setRelated_posts( [w.getUrl() for w in valeur if w!=valeur[i] and w != valeur[len(valeur) -1]])
            valeur[i].setKeyWordsRP(valeur[len(valeur)-1])
            cc.append(valeur[i].getDict())
            i+=1
    
    print("Je suis dans lienPosts")
    print("\n")
    #print (cc)
    print("++++++++++++++++++++++++++++++++++++++++++++")
    return cc


def recuperationRelatedPosts(relp, topMC, indices, true_k):
    i=0
    groupe=[]
        
    for i in range(true_k):
        r=0
        while r < len(indices) :
            if indices[r]==i:
                groupe.append(relp[r][1])
            r+=1
        groupe.append(topMC[i])
    return groupe
   
   
def fonctionLiensRubrique(true_k, rubrique, claims):
    posts=[]
    keyWords=[]
    #true_k=3
    retour= traitementPostsRubrique(keyWords, posts,claims)
    topMC, indices=getLiensPosts(retour, true_k, rubrique)
    cc=recuperationElementsPredits(topMC, indices, true_k, claims)
    return cc

def fonctionLiensRelatedPosts(relp, true_k, rubrique):
    posts=[]
    keyWords=[]
    #true_k=3
    retour= traitementRelatedPosts(relp,keyWords, posts)
    topMC, indices=getLiensPosts(retour, true_k, rubrique)
    rlp=recuperationRelatedPosts(relp, topMC, indices, true_k)    
    return rlp



