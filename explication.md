## 01_EDA :
### 1. L'Aperçu global (Inspection)

L'action : On charge le fichier CSV et on affiche les premières lignes, la taille du tableau et le type des colonnes.
L'objectif : Comprendre le format. C'est ici que tu constates que TV, Radio, Social Media et Sales sont des chiffres (numériques), tandis que Influencer est du texte (catégorielle).

### 2. La détection des valeurs manquantes (Les "trous")

L'action : On compte combien de cases sont vides dans chaque colonne.
L'objectif : Savoir ce qu'il faudra réparer. C'est à cette étape que tu as découvert qu'il manquait 6 valeurs pour ta variable cible Sales, et quelques autres pour les budgets.

### 3. Les statistiques descriptives et les Outliers (Valeurs extrêmes)

L'action : On calcule la moyenne, la médiane, les minimums et maximums. On utilise souvent des graphiques appelés "boîtes à moustaches" (boxplots).
L'objectif : Repérer les anomalies ou les valeurs aberrantes (outliers). C'est ici que tu as identifié que les colonnes Radio et Social Media contenaient des valeurs bizarres ou extrêmes.

### 4. Les distributions (Analyse Univariée)

L'action : On trace des histogrammes pour chaque colonne séparément.
L'objectif : Voir la forme des données. Est-ce que la plupart des budgets TV sont petits, moyens, ou très élevés ? Cela aide à comprendre le comportement global des campagnes.

### 5. Les corrélations (Analyse Bivariée)

L'action : C'est l'étape la plus stratégique. On croise chaque budget avec ta cible (Sales) à l'aide de nuages de points (scatter plots) ou d'une matrice de corrélation (heatmap).
L'objectif : Déterminer quelle variable a le plus d'impact sur les ventes. C'est à ce moment-là que tu as pu constater que le budget TV est presque parfaitement corrélé aux ventes.

#### En résumé, l'EDA sert uniquement à poser un diagnostic pour savoir comment nettoyer et préparer tes données à l'étape suivante (le Preprocessing).

## 02_Modeling

### 1. La Préparation du terrain (Importations)

On commence par importer les outils nécessaires : pandas pour manipuler les données, et surtout scikit-learn (sklearn), qui contient toutes les briques de notre chaîne de montage (préparation, modèles, évaluation).  

### 2. Le Tri Sélectif (Nettoyage et Split)

Nettoyage ciblé : On supprime les lignes où la cible (Sales) est vide. Si on ne sait pas ce qu'on doit prédire, on ne peut pas apprendre au modèle.  
Le Split (80/20) : On sépare les données en deux groupes.
Le Train set (80%) sert au modèle pour apprendre.
Le Test set (20%) est mis dans un coffre-fort. On ne le sortira qu'à la toute fin pour vérifier si le modèle a bien appris ou s'il a juste appris par cœur (fuite de données).  
+1

### 3. La Chaîne de Préparation (Pipelines & ColumnTransformer)

C'est ici qu'on automatise le nettoyage pour chaque type de donnée :  
Pour les chiffres (TV, Radio, etc.) : Si une case est vide, on met la médiane (imputation). Ensuite, on ramène tout à la même échelle (StandardScaler) pour ne pas qu'une variable écrase les autres.  
Pour le texte (Influencer) : On remplace les vides par la valeur la plus fréquente, puis on transforme les mots en chiffres (OneHotEncoder) car les modèles ne lisent que les chiffres.  
Le ColumnTransformer : C'est le chef d'orchestre qui envoie chaque colonne dans la bonne file de nettoyage.  

### 4. L'Apprentissage (Entraînement des modèles)

On crée trois "cerveaux" différents (pipelines) qui incluent à la fois le nettoyage et l'algorithme :
Régression Linéaire : Le modèle le plus simple, qui cherche une ligne droite.  
Random Forest : Une armée d'arbres de décision qui votent pour la meilleure réponse.  
Gradient Boosting : Un modèle qui apprend de ses erreurs précédentes pour s'améliorer.  

### 5. Le Contrôle Qualité (Évaluation et Cross-Validation)

Évaluation simple : On sort le Test set du coffre-fort. On demande au modèle de prédire, et on compare avec la réalité (RMSE et R 
2
 ).  
+1

Validation Croisée (Cross-Validation) : Comme tu l'as vu sur l'image, on redécoupe le jeu d'entraînement 5 fois pour vérifier que le modèle est stable partout et pas seulement sur un morceau de données.  
+1

### 6. Le Verdict (Conclusion)

Dans ton cas, le Gradient Boosting est le plus précis (RMSE le plus bas : 3.31 et R 
2 le plus haut : 0.9987). C'est donc lui que tu vas choisir d'industrialiser dans ton API et ton Dashboard.