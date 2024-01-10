import json

""" 
--- Parametre de la config reseau ---
"""

""" AS 111 """

# Nom AS
Nom_AS1 = "111"
# Nombre de routeur
N1 = 3
#numeros des routers dans l'AS :
L1 = [1,2,3]
# Protocole interne
Protocole_AS1 = "RIPng"
# Graphe d'adjacence de taille N1xN1
M1 = [[0,1,1],[1,0,1],[1,1,0]]
# Masque reseau
Masque1 = "111::0/40"
# Routeur bordeur
ID_routeur_bordeur1 = 3

""" AS 112 """

# Nom AS
Nom_AS2 = "112"
# Nombre de routeur
N2 = 3
#numeros des routers dans l'AS :
L2 = [4,5,6]
# Protocole interne
Protocole_AS2 = "OSPF" 
# Graphe d'adjacence de taille N2xN2
M2 = [[0,1,1],[1,0,1],[1,1,0]]
# Masque reseau
Masque2 = "112::0/40"
# Routeur bordeur
ID_routeur_bordeur2 = 3               ############## cest pas 4 ici ?


"""
Creation du dictionnaire vide
"""

config = {
     Nom_AS1 : { "Nombre_routeur" : N1 , "Liste_router" : L1, "Matrice_adjacence" : M1 , "Masque_reseau" : Masque1 , "Matrice_adressage" : [["","",""],["","",""],["","",""]] , "Routage_intraAS" : { "Protocol" : Protocole_AS1 , "Attribut" : "" } , "Routage_interAS" : { "Protocol" : "BGP" , "ID_routeur_bordeur" : ID_routeur_bordeur1 , "Remote_AS" : Nom_AS2 , "Attribut" : "" } },
     Nom_AS2 : { "Nombre_routeur" : N2 , "Liste_router" : L2, "Matrice_adjacence" : M2 , "Masque_reseau" : Masque2 , "Matrice_adressage" : [["","",""],["","",""],["","",""]] , "Routage_intraAS" : { "Protocol" : Protocole_AS2 , "Attribut" : "" } , "Routage_interAS" : { "Protocol" : "BGP" , "ID_routeur_bordeur" : ID_routeur_bordeur2 , "Remote_AS" : Nom_AS1 , "Attribut" : "" } },
}

""" 
Fonction Adressage_AS(Nom_As , Matrice_adjacence , Nombre_routeur) --> None
Configure les masques reseau et les adresses des liens d'une AS dans le fichier json
"""
def Adressage_AS(Nom_AS , Matrice_adjacence, Nombre_routeur) :
        for i in range(Nombre_routeur) :
            for j in range(Nombre_routeur) :
                if Matrice_adjacence[i][j] :
                     adresse_unique1 = config[Nom_AS]["Masque_reseau"][:3]+":0:"+str(i+1)+"::"+"1/64"
                     adresse_unique2 = config[Nom_AS]["Masque_reseau"][:3]+":0:"+str(i+1)+"::"+"2/64"
                     config[Nom_AS]["Matrice_adressage"][i][j] = adresse_unique1
                     config[Nom_AS]["Matrice_adressage"][j][i] = adresse_unique2
                     

"""
Programme principal
"""
Adressage_AS(Nom_AS1,M1,N1) # Adressage de l'AS1
Adressage_AS(Nom_AS2,M2,N2) # Adressage de l'AS2

fichier = open("config.json","w") # Creation du fichier json
json.dump(config, fichier, indent=4)


