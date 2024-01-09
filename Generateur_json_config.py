import json

""" 
--- Parametre de la config reseau ---

- Configuration interne des AS

"""

""" AS 111 """

# Nom AS
Nom_AS1 = "111"

# Nombre de routeur
N1 = 3

# Protocole interne
Protocole_AS1 = "RIPng"

# Graphe d'adjacence de taille N1xN1
M1 = [[0,1,1],[1,0,1],[0,1,0]]

""" AS 112 """

# Nom AS
Nom_AS2 = "112"

# Nombre de routeur
N2 = 3

# Protocole interne
Protocole_AS2 = "OSPF" 

# Graphe d'adjacence de taille N2xN2
M2 = [[0,1,1],[1,0,1],[0,1,0]]

"""
Creation du dictionnaire vide
"""

config = {
     Nom_AS1 : { "Nombre_routeur" : N1 , "Matrice_adjacence" : M1 , "Matrice_adressage" : [["","",""],["","",""],["","",""]] },
     Nom_AS2 : { "Nombre_routeur" : N2 , "Matrice_adjacence" : M2 , "Matrice_adressage" : [["","",""],["","",""],["","",""]] }
}

""" 
Fonction Adressage_AS(Nom_As ; Nombre_routeur) --> None
Configure les adresses des routeurs d'une AS dans le fichier json 
"""
def Adressage_AS(Nom_AS , Matrice_adjacence, Nombre_routeur) :
        for i in range(Nombre_routeur) :
            for j in range(Nombre_routeur) :
                if Matrice_adjacence[i][j] :
                     addresse_unique1 = Nom_AS+"."+str(i)+"::"+"1"
                     addresse_unique2 = Nom_AS+"."+str(i)+"::"+"2"
                     config[Nom_AS]["Matrice_adressage"][i][j] = addresse_unique1
                     config[Nom_AS]["Matrice_adressage"][j][i] = addresse_unique2
                     

"""
Programme principal
"""
Adressage_AS(Nom_AS1,M1,N1)
Adressage_AS(Nom_AS2,M2,N2)

fichier = open("config.json","w")
json.dump(config, fichier)


