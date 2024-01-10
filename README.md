# Projet GNS3


# Generateur_json_config :
Automatisation de la generation du dictionnaire vide :
- Generateur du graphe d'adjacence (plutôt que de le faire soi-même) à partir de tableaux plus simples à comprendre (Ex : R1 = [R2,R3,R4]) /A FAIRE
- Generateur d'un graphe d'adressage vide /A FAIRE
- Generateur de la base de donnée des routeurs /A FAIRE
  Remarque :
  - Chaque routeur a un numero de routeur (unique seulement dans l'AS)
  - Chaque routeur a un nom généré automatiquement (Ex : AS2_R1 )
  - Chaque routeur a un dynamips ID unique généré automatiquement
  - Le dynamips ID est un identifiant cree par GNS3 en fonction de l'ordre dans lequel on a placé les routeurs. L'ordre standard est Num_AS croissant > Num_routeur croissant
Fonction :
- Adressage_AS(Nom_As , Matrice_adjacence , Nombre_routeur) --> None : Configure les adresses des liens d'une AS dans le fichier json /FAIT

# A definir : 
Routage inter AS :
- Mettre en forme le json BGP (quelles infos on met dedans...)
- Des parties à automatiser ?
- Definir les entrées à parametrer


# Generateur_fichier_cfg pour chacun des routeurs :
# / Création du cfg :
- Verifier le dynamips_ID /A FAIRE
- Creer/Remplacer les fichiers cfg "[Nom du routeur]_configs_i[Dynamips ID]_startup_config.cfg" dans le dossier "users/patri/GNS3/import/Config_reseau" /A MODIFIER
  Remarque :
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

# A definir : 
- Regarder comment sont fait les cfg pour savoir comment ce sera le plus pratique de faire les boucles

# Json 
- Rajouter les loopbacks dans le json pour simplifier le code ?

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
