## TER_FullFact

Extraction de connaissances et clusterisation des claims à partir du site britanique de fact-checking [fullfact](https://fullfact.org/)


## Description

* Projet réalisé dans le cadre du Travail d'Étude et de Recherche (TER) de Master 1. 
* Ci-dessous les travaux que nous avons réalisés : 
	* Extraction des claims, revues et conclusions associées à partir du site [fullfact](	https://fullfact.org/) en tenant compte de sa structure particulière.

	* Traitement des conclusions associées aux claims pour extraire la valeur de véracité. 		Nous avons pour cela développer une méthode d'éxtraction symbolique en s'appuyant sur 		des patterns que nous avons définis en analysant le site.
	* Clusterisation des claims selon leur catégorie : Santé, Economy, Europe, Education, 		etc.
	* Structuration des claims et de leurs méta-données en suivant le modèle de données du 		graphe de connaissances [claimsKG](https://data.gesis.org/claimskg/).
	
	

## Prérequis 


Le programme s'exécute avec Python 3.5 +. Les dépendances de packages attendues sont répertoriées dans le fichier `requirements.txt` pour PIP. Pour les obtenir,  veuillez exécuter la commande :


```
pip install -r requirements.txt
```



## Exécution du programme


* Une fois positionné dans le repertoire `src`, le programme s’exécute grâce à la commande suivante :

```
python Exporter.py --website  fullfact --maxClaims  <le nombre de claims que vous voulez recupérer>  --output  <nom du fichier résultat>
```





* Les paramètres 'website', 'maxClaims' et 'output' sont définis par défaut dans le fichier 'Criteria.py'. Dans le cas où vous ne faites entrer aucun paramètre, le programme se chargera automatiquement d'extraire 500 claims et stockera les résultats dans un fichier nommé `output_got.csv` :

```
python Exporter.py
```





## Fichiers



* `Exporter.py` : Le point d’entrée de notre projet (il contient la fonction “main”). Quant au reste des programmes, nous avons :


* `fullfact.py` : se charge -entre autres- d’extraire les entités principales du site Full Fact (claim, conclusion, texte de la revue, titre de la revue, etc).


* `getPosts.py` : récupère les claims, le titre, l’URI et la rubrique des articles qui se trouvent dans la section “related posts” d’une revue donnée.


* `TraitementConclusion.py` : ce programme détermine la valeur de véracité d’une claim (TRUE, FALSE, OTHER, MIXTURE) à partir de sa conclusion.


* `relationsEntreLesClaims.py` : ce programme détermine le lien entre les claims se trouvant dans la même section “related posts”, mais aussi le lien entre les différentes claims d’une même rubrique.


* `additionalRows.py` :récupère les claims/conclusions qui se trouvent dans une même revue.


* `Claim.py` : se charge de la création de l’objet claim.


* `claimextractor.py` : fait appel au fichier fullfact.py et exporte le résultat de l’extraction en fichier CSV.


*  `Criteria.py` : se charge d'initialiser les paramètres d'extraction du programme.

## Notes

* Le repertoire `results` contient un fichier `output_got.csv`: un exemple du résultat obtenu après l'exécution du programme.
* Le repertoire `notebooks` contient :
  * `lienEntrePostsDeChaqueRubrique.ipynb` explicant le programme `.py` du partionnement des claims en clusters et l'extraction des mots clés associés à chaque cluster. Ce notebook contient également une analyse des résultats obtenus.

## Auteurs

* Nihed Bendahman
* Maroua Dorsaf Djelouat
* Cheimae Assarar

