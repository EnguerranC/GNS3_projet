import json

""" 
--- Parametre de la config reseau ---
"""
# Temp
Num_routeur = 1
Dynamips_ID = 1

""" AS 1 """

# Num AS
Num_AS1 = 1
# Nombre de routeur
N1 = 3
# Protocole interne
Protocole_AS1 = "RIPng"
# Graphe d'adjacence de taille N1xN1 (a modifier avec tableau plus comprehensibles)
M1 = [[0,1,1],[1,0,1],[1,1,0]]
# Masque reseau
Masque1 = "111::0/40"
# Routeur bordeur
Num_routeur_bordeur1 = 3

""" AS 2 """

# Num AS
Num_AS2 = 2
# Nombre de routeur
N2 = 3
# Protocole interne
Protocole_AS2 = "OSPF" 
# Graphe d'adjacence de taille N2xN2 (a modifier avec tableau plus comprehensibles)
M2 = [[0,1,1],[1,0,1],[1,1,0]]
# Masque reseau
Masque2 = "112::0/40"
# Routeur bordeur
Num_routeur_bordeur2 = 3

"""
Automatisation de la generation du dictionnaire vide :
- Generateur du graphe d'adjacence
- Generateur du graphe vide
- Generateur de la base de donnee des routeurs :
   - Numero de routeur (unique seulement dans l'AS)
   - Nom du routeur (Ex : AS1_R2)
   - Dynamips_ID unique
"""


"""
Creation du dictionnaire vide
"""

config = {
   Num_AS1:{
      "Nombre_routeur":N1,
      "Matrice_adjacence":M1,
      "Masque_reseau":Masque1,
      "Matrice_adressage":[
         [
            "",
            "",
            ""
         ],
         [
            "",
            "",
            ""
         ],
         [
            "",
            "",
            ""
         ]
      ],
      "Donnees_routeurs":{
           Num_routeur :{ "Nom":"" , "Dynamips_ID" : Dynamips_ID , "Attributs":""
                
           },
           Num_routeur :{ "Nom":"" , "Dynamips_ID" : Dynamips_ID , "Attributs":""
                
           }
      },
      "Routage_intraAS":{
         "Protocol":Protocole_AS1,
         "Attribut":""
      },
      "Routage_interAS":{
         "Protocol":"BGP",
         "Num_routeur_bordeur":Num_routeur_bordeur1,
         "Remote_AS":Num_AS2,
         "Attribut":""
      }
   },
   Num_AS2:{
      "Nombre_routeur":N2,
      "Matrice_adjacence":M2,
      "Masque_reseau":Masque2,
      "Matrice_adressage":[
         [
            "",
            "",
            ""
         ],
         [
            "",
            "",
            ""
         ],
         [
            "",
            "",
            ""
         ]
      ],
      "Donnees_routeurs":{
           Num_routeur :{ "Nom":"" , "Dynamips_ID" : Dynamips_ID , "Attributs":""
                
           },
           Num_routeur :{ "Nom":"" , "Dynamips_ID" : Dynamips_ID , "Attributs":""
                
           }
      },
      "Routage_intraAS":{
         "Protocol":Protocole_AS2,
         "Attribut":""
      },
      "Routage_interAS":{
         "Protocol":"BGP",
         "Num_routeur_bordeur":Num_routeur_bordeur2,
         "Remote_AS":Num_AS1,
         "Attribut":""
      }
   }
}

""" 
Fonction Adressage_AS(Nom_As , Matrice_adjacence , Nombre_routeur) --> None
Configure les adresses des liens d'une AS dans le fichier json
"""
def Adressage_AS(Nom_AS , Matrice_adjacence, Nombre_routeur) :
        for i in range(Nombre_routeur) :
            for j in range(Nombre_routeur) :
                if Matrice_adjacence[i][j] :
                     adresse_unique1 = config[Nom_AS]["Masque_reseau"][:3]+":0:0:0:"+str(i+1)+"::"+"1/64"
                     adresse_unique2 = config[Nom_AS]["Masque_reseau"][:3]+":0:0:0:"+str(i+1)+"::"+"2/64"
                     config[Nom_AS]["Matrice_adressage"][i][j] = adresse_unique1
                     config[Nom_AS]["Matrice_adressage"][j][i] = adresse_unique2
                     

"""
Programme principal
"""
Adressage_AS(Num_AS1,M1,N1) # Adressage de l'AS1
Adressage_AS(Num_AS2,M2,N2) # Adressage de l'AS2

fichier = open("config.json","w") # Creation du fichier json
json.dump(config, fichier, indent=4)


