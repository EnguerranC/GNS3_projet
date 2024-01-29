# Projet GNS3


# Generateur_json_config :

# / Programme
Automatisation de la generation du dictionnaire vide :
- Generateur d'un graphe d'adressage vide
- Generateur de la base de donnée des routeurs
  Remarque :
  - Chaque routeur a un numero de routeur (unique seulement dans l'AS)
  - Chaque routeur a un nom généré automatiquement (Ex : AS2_R1 )
  - Chaque routeur a un dynamips ID unique généré automatiquement
  - Le dynamips ID est un identifiant cree par GNS3 en fonction de l'ordre dans lequel on a placé les routeurs. L'ordre standard est Num_AS croissant > Num_routeur croissant
Fonction :
- Adressage_AS(Nom_As , Matrice_adjacence , Nombre_routeur) --> None : Configure les adresses des liens d'une AS dans le fichier json /FAIT

# / Json
Explication du json :
- Première clé : le numéro de l'AS, simple incrémentation suivant le nombre d'AS
- Deuxième clé : les clés suivantes sont les caractéristiques au sein de l'AS
  - "Masque_reseau" : le masque utilisé pour les routers de l'AS
  - "Matrice_adressage_interface" : la matrice d'adressage et d'interfaces où chaque élément vaut : soit ["",""] si il n'y a pas de lien entre les routers correspondants; soit une liste où le premier élément est l'adresse et le deuxième est l'interface utilisée. Chaque ligne correspond à la configuration du router dont le numéro correspond à l'indice de la ligne
  - "Donnees_routeurs" : les clés correspondent au numero du router dans l'AS, simple incrémentation suivant le nombre de routers comme pour les AS; les clés suivantes donnent le dynamips ID et le Nom de chaque router
  - "Routage_intraAS" : le protocole utilisé dans l'AS
  - "Routage_interAS" : 
    - Première clé : le numéro du router de bordure considéré
    - Deuxième clé : le numéro de l'AS qui est relié à l'AS courante par le router de bordure
  
Suggestions :
- Rajouter les loopbacks dans le json pour simplifier le code ?



# Generateur_fichier_cfg pour chacun des routeurs :

# / Création du cfg :
- Verifier le dynamips_ID /A FAIRE
- Creer/Remplacer les fichiers cfg "[Nom du routeur]_configs_i[Dynamips ID]_startup_config.cfg" dans le dossier "users/.../GNS3/import/Config_reseau" /A MODIFIER
  Remarque :
  - Creer un dossier import pour que ca soit plus clair (au même endroit ou il y a deja le dossier projects)
  - Lors de la création de la config graphique sur GNS3 il faut que le nom des routeurs concordent
  - Standard des noms de routeurs : AS[Num_AS]_R[Num_routeur] (Ex : Le routeur de la deuxième ligne de l'AS 1 s'appelle AS1_R2 )
  - Le dynamips ID est un identifiant cree par GNS3 en fonction de l'ordre dans lequel on a placé les routeurs. L'ordre standard est Num_AS croissant > Num_routeur croissant
  - Le Num_routeur correspond à la ligne de ce routeur dans la matrice d'adjacence

# / Initialisation du routeur:
- Enable Ipv6 unicast-routing
- Protocol de routage intra AS :
  - RIP : redistribute connected : actif ou non
  - OSPF :

# / Interface loopback0 :
- Enable ipv6 
- Enable le protocol de routage intra As (RIP ou OSPF)
- Associer a une adresse avec une adresse unique generee automatiquement (Ex : 5000::[Dynamips_ID]/128)

# / Interface GigabitEthernetX/0
- Enable ipv6
- Associer a une adresse avec l'adresse dans la matrice d'adressage correspondante
- Enable le protocol de routage intra AS (RIP ou OSPF)

# / iBGP :
- Generateur d'ID des routeurs uniques à partir de la Dynamips ID
- Set les neighbors avec la matrice d'adjacence et leur loopback associée
- Activer les loopback des routeurs de l'AS
Remarque : Il me semble qu'il n'y a pas besoin de network advertisement pour les routeurs qui ne sont pas en bordure


# A FAIRE
Obj : Configurer les AS séparées avec leur protocol de routage intra AS
- Finir generateur de json /FAIT
- Finir generateur de cfg /ENGUERRAN
Obj : A definir


# Test de flexibilité de l'automatisation :
- Rajout d'un lien ?
- Suppression d'un lien ?
- Rajout d'un routeur ?
- Suppression d'un routeur ?
- Rajout d'un routeur border ?
- Suppression d'un router border ?
- Changer le nom d'un router ?
- Choisir le nom d'un routeur ?

# Config BGP

# / Communauté fromprovider : à mettre dans tous les routeurs qui sont bordeur avec un provider

# // Addresse-family ipv6
neighbor [addresse du routeur provider] route-map fromprovider in
# // Route Map
route-map fromprovider permit [numero de prio
  set community 1
# // Ip community-list
ip community-list standard provider permit 1

# / Communauté fromclient : à mettre dans tous les routeurs qui sont bordeur avec un client

# // Addresse-family ipv6
neighbor [addresse du routeur client] route-map fromclient in
# // Route Map
route-map fromclient permit [numero de prio]
 set community 2
# // Ip community-list
ip community-list standard client permit 2

# / Communauté frompeer : à mettre dans tous les routeurs qui sont bordeur avec un peer

# // Addresse-family ipv6
neighbor [addresse du routeur peer] route-map frompeer in
# // Route Map
route-map frompeer permit [numero de prio]
  set community 3
# // Ip community-list
ip community-list standard peer permit 3

