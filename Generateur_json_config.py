import json

""" 
--- Parametre de la config reseau ---

      Pour rajouter un AS, rajouter juste l'AS et ses caractéristiques dans le dico config et modifier les autres AS pour les éventuels liens
"""


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
   return M_ad


"""
Creation du dictionnaire à moitié vide
"""

config = {
   1 : {
      "Nombre_routeur" : 4,
      "Type_AS" : "AS",
      "Matrice_adjacence" : [[0,1,0,0],
                             [1,0,1,0],
                             [0,1,0,1],
                             [0,0,1,0]],
      "Masque_reseau" : "111::0/48",
      "Maque_loopback" : "5000::0/64",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 4),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : "RIPng",
         "Attribut" : ""
      },
      "Routage_interAS":{
         3 : {
            2 : {
               "Num_routeur_bordeur_remote" : 3,
               "Protocole" : "BGP",
               "Adresse" : "",
               "Interface" : ""
            }
         },
         2 : {
            3 : {
               "Num_routeur_bordeur_remote" : 1,
               "Protocole" : "BGP",
               "Adresse" : "",
               "Interface" : ""
            }
         },
         1 : {
            4 : {
               "Num_routeur_bordeur_remote" : 1,
               "Protocole" : "BGP",
               "Adresse" : "",
               "Interface" : ""
            }
         },
         4 : {
            5 : {
               "Num_routeur_bordeur_remote" : 1,
               "Protocole" : "BGP",
               "Adresse" : "",
               "Interface" : ""
            }
         }
      }
   },
   2 : {
      "Nombre_routeur" : 4,
      "Type_AS" : "AS",
      "Matrice_adjacence" : [[0,1,0,0],
                             [1,0,1,0],
                             [0,1,0,1],
                             [0,0,1,0]],
      "Masque_reseau" : "112::0/48",
      "Maque_loopback" : "5000::0/64",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 4),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : "OSPF",
         "Attribut" : ""
      },
      "Routage_interAS":{
         3 : {
            1 : {
               "Num_routeur_bordeur_remote" : 3,
               "Protocole" : "BGP",
               "Adresse" : "",
               "Interface" : ""
            }
         },
         2 : {
            6 : {
               "Num_routeur_bordeur_remote" : 1,
               "Protocole" : "BGP",
               "Adresse" : "",
               "Interface" : ""
            }
         },
         1 : {
            3 : {
               "Num_routeur_bordeur_remote" : 1,
               "Protocole" : "BGP",
               "Adresse" : "",
               "Interface" : ""
            }
         }
      }
   },
   3 : {
      "Nombre_routeur" : 1,
      "Type_AS" : "Provider",
      "Matrice_adjacence" : [[0]],
      "Masque_reseau" : "113::0/48",
      "Maque_loopback" : "5000::0/64",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 1),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : "",
         "Attribut" : ""
      },
      "Routage_interAS":{
         1 : {
            2 : {
               "Num_routeur_bordeur_remote" : 1,
               "Protocole" : "BGP",
               "Adresse" : "",
               "Interface" : ""
            },
            1 : {
               "Num_routeur_bordeur_remote" : 2,
               "Protocole" : "BGP",
               "Adresse" : "",
               "Interface" : ""
            }
         }         
      }
   },
   4 : {
      "Nombre_routeur" : 1,
      "Type_AS" : "Peer",
      "Matrice_adjacence" : [[0]],
      "Masque_reseau" : "114::0/48",
      "Maque_loopback" : "5000::0/64",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 1),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : "",
         "Attribut" : ""
      },
      "Routage_interAS":{
         1 : {
            1 : {
               "Num_routeur_bordeur_remote" : 1,
               "Protocole" : "BGP",
               "Adresse" : "",
               "Interface" : ""
            }
         }
      }
   },
   5 : {
      "Nombre_routeur" : 1,
      "Type_AS" : "Client",
      "Matrice_adjacence" : [[0]],
      "Masque_reseau" : "115::0/48",
      "Maque_loopback" : "5000::0/64",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 1),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : "",
         "Attribut" : ""
      },
      "Routage_interAS":{
         1 : {
            1 : {
               "Num_routeur_bordeur_remote" : 4,
               "Protocole" : "BGP",
               "Adresse" : "",
               "Interface" : ""
            }
         }
      }
   },
   6 : {
      "Nombre_routeur" : 1,
      "Type_AS" : "Client",
      "Matrice_adjacence" : [[0]],
      "Masque_reseau" : "116::0/48",
      "Maque_loopback" : "5000::0/64",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 1),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : "",
         "Attribut" : ""
      },
      "Routage_interAS":{
         1 : {
            2 : {
               "Num_routeur_bordeur_remote" : 2,
               "Protocole" : "BGP",
               "Adresse" : "",
               "Interface" : ""
            }
         }
      }
   },
}

# Generateur de la base de donnee des routeurs : Num_routeur, Nom, Dynamips_ID
Dynamips_ID = 1
for i in range(1,len(config)+1) :
   for j in range(1, config[i]["Nombre_routeur"]+1) :
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
for i in range(len(config)) : 
   Adressage_AS(i+1, config[i+1]["Matrice_adjacence"], config[i+1]["Nombre_routeur"])

fichier = open("config.json","w") # Creation du fichier json
json.dump(config, fichier, indent=4)
