#Les imports necessaires au programme.
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
mots=["people", "new", "list", "years", "days"]
categorie=["economy", "health", "europe", "online"]
stop_words = stopwords.words('english')

rubHealth=[]
rubEconomy=[]
rubEurope=[]
rubOnline=[]
def loadData(nomRubrique, nomFichier):
 
    with open(nomFichier, 'rb') as fichier:
        mon_depickler = pickle.Unpickler(fichier)
        nomRubrique=mon_depickler.load()
    fichier.close()
    return nomRubrique


rubHealth=loadData(rubHealth,'health')
rubEconomy=loadData(rubEconomy,'economy')
rubEurope=loadData(rubEurope,'europe')
rubOnline=loadData(rubOnline,'online')



def traitementPosts(post):
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



def traitementRelatedPosts(relp,keyWords, posts):
    
    for v in relp:
        if(v[0] not in categorie and v[0] not in keyWords):
            keyWords.append(v[0])
        post= v[2] + " " + v[3]
        post= post.replace(".", "")
        #print(post)
        ph=traitementPosts(post)
        posts.append(ph)
     
    return posts


def getLiensPosts(posts, true_k, rubrique):
    
    vectorizer = TfidfVectorizer()
 

    df = pd.DataFrame(
    data=vectorizer.fit_transform(posts).toarray(),
    columns=vectorizer.get_feature_names()
    )
    res= vectorizer.fit_transform(posts)
  

    model = KMeans(n_clusters=true_k)
    model.fit(res)
    
    kmeans_indices = model.fit_predict(res)
    #print(posts)
    #print(len(posts))
    #print(model.labels_)
    #print(kmeans_indices)
    
    '''
    #affichage des points avec PCA
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
  

    print("Top terms per cluster ( " +rubrique+" )")
    topMC=[]
    for i in range(true_k):
        topMC.append([])
        for ind in order_centroids[i, :5]:
            print(terms[ind])
            topMC[i].append(terms[ind])
        print("-----end cluster-----")
    #print (topMC)

    return topMC, kmeans_indices
  

def recuperationElementsPredits(relp, topMC, indices, true_k):
    i=0
    groupe=[]
    k=0
    for r in relp:
        print(str(r[1])+"  ============> "+str(indices[k]))
        k+=1
        
    for i in range(true_k):
        groupe.append([])
        r=0
        while r < len(indices) :
            if indices[r]==i:
                groupe[i].append(relp[r][1])
            r+=1
        groupe[i].append(topMC[i])
            
    return groupe
    
def fonctionPRelatedPosts(relp, true_k, rubrique):
    posts=[]
    keyWords=[]
    #true_k=3
    retour= traitementRelatedPosts(relp,keyWords, posts)
    topMC, indices=getLiensPosts(retour, true_k, rubrique)
    rlp=recuperationElementsPredits(relp, topMC, indices, true_k)
  
    
    return rlp

