import json

""" 
--- Parametre de la config reseau ---
"""

""" AS 1 """

# Num AS
Num_AS1 = 1
# Nombre de routeur
N1 = 4
#numeros des routers dans l'AS :
L1 = [1,2,3]
# Protocole interne
Protocole_AS1 = "RIPng"
# Graphe d'adjacence de taille N1xN1
M1 = [[0,1,0,0],
      [1,0,1,0],
      [0,1,0,1],
      [0,0,1,0]]

# Masque reseau interface physique
Masque1 = "111::0/40"
# Masque reseau interface loopback
Masque2_loopback = ""
# Routeur bordeur
Num_routeur_bordeur1 = 3

""" AS 2 """

# Num AS
Num_AS2 = 2
# Nombre de routeur
N2 = 3
#numeros des routers dans l'AS :
L2 = [4,5,6]
# Protocole interne
Protocole_AS2 = "OSPF" 
# Graphe d'adjacence de taille N2xN2
M2 = [[0,1,0],[1,0,1],[0,1,0]]
# Masque reseau interface physique
Masque2 = "112::0/40"
# Masque reseau interface loopback
Masque2_loopback = ""
# Routeur bordeur
Num_routeur_bordeur2 = 3

"""
A rajouter plus tard :
- Generateur du graphe d'adjacence à partir de tableau
"""

# Generateur de la matrice d'adressage vide
M_ad1 = []
for i in range(N1) :
   M_temp = []
   for j in range(N1) :
      M_temp.append("")
   M_ad1.append(M_temp)

M_ad2 = []
for i in range(N2) :
   M_temp = []
   for j in range(N2) :
      M_temp.append("")
   M_ad2.append(M_temp)

"""
Creation du dictionnaire vide
"""

config = {
   Num_AS1:{
      "Nombre_routeur":N1,
      "Matrice_adjacence":M1,
      "Masque_reseau":Masque1,
      "Matrice_adressage":M_ad1,
      "Donnees_routeurs":{
      },
      "Routage_intraAS":{
         "Protocol":Protocole_AS1,
         "Attribut":""
      },
      "Routage_interAS":{
         Num_routeur_bordeur1 : {
            Num_AS2 : {
               "Protocole" : "BGP",
               "Adresse": ""
         }
         }
      }
   },
   Num_AS2:{
      "Nombre_routeur":N2,
      "Matrice_adjacence":M2,
      "Masque_reseau":Masque2,
      "Matrice_adressage":M_ad2,
      "Donnees_routeurs":{     
      },
      "Routage_intraAS":{
         "Protocol":Protocole_AS2,
         "Attribut":""
      },
      "Routage_interAS":{
         Num_routeur_bordeur2 : {
            Num_AS1 : {
               "Protocole" : "BGP",
               "Adresse": ""
         }
         }
      }
   }
}

# Generateur de la base de donnee des routeurs : Num_routeur, Nom, Dynamips_ID
Dynamips_ID = 1
for i in range(1,3) :
   for j in range(1,globals()["N"+str(i)]+1) :
      Num_routeur = j
      config[i]["Donnees_routeurs"][Num_routeur] = {"Nom":"AS"+str(i)+"_R"+str(j) , "Dynamips_ID":Dynamips_ID  , "Attributs":""}
      Dynamips_ID = Dynamips_ID +1

""" 
Fonction Adressage_AS(Nom_As , Matrice_adjacence , Nombre_routeur) --> None
Configure les adresses des liens d'une AS dans le fichier json
"""
def Adressage_AS(Num_AS , Matrice_adjacence, Nombre_routeur) :
        nb_connexions = [0 for i in range(Nombre_routeur)]
        for i in range(Nombre_routeur) :
            for j in range(i,Nombre_routeur) :
               if Matrice_adjacence[i][j] :
                  nb_connexions[i]+=1
                  nb_connexions[j]+=1
                  interface1 = "GigabitEthernet" + str(nb_connexions[i]) + "/0"
                  interface2 = "GigabitEthernet" + str(nb_connexions[j]) + "/0"

                  adresse_unique1 = config[Num_AS]["Masque_reseau"][:3]+":0:0:"+str(i+1)+"::"+"1/64"
                  adresse_unique2 = config[Num_AS]["Masque_reseau"][:3]+":0:0:"+str(i+1)+"::"+"2/64"
                  config[Num_AS]["Matrice_adressage"][i][j] = [adresse_unique1,interface1]
                  config[Num_AS]["Matrice_adressage"][j][i] = [adresse_unique2, interface2]
               
                     

"""
Programme principal
"""
Adressage_AS(Num_AS1,M1,N1) # Adressage de l'AS1
Adressage_AS(Num_AS2,M2,N2) # Adressage de l'AS2

fichier = open("config.json","w") # Creation du fichier json
json.dump(config, fichier, indent=4)


