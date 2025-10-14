# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 09:57:39 2025

@author: saliou.thiam
"""

import requests             
import pandas as pd          
import os       
import duckdb              

# -------------------- Paramètres API ------------------

API_BASE = "https://data.ameli.fr/api/records/1.0/search/"  # URL de base de l'API (Ameli)
DATASET  = "effectifs"                                      # Nom du dataset cible 
ROWS     = 100                                             # Nombre de lignes à garder 



# -------------------- Paramètres DuckDB ------------------
DB_PATH  = os.path.join("data", "ameli_idf.duckdb")  # chemin où le fichier .duckdb (sera créé )
TABLE    = "cancers_idf"                             # nom de la table cible dans DuckDB



def fetch_idf_cancers() -> pd.DataFrame:
    """
    Récupère des enregistrements pour l'Île-de-France (region=11) ET patho_niv1='Cancers'.
    """

    ##parametre a appliqué pour notre filtre avec idf=11 et patho_niv1=Cancers
    paramsA = {
        "dataset": DATASET,               
        "rows": ROWS,                     
        "refine.region": "11",            
        "refine.patho_niv1": "Cancers",   
    }
    r = requests.get(API_BASE, params=paramsA, timeout=60)  # Appel GET avec paramètres (encodage géré par requests)
    #print("URL (IDF + Cancers) :", r.url)                   # Affiche l'URL finale 
    r.raise_for_status()                                    # Vérification si la réponse HTTP est “OK
    recs = r.json().get("records", [])                      # Parse la réponse JSON et récupère la liste 'records'
    print("Records (API IDF + Cancers) :", len(recs))       # check sur le nombre de lignes renvoyé par l' API


##boucle pour recuperer les fields et l'id de l'api 
    rows = []                                               
    for rec in recs:                                        
        f = rec.get("fields", {})                           
        f["_recordid"] = rec.get("recordid")                
        rows.append(f)                                      
    df = pd.DataFrame(rows)                                 # Conversion liste de dicts -> DataFrame
    if not df.empty:                                        
        return df                                           
                                                             




# fonction pour la creation de la base avec duckdb

def save_to_duckdb(df: pd.DataFrame) -> None:
    """
    Crée/ouvre la base DuckDB, réinitialise la table, insère df, puis affiche le nombre de ligne de la TABLE.
    """
    
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  #check du path

    
    db = duckdb.connect(DB_PATH) # creation de la base DuckDB 

    try:
       
        db.execute(f"CREATE TABLE IF NOT EXISTS {TABLE} AS SELECT * FROM df LIMIT 0;")  #  Création de la TABLE en recuperant les noms de colonne de la table DataFrame df

       
        db.execute(f"DELETE FROM {TABLE};") #Vide la table avant insertion → le script est idempotent (pas de doublons si on relance)

        
        db.register("df", df) #  Enregistrement du DataFrame 'df' comme vue temporaire nommée 'df' côté DuckDB afin de récuperer les infos

        
        db.execute(f"INSERT INTO {TABLE} SELECT * FROM df;") #  Insérer toutes les lignes du DataFrame dans la TABLE 

        #  Contrôle : afficher le nombre de lignes insérées
        out = db.execute(f"SELECT COUNT(*) AS n FROM {TABLE};").fetchdf()
        print(out)   
    finally:
        
        db.close() #  Fermuture de la connexion




if __name__ == "__main__":
    df = fetch_idf_cancers()      #recuperation de la table dataset depuis l'api ameli                                            

    # ---- Check des résultats ----
    print("\nShape :", df.shape)                                                 # Affiche (nb_lignes, nb_colonnes)
    print("Colonnes :", list(df.columns))                                        # Liste des colonnes disponibles
    print("\nAperçu (5 premières lignes) :")                                     # check des 5 premiers lignes
    print(df.head())

    save_to_duckdb(df)  # creation de la base 
    
    
    
    
    ####Verification si les données sont correctement importées et accessibles dans DuckDB
    con = duckdb.connect("data/ameli_idf.duckdb")

    # Nombre de lignes
    print(con.execute("SELECT COUNT(*) FROM cancers_idf;").fetchdf())

    # 5 premières lignes
    print(con.execute("SELECT * FROM cancers_idf LIMIT 5;").fetchdf())

    # Schéma des colonnes
    print(con.execute("DESCRIBE cancers_idf;").fetchdf())

    con.close()