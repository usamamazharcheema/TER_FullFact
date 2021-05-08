# Explication du fichier CSV obtenu

Le programme récupère 13 colonnes dans un fichier `output_got.csv`. Ci-dessous le contenu de chaque colonne:


### source: 
Comme son nom l'indique, cette colonne représente le site duquel les claims ont été extraites (Full Fact dans notre cas).


### claim:
Cette colonne contient le texte de la claim tel qu'il est présent sur le site.


### body: 
Contient le texte de la revue donnée par le journaliste.


### conclusion:
Cette colonne contient le texte de la conclusion tel qu'il est formulé par le journaliste.


### title:
Comme son nom l'indique également, cette colonne fait référence au titre de l'article.


### date:
Date de publication de l'article sur le site.


### uri:
L'URI de l'article.


### rubrique:
La thématique de l'article. Le site Full Fact contient bon nombre de rubriques, dont: law, economy, europe, health, crime, immigration, education et online.


### valeur_de_véracité: 
Cette colonne contient le résultat du traitement de la conclusion de chaque claim, autrement dit la valeur de véracité de la claim {TRUE, FALSE, MIXTURE ou OTHER}.


### idClaim:
Représente l'identifiant de la claim. Les claims qui ont le même identifiant font partie du même article; en effet, comme nous l'avons expliqué dans le rapport, un article peut avoir une seule claim, tout comme il peut se retrouver avec deux ou trois,voire sept claims. 


### related_posts:
Cette colonne renferme un dictionnaire de listes:

* `RelatedPosts` : liste des URI des articles présents dans la section "Related posts". Toujours comme expliqué dans notre rapport, outre les parties "claim-conclusion-revue", chaque article possède une rubrique "Related Posts". Cette rubrique contient des liens vers cinq autres articles en rapport de près ou de loin avec ledit article.

* `ClaimsSimilaires` : liste des URI des articles appartenant à une même rubrique et traitant des mêmes thématiques.


### keywords:
Comme la colonne précédente, celle là aussi contient un dictionnaire de listes:

* `RelatedPosts` : ensemble des mots clés reliant un article aux articles présents dans la même section "Related posts".

* `ClaimsSimilaires` : ensemble des mots clés reliant les articles appartenant à une même rubrique et traitant des mêmes thématiques.

Les deux ensembles de mots clés sont les résultats de la clusterisation à l'aide de l'algorithme K-means.


### liens_revue:
Liste contenant les différentes URI présentes dans la revue.