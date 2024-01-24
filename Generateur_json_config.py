import json

""" 
--- Parametre de la config reseau ---

      Pour rajouter un AS :
      - rajouter le champs de l'AS juste en dessous
      - rajouter une clé/valeur dans le dictionnaire config correspondant à la configuration de l'AS
      - adapter les autres AS pour les connexions entre AS dans le dictionnaire config
      - rajouter un appel a la fonction Adressage_AS pour l'AS voulu
      - relancer les fichiers pythons 
"""


""" AS 1 """

# Num AS
Num_AS1 = 1
# Nombre de routeur
N1 = 4
# Protocole interne
Protocole_AS1 = "RIPng"
# Graphe d'adjacence de taille N1xN1
M1 = [[0,1,0,0],
      [1,0,1,0],
      [0,1,0,1],
      [0,0,1,0]]

# Masque reseau interface physique
Masque1 = "111::0/48"
# Masque loopback
Masque_loopback1 = "5000::0/64"
# Routeur bordeur
Num_routeur_bordeur1 = 3

""" AS 2 """

# Num AS
Num_AS2 = 2
# Nombre de routeur
N2 = 3
# Protocole interne
Protocole_AS2 = "OSPF"
# Graphe d'adjacence de taille N2xN2
M2 = [[0,1,0],[1,0,1],[0,1,0]]
# Masque reseau interface physique
Masque2 = "112::0/48"
# Masque loopback
Masque_loopback2 = "5000::0/64"
# Routeur bordeur
Num_routeur_bordeur2 = 3

""" AS 3 """

# Num AS
Num_AS3 = 3
# Nombre de routeur
N3 = 3
# Protocole interne
Protocole_AS3 = "OSPF"
# Graphe d'adjacence de taille N2xN2
M3 = [[0,1,0],[1,0,1],[0,1,0]]
# Masque reseau interface physique
Masque3 = "113::0/48"
# Masque loopback
Masque_loopback3 = "5000::0/64"
# Routeur(s) bordeur(s)
Num_routeur_bordeur3 = 2

"""
A rajouter plus tard :
- Generateur du graphe d'adjacence à partir de quelque chose plus pratique
"""

# Generateur de la matrice d'adressage vide
def Matrice_addressage_vide(M_ad, N) :
   for i in range(N) :
      M_temp = []
      for j in range(N) :
         M_temp.append(["",""])
      M_ad.append(M_temp)

M_ad1, M_ad2, M_ad3 = [], [], []
Matrice_addressage_vide(M_ad1, N1)
Matrice_addressage_vide(M_ad2, N2)
Matrice_addressage_vide(M_ad3, N3)

"""
Creation du dictionnaire vide
"""

config = {
   Num_AS1:{
      "Nombre_routeur":N1,
      "Matrice_adjacence":M1,
      "Masque_reseau":Masque1,
      "Maque_loopback":Masque_loopback1,
      "Matrice_adressage_interface": M_ad1,
      "Donnees_routeurs":{
      },
      "Routage_intraAS":{
         "Protocol":Protocole_AS1,
         "Attribut":""
      },
      "Routage_interAS":{
         Num_routeur_bordeur1 : {
            Num_AS2 : {
               "Num_routeur_bordeur_remote": Num_routeur_bordeur2,
               "Protocole": "BGP",
               "Adresse": "",
               "Interface":""
            },
            Num_AS3 : {
               "Num_routeur_bordeur_remote": Num_routeur_bordeur3,
               "Protocole": "BGP",
               "Adresse": "",
               "Interface":""
            }
         }
      }
   },
   Num_AS2:{
      "Nombre_routeur":N2,
      "Matrice_adjacence":M2,
      "Masque_reseau":Masque2,
      "Maque_loopback":Masque_loopback2,
      "Matrice_adressage_interface":M_ad2,
      "Donnees_routeurs":{     
      },
      "Routage_intraAS":{
         "Protocol":Protocole_AS2,
         "Attribut":""
      },
      "Routage_interAS":{
         Num_routeur_bordeur2 : {
            Num_AS1 : {
               "Num_routeur_bordeur_remote": Num_routeur_bordeur1,
               "Protocole": "BGP",
               "Adresse": "",
               "Interface":""
            }
         }
      }
   },
   Num_AS3:{
      "Nombre_routeur":N3,
      "Matrice_adjacence":M3,
      "Masque_reseau":Masque3,
      "Maque_loopback":Masque_loopback3,
      "Matrice_adressage_interface":M_ad3,
      "Donnees_routeurs":{     
      },
      "Routage_intraAS":{
         "Protocol":Protocole_AS3,
         "Attribut":""
      },
      "Routage_interAS":{
         Num_routeur_bordeur3 : {
            Num_AS1 : {
               "Num_routeur_bordeur_remote": Num_routeur_bordeur1,
               "Protocole": "BGP",
               "Adresse": "",
               "Interface":""
            }
         }
      }
   }
}

