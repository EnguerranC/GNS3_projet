# Projet GNS3


# Generateur_json_config :
Automatisation de la generation du dictionnaire vide :
- Generateur du graphe d'adjacence (plutôt que de le faire soi-même) à partir de tableaux plus simples à comprendre (Ex : R1 = [R2,R3,R4])
- Generateur d'un graphe d'adressage vide
- Generateur de la base de donnée des routeurs
  Remarque :
  - Chaque routeur a un numero de routeur (unique seulement dans l'AS)
  - Chaque routeur a un nom généré automatiquement (Ex : AS2_R1 )
  - Chaque routeur a un dynamips ID unique généré automatiquement
Fonction :
- Adressage_AS(Nom_As , Matrice_adjacence , Nombre_routeur) --> None : Configure les adresses des liens d'une AS dans le fichier json

# A faire : 
  Routage inter AS :
  - Mettre en forme le json BGP (quelles infos on met dedans...)
  - Des parties à automatiser ?
  - Definir les entrées à parametrer


# Generateur_fichier_cfg :
# / Création du cfg :
- Verifier le dynamips_ID
- Creer/Remplacer les fichiers cfg "[Nom du routeur]_configs_i[Dynamips ID]_startup_config.cfg" dans le dossier "users/patri/GNS3/import/Config_reseau"
  Remarque :
  - Lors de la création de la config graphique sur GNS3 il faut que le nom des routeurs concordent
  - Standard des noms de routeurs : AS[Num_AS]_R[Num_routeur] (Ex : Le routeur de la deuxième ligne de l'AS 1 s'appelle AS1_R2 )
  - Le dynamips ID est un identifiant cree par GNS3 en fonction de l'ordre dans lequel on a placé les routeurs. L'ordre standard est Num_AS croissant > Num_routeur croissant
  - Le Num_routeur correspond à la ligne de ce routeur dans la matrice d'adjacence

# / Initialisation des interfaces :
- Enable ipv6 unicast-routing
- Associer a chaque adresse de la matrice d'adressage une interface GigabitethernetX/0
- Activer ipv6 sur toutes les interfaces
- Creer une interface loopback0 avec une adresse unique generee automatiquement (Ex : 5000::[Dynamips_ID]/128)
# / RIP :

# / OSPF :

# / iBGP :
- Generateur d'ID des routeurs uniques

# A faire : 
- Regarder comment sont fait les cfg pour savoir comment ce sera le plus pratique de faire les boucles

# Test de flexibilité du json :
- Rajout d'un lien ?
- Suppression d'un lien ?
- Rajout d'un routeur ?
- Suppression d'un routeur ?
- Rajout d'un routeur border ?
- Suppression d'un router border ?
- Changer le nom d'un router ?
- Choisir le nom d'un routeur ?


# Notes utiles
