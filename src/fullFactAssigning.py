import sys
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import dateparser
import Claim as claim_obj
from nltk import word_tokenize
import nltk
import TraitementConclusion
import getPosts
import additionalRowsAssigning
import assigningIndToSummarizedClaims
import IndividualClaimExtraction as ind_claim_extraction
import relationsEntreLesClaims
import string
import Criteria

claims = []

urlTraite = []
urls_ = []
idClaim = 1
uriSansClaim = 0
count_url = 0
article_more_than_one_Sclaim = 0
article_indClaim_gt_Sclaim = 0
summ_claim_per_article = {}
ind_claim_per_article = {}
Ind_id=0

claimsParRubrique = {}

nbClaims = 0


# def triClaimsParRubrique(rubri, claim):
# 	global claimsParRubrique
# 	#print(rubri)
# 	listeClaims=[]
# 	if (not(rubri in claimsParRubrique)):
# 		listeClaims.append(claim)
# 		claimsParRubrique[rubri]= listeClaims
# 	else:
# 		claimsParRubrique[rubri].append(claim)


# Fonction récursive qui extrait les entités qu'on stocke dans le csv.
def exactractionClaim(page, url, maxClaims):
    global urlTraite, urls_, claims, idClaim, uriSansClaim, nbClaims, count_url, article_more_than_one_Sclaim, article_indClaim_gt_Sclaim, dic_data, Ind_id

    if nbClaims < maxClaims:

        print(str(nbClaims) + "/" + str(maxClaims) + " extracting " + str(url))
        soup = BeautifulSoup(page, 'html.parser')
        # soup.prettify()
        claim_ = claim_obj.Claim()

        claim = soup.find('div', {"class": "card-body card-claim-body"})

        # si la page contient une claim et une conclusion.
        if claim:
            ind_claim_list = ind_claim_extraction.IndividualClaimExtraction
            ind_claim_list = ind_claim_list.getIndClaims(soup)

            #	nbClaims+=1
            claim_.setSource("fullfact")
            claim_.setUrl(url)
            summarized_claim = claim.get_text().replace("\nWhat was claimed\n", "")
            claim_.setClaim(summarized_claim)
            claim_.setIdClaim(idClaim)

            # texte de la conclusion.
            # conclusion = soup.find('div', {"class": "card-body accent card-conclusion-body"})
            # if conclusion:
            #     claim_.setConclusion(conclusion.get_text().replace("\nOur verdict\n", ""))
            #     c = conclusion.get_text().replace("\nOur verdict\n", "")
                #				fonct=TraitementConclusion.fonctionPrincipale(c)
                # TraitementConclusion.fonctionPrincipale(c)
                # claim_.setVerdictTompo(c)

            # block_quote = soup.find_all('blockquote')
            # claim_ = claim_obj.Claim()
            # if block_quote:
            # 	for claim in block_quote:
            #
            # 		# print(claim)
            # 		concat = ""
            # 		for link in claim.select('p'):
            # 			concat_text = link.get_text()
            # 			concat = concat + '\n' + concat_text
            #
            # 			if link.select('a', href=True):
            # 				individual_claim = "\n".join(concat.split('\n')[0:-1])
            #
            # 				if individual_claim:
            # 					print(individual_claim)
            #
            # 					claim_.setIndClaim(individual_claim)
            #
            # 				a_link = [a['href'] for a in link.select('a', href=True)]
            # 				link_content = concat.split('\n')[-1]
            # 				individual_claim_source = link_content + '\n' + a_link[0]
            # 				if individual_claim_source:
            # 					claim_.setIndClaimSource(individual_claim_source)
            # 				concat = ""
            #
            # 		footer = claim.find('footer')
            # 		if footer:
            # 			link = footer.find('a', href=True)
            # 			if link:
            # 				if concat:
            # 					individual_claim = concat
            # 					print(individual_claim)
            # 					claim_.setIndClaim(individual_claim)
            # 					individual_claim_source = footer.get_text() + "\n" + link['href']
            #
            # 					claim_.setIndClaimSource(individual_claim_source)

            # header
            # title = soup.find("h1", {"class": "mb-3 highlight-js"})
            # t = ""
            # if title:
            #     t = title.get_text()
            #     # print(t)
            #     claim_.setTitle(t)

            # date = soup.find("div", {"class": "published-at mb-2"})
            # d = ""
            # if date:
            #     d = date.get_text()
            #
            #     claim_.setDate(d)

            # texte de la revue.
            # body = soup.find("article")
            # if body:
            #
            #     liensRevue = []
            #     text = []
            #
            #     for b in body.find_all(lambda tag: tag.name == 'p' and not tag.attrs):
            #         for link in b.find_all('a', href=True):
            #             liensRevue.append(link['href'])
            #         text.append(b.get_text())
            #     result = " ".join(text)
            #     claim_.setLiensRevue(liensRevue)
            #     claim_.setBody(result)

            # extraction du nom de la rubrique du claim.
            # categories = soup.find('nav', {"class": "breadcrumbs"})
            # if categories:
            #     rub = []
            #     for c in categories.findAll('a', href=True):
            #         rub.append(c.get_text())
            #
            #     rubri = rub[0].lower()
            #     claim_.setRubrique(rubri)

            # extraction des claims contenus dans la rubrique "related posts" du claim courant.
            # relp = getPosts.getRelatedPosts(soup)
            # #appel du programme qui extrait les mots clés/thématique pour lesquels les claims ont été mis en ensemble dans "related posts".
            # l=relationsEntreLesClaims.relationClaims(1, "RelatedPosts", relp, RP=True)
            # motsCles=l[-1]
            # #rub[-1]
            # if not (rub[0].lower() == "online"):
            # 	motsCles.append(rub[0])
            # print("\n commun subjects -section related posts-: " + str(motsCles))
            # del l[-1]

            # stockage des URL des claims de "related posts" et mots clés associés dans l'attribut relatesPosts du claim courant
            # claim_.setRelated_posts("RelatedPosts", l)
            # claim_.setKeyWordsRP("RelatedPosts",motsCles)

            # Cas où il y a plusieurs claims/conclusions traitées par la même revue.
            autresClaims = soup.find_all('div',
                                         {"class": "card card-block card-claim-conclusion claimConclusion-js mb-2"})
            if autresClaims:

                count_url += 1
                # print(count_url)
                #	print(len(autresClaims))
                nbClaims += len(autresClaims)
                # summ_claim_per_article[url] = len(autresClaims)
                # individual_claims = len(ind_claim_list) / 2
                # if len(autresClaims) > 1:
                #     article_more_than_one_Sclaim += 1
                #
                # if ind_claim_list != "empty":
                #     ind_claim_per_article[url] = individual_claims
                #     if len(autresClaims) > 1 and individual_claims > len(autresClaims):
                #         article_indClaim_gt_Sclaim += 1
                # else:
                #     ind_claim_per_article[url] = 0

                if nbClaims > maxClaims:
                    return "break"

                if ind_claim_list != "empty":

                    if (len(ind_claim_list) / 2 == 1) or (len(autresClaims) == 1):
                        print("lenrth is equal to 1")

                        i = 0
                        while i < len(ind_claim_list):
                            # Ind_id +=1


                            for row in autresClaims:
                                # print(Ind_id)

                                dic_data = additionalRowsAssigning.briefAdditionalRowsAssigning(row, url,
                                                                              ind_claim_list[i])
                                if dic_data != "empty":
                                    print(dic_data.getAssignDic())
                                    claims.append(dic_data.getAssignDic())
                            i = i + 2
                    elif (len(ind_claim_list) / 2 > 1) and (len(autresClaims) > 1):

                        for row in autresClaims:
                            simi_list1 = []
                            data_simi1 = []
                            j = 0
                            while j < len(ind_claim_list):

                                dic_data = additionalRowsAssigning.briefAdditionalRowsAssigning(row, url,
                                                                              ind_claim_list[j])
                                if dic_data != "empty":
                                    similarities = dic_data.getAssignDic()['similarity']
                                    simi_list1.append(similarities)
                                    data_simi1.append(dic_data.getAssignDic())
                                j = j + 2
                            # check_duplicates=[]
                            for ind_simi in data_simi1:
                                if (ind_simi['similarity'] == max(simi_list1)) or (ind_simi['similarity'] >=0.5):
                                    claims.append(ind_simi)
                                    print(ind_simi)

                            # claims.append(check_duplicates[0])
                            # print(check_duplicates[0])



                        # Another set of loop to complete Individual claims
                        if len(ind_claim_list) / 2 > len(autresClaims):
                            print("length of individual is greater" + str(len(ind_claim_list) / 2) + " " + str(
                                len(autresClaims)))
                            k = 0
                            while k < len(ind_claim_list):


                                if not any(ind_claim_list[k] == claims_value['ind_claim'] for claims_value in claims):
                                    simi_list2 = []
                                    data_simi2 = []
                                    for row in autresClaims:
                                        dic_data2 = additionalRowsAssigning.briefAdditionalRowsAssigning(row, url,
                                                                                       ind_claim_list[k])
                                        if dic_data2 != "empty":
                                            similarities = dic_data2.getAssignDic()['similarity']
                                            simi_list2.append(similarities)
                                            data_simi2.append(dic_data2.getAssignDic())

                                    for ind_simi in data_simi2:
                                        if (ind_simi['similarity'] == max(simi_list2)) or (ind_simi['similarity'] >=0.5):
                                            claims.append(ind_simi)
                                            print(ind_simi)
                                k = k + 2










                # If Individual claim is empty
                else:
                    # Ind_id="empty"
                    for row in autresClaims:
                        c_dic = additionalRowsAssigning.briefAdditionalRowsAssigning(row, url,
                                                                   "empty")
                        print("without Ind_claim")
                        if c_dic != "empty":
                            print(c_dic.getAssignDic())
                            claims.append(c_dic.getAssignDic())











        # idClaim+=1
        #
        #
        # #stockage du claim courant dans la rubrique associée (necéssaire dans l'étape de clustering pour déduire s'il y a une relation entre claims de même rubrique).
        # triClaimsParRubrique(rubri, claim_)

        # appel récursif sur les claims de related posts.
        # if len(relp)!=0 :
        #
        # 	for r in relp:
        #
        # 		if not (r[0] in urlTraite):
        # 			try:
        # 				page = urlopen(r[0]).read()
        # 				urlTraite.append(r[0])
        # 				exactractionClaim(page, r[0], maxClaims)
        # 			except:
        # 				continue

        # Si la page qu'on scrappe ne contient pas de claim/conclusion, juste une revue.
        else:
            date = soup.find("div", {"class": "published-at mb-2"})
            if date:
                uriSansClaim += 1
            print("page :  " + url + "   without a claim !")
            ls = soup.findAll('a', href=True)
            if len(ls) != 0:
                for anchor in ls:
                    if not anchor['href'].startswith('https'):
                        u = "https://fullfact.org" + anchor['href'].replace(
                            "?utm_source=content_page&utm_medium=related_content", "")
                        if ((u not in urls_) and (u not in urlTraite)):
                            urls_.append(u)















    else:
        return "break"


