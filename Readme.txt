========================================
DESCRIPTION DU PROJET
========================================
Ce projet met en place une chaîne reproductible « API → Base locale → Rapport » autour
des données Ameli.

Objectif :
- Récupérer un échantillon de 100 lignes limité à la région Île-de-France (code INSEE 11)
  et à la pathologie « Cancers » ;
- Stocker ces données dans une base DuckDB locale ;
- Produire un rapport descriptif (tableau gtsummary) en HTML.

Pour éviter d’occuper inutilement de la place dans le dépôt, les fichiers générés/volumineux
sont ignorés par Git (voir .gitignore) : la base DuckDB, le rapport HTML et les exports de
données. Ils peuvent être régénérés à partir du code.

========================================
ÉTAPES (COMMENT ÇA FONCTIONNE)
========================================
1) Extraction (Python)
   - Le script appelle l’API Ameli (dataset « effectifs ») avec les filtres :
     • region = 11 (Île-de-France)
     • patho_niv1 = « Cancers »
   - Le résultat est borné à 100 lignes.

2) Stockage (DuckDB)
   - Les 100 lignes sont écrites dans la base locale : data/ameli_idf.duckdb
   - Nom de la table : cancers_idf
   - Un contrôle COUNT(*) et l’affichage des 5 premières lignes confirment l’insertion.

3) Rapport (RMarkdown)
   - Le fichier reports/rapport.Rmd se connecte à la base DuckDB,
     exécute des requêtes simples de contrôle (COUNT, aperçu),
     puis génère un tableau descriptif (gtsummary) en HTML.

4) Reproductibilité
   - Les artefacts (base .duckdb, HTML, exports) ne sont pas versionnés.
   - Relancer le script Python et « knitter » le RMarkdown permet de recréer les résultats.
   - Le rapport HTML attendu après kinit est disponible aussi dans le dossier reports

========================================
PRÉREQUIS
========================================
Outils
- Git
- Python 3.11+ (ou Conda/Anaconda) avec accès Internet
- R et (de préférence) RStudio

Dépendances Python (requirements.txt)
- pandas
- duckdb
- requests

Installation (exemples) :
- Conda :
  conda create -n lejeune python=3.11 -y
  conda activate lejeune
  python -m pip install -r requirements.txt

- Environnement Python existant :
  python -m pip install -r requirements.txt

Dépendances R (à installer une fois dans R/RStudio)
  install.packages(c("rmarkdown","DBI","duckdb","dplyr","gtsummary","gt"))

========================================
INSTRUCTIONS D’EXÉCUTION
========================================
A. Récupérer le projet
- Cloner le dépôt :
  git clone <URL_DU_REPO>
  cd lejeune-test-technique

B. Générer la base locale (Python)
- Assurez-vous d’être à la racine du dépôt (important pour les chemins relatifs).
  • Windows (PowerShell / cmd) :
    python src\fetch_idf_cancers_to_duckdb.py
  • macOS / Linux :
    python3 src/fetch_idf_cancers_to_duckdb.py

- Sortie attendue :
	-Après connexion à l'APIS
 	 	• Affichage du nombre de record récupéré dans l'api 
  		• Affichage des noms des colonnes récupérés
  		• Affichage des 5 premières lignes
       -Après création de la base 
  		• COUNT(*) = 100 en console
  		• Affichage des 5 premières lignes et du schéma de colonnes
  		• Création du fichier data/ameli_idf.duckdb (table cancers_idf)

- Remarques :
  • Si vous exécutez le script depuis un autre répertoire, adaptez le chemin ou lancez-le
    avec un chemin absolu (la ligne à modifier est : 
os.chdir(r"os.chdir(r"C:\Users\saliou.thiam\OneDrive - Groupe Astek\Documents\Dossier Saliou\Test jerome lejeune\lejeune-test-technique")
 ; sinon la base pourrait être créée ailleurs.
  

C. Produire le rapport (RMarkdown)
- Ouvrir RStudio, charger reports/rapport.Rmd , puis cliquer « Knit » (HTML).
- Le rapport affiche un tableau descriptif (gtsummary).
- Pour afficher les contrôles (COUNT, aperçu) si masqués, décommentez les blocs concernés
  dans le code du .Rmd.


========================================
NOTES COMPLÉMENTAIRES
========================================
- Dataset API ciblé : « effectifs » (Ameli).
- Région Île-de-France = code INSEE 11 ; pathologie filtrée : « Cancers ».
- Dans le commit “Added the rapport.Rmd code and the expected HTML report”, le fichier HTML n’a pas été inclus : il a été ajouté directement sur GitHub.
- Pour ajouter le dossier Data (vide), c’était un peu compliqué, donc j’ai forcé le commit à inclure aussi le fichier ameli_idf.duckdb (même s’il est ignoré par le .gitignore)

========================================
ARBORESCENCE DU PROJET (SYNTHÈSE)
========================================
.
├─ src/
│  └─ fetch_idf_cancers_to_duckdb.py   (Extraction API → DuckDB, 100 lignes)
├─ data/
│  └─ ameli_idf.duckdb                 (Base locale — ignorée par Git)
├─ reports/
│  └─ rapport.Rmd                      (RMarkdown → HTML ignoré par Git)
├─ requirements.txt
└─ README.txt






