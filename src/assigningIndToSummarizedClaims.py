from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
porter = PorterStemmer()
import nltk, string

from nltk import word_tokenize
from nltk.corpus import stopwords
from unidecode import unidecode
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer




def assigningIndToSummarizedClaims(summarized_claim, individual_claim):
    similarity_list=[]

    if summarized_claim and individual_claim:

        summarized_claim_list = word_tokenize(summarized_claim)
        individual_claim_list = word_tokenize(individual_claim)
        sw = stopwords.words('english')
        summarized_claim_set = {porter.stem(w) for w in summarized_claim_list if not w in sw}
        individual_claim_set = {porter.stem(w) for w in individual_claim_list if not w in sw}
        intersection =  summarized_claim_set.intersection(individual_claim_set)
        # print(intersection)
        union =  summarized_claim_set.union(individual_claim_set)

        Jaccard_Similarity = float(len(intersection)) / len(union)
        similarity_list.append(Jaccard_Similarity)
        # print(similarity_list)
        return Jaccard_Similarity
    else:
        return "0"

# stemmer = nltk.stem.porter.PorterStemmer()
# remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
#
# def stem_tokens(tokens):
#     return [stemmer.stem(item) for item in tokens]
#
# '''remove punctuation, lowercase, stem'''
# def normalize(text):
#     return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))
#
# vectorizer = TfidfVectorizer(strip_accents='unicode',tokenizer=normalize, stop_words='english')
#
# def cosine_sim(text1, text2):
#     if text1 and text2:
#         tfidf = vectorizer.fit_transform([text1, text2])
#         return ((tfidf * tfidf.T).A)[0, 1]
#     else:
#         return "0"



lemmatizer = WordNetLemmatizer()
def pre_process(sentence):
    sentence = sentence.lower()
    stopset = stopwords.words('english') + list(string.punctuation) + [".",",","!",";","?", "'", "â€˜", "â€™",'"']
    sentence = " ".join([lemmatizer.lemmatize(i) for i in word_tokenize(sentence) if i not in stopset])
    sentence = unidecode(sentence)
    return sentence
def cosine_sim(text1, text2):
    text1=pre_process(text1)
    text2= pre_process(text2)
    if text1 and text2:
        tfidf =  TfidfVectorizer().fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0, 1]
    else:
        return "0"