# Generateur de la base de donnee des routeurs : Num_routeur, Nom, Dynamips_ID
Dynamips_ID = 1
for i in range(1,len(config)+1) :
   for j in range(1,globals()["N"+str(i)]+1) :
      Num_routeur = j
      config[i]["Donnees_routeurs"][Num_routeur] = {"Nom":"AS"+str(i)+"_R"+str(j) , "Dynamips_ID":Dynamips_ID  , "Attributs":""}
      Dynamips_ID = Dynamips_ID +1

""" 
Fonction Adressage_AS(Nom_As, Matrice_adjacence, Nombre_routeur) --> None
Configure les adresses et les interfaces des liens d'une AS et inter AS dans le fichier json
"""
def Adressage_AS(Num_AS , Matrice_adjacence, Nombre_routeur) :
   nb_connexions = [0 for i in range(Nombre_routeur)]
   for routeur in range(Nombre_routeur) :
      for lien in range(routeur,Nombre_routeur) :
         if Matrice_adjacence[routeur][lien] :
            nb_connexions[routeur]+=1
            nb_connexions[lien]+=1
            interface1 = "GigabitEthernet" + str(nb_connexions[routeur]) + "/0"
            interface2 = "GigabitEthernet" + str(nb_connexions[lien]) + "/0"

            adresse_unique1 = config[Num_AS]["Masque_reseau"][:3]+":0:0:"+str(routeur+1)+"::"+"1/64"
            adresse_unique2 = config[Num_AS]["Masque_reseau"][:3]+":0:0:"+str(routeur+1)+"::"+"2/64"
            config[Num_AS]["Matrice_adressage_interface"][routeur][lien] = [adresse_unique1,interface1]
            config[Num_AS]["Matrice_adressage_interface"][lien][routeur] = [adresse_unique2, interface2]
      routeur+=1
      if routeur in list(config[Num_AS]["Routage_interAS"].keys()) :
         for remote_AS in list(config[Num_AS]["Routage_interAS"][routeur].keys()) :
            nb_connexions[routeur-1]+=1
            config[Num_AS]["Routage_interAS"][routeur][remote_AS]["Interface"] = "GigabitEthernet" + str(nb_connexions[routeur-1]) + "/0"
            if Num_AS > remote_AS :
               config[Num_AS]["Routage_interAS"][routeur][remote_AS]["Adresse"] = "2000:"+str(Num_AS)+str(remote_AS)+"::"+str(Num_AS)+"/32"
            else :
               config[Num_AS]["Routage_interAS"][routeur][remote_AS]["Adresse"] = "2000:"+str(remote_AS)+str(Num_AS)+"::"+str(Num_AS)+"/32"

"""
Programme principal
"""

Adressage_AS(Num_AS1,M1,N1) # Adressage de l'AS1
Adressage_AS(Num_AS2,M2,N2) # Adressage de l'AS2
Adressage_AS(Num_AS3,M3,N3) # Adressage de l'AS3

fichier = open("config.json","w") # Creation du fichier json
json.dump(config, fichier, indent=4)
