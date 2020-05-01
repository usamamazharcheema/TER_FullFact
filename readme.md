## Prérequis 


Le programme s'exécute avec Python 3.5 +. Les dépendances de package attendues sont répertoriées dans le fichier `requirements.txt` pour PIP. Pour les obtenir,  veuillez exécuter la commande suivante :


```
pip install -r requirements.txt
```



## Exécution du programme


Le  programme s’exécute grâce à la commande suivante :

```
python Exporter.py --website  fullfact
```


## Fichiers



* `Exporter.py` : Le point d’entrée de notre projet (il contient la fonction “main”). Quant au reste des programmes, nous avons :


* `fullfact.py` : se charge -entre autres- d’extraire les entités principales du site Full Fact (claim, conclusion, texte de la revue, titre de la revue, etc).


* `getPosts.py` : récupère les claims, le titre, l’URI et la rubrique des articles qui se trouvent dans la section “related posts” d’une revue donnée.


* `TraitementConclusion.py` : ce programme détermine la valeur de véracité d’un claim (TRUE, FALSE, OTHER, MIXTURE) à partir de sa conclusion.


* `relationsEntreLesClaims.py` : ce programme détermine le lien entre les claims se trouvant dans la même section “related posts”, mais aussi le lien entre les différents claims d’une même rubrique.


* `additionalRows.py` :récupère les claims/conclusions qui se trouvent dans une même revue.


* `Claim.py` : qui se charge de la création de l’objet claim.


* `claimextractor.py` : exporte le résultat de l’extraction en fichier CSV.

## Notes

* Le fichier `output_got.csv` est un exemple du résultat obtenu après l'exécution du programme.