def get_all_claimsAssign(criteria):
    global urls_, urlTraite, idClaim, claims, claimsEconomy, claimsHealth, claimsOnline, claimsEurope
    rubriques = ["/latest/", "/law/", "/economy/", "/economy/brexit/", "/economy/jobs-and-work/", "/europe/",
                 "/europe/brexit-options/", "/europe/trade/", "/health", "/health/coronavirus/", "/health/vaccines/",
                 "/online", "/crime/", "/immigration/", "/education/"]
    # subcatagories=[]

    # le nombre de claims qu'on veut récuperer à l'extraction.
    maxClaims = criteria.maxClaims

    # scrapping du site catégorie par catégorie et rajout des uri trouvées dans "url_" pour les parcourir après.
    # à noter que qu'on garde que les uri commmençant par le nom d'une catégorie car les les autres ne correspondent pas aux pages de claims.
    for rub in rubriques:
        p = urlopen("https://fullfact.org" + rub).read()
        soup = BeautifulSoup(p, "html.parser")
        links = soup.findAll('a', href=True)
        if len(links) != 0:
            for anchor in links:
                for start_match in rubriques:
                    url_complete = "https://fullfact.org" + anchor['href'].replace(
                        "?utm_source=content_page&utm_medium=related_content", "")
                    # print("testing" + anchor['href'])

                    if ((url_complete not in urls_) and (anchor['href'].startswith(start_match))):
                        # if url_complete not in urls_:
                        urls_.append(url_complete)
                        print("adding " + anchor['href'])
                # print(urls_)




        else:
            print("break.")

    # parcourir des uri stockées et appel de la fonction "extractionClaim" pour l'extraction des entités des claims.
    for url in urls_:

        if (not (url in urlTraite)):
            try:

                page = urlopen(url).read()
                urlTraite.append(url)
                if exactractionClaim(page, url, maxClaims) == "break":
                    break

            except:
                print("Cannot open this page. \n")
                continue

        else:
            continue

    # cRubriques=[]
    # for cle, valeur in claimsParRubrique.items():
    # 	cRubriques= cRubriques+ relationsEntreLesClaims.relationClaims(3, cle, valeur)
    #
    #
    # print("URI without claims :" +str(uriSansClaim))
    # .sort_values(by= "idClaim")
    # cRubriques+

    pdf = pd.DataFrame(claims)
    pdf=pdf.assign(id=(pdf['ind_claim']).astype('category').cat.codes)
    # pdf['ind_id']=pdf.groupby('ind_claim').ngroup()
    print(pdf)
    print("number of articles: " + str(count_url))
    # print("number of articles having body but without summarized claim: " + str(uriSansClaim))
    # print("number of articles without body: " + str(len(urls_)))
    # print(urls_)

    # print(summ_claim_per_article)
    # print(ind_claim_per_article)
    # print("Number of Articles having more than one summarized claim: " + str(article_more_than_one_Sclaim))
    # print("Articles having more than one summarized claim and more individual claims than summarized claims: " + str(
    #     article_indClaim_gt_Sclaim))

    return pdf


