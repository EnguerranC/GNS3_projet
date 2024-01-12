import json

with open("config.json", 'r') as fichier:
    # Charger le contenu JSON dans une variable Python (ici, un dictionnaire)
    config = json.load(fichier)

def masque_reseau(adresse) :
    masque = int(adresse.split('/')[1])
    masque_res = ""
    liste_adresse = adresse.split(':')
    for i in range(int(masque/16)) :
        masque_res +=liste_adresse[i] + ':'
    return masque_res + f':/{masque}'

nombre_routers = 0
liste_AS = list(config.keys())
nombre_AS = len(liste_AS)

for i in range(nombre_AS):
    nombre_routers += int(config[liste_AS[i]]["Nombre_routeur"])


for i in range(nombre_AS) :
    nombre_routers_AS = config[liste_AS[i]]["Nombre_routeur"]
    liste_router = [config[liste_AS[i]]["Donnees_routeurs"][f"{j+1}"]["Dynamips_ID"] for j in range(nombre_routers_AS)]

    for j in range(config[liste_AS[i]]["Nombre_routeur"]) :
        num_router = config[liste_AS[i]]["Donnees_routeurs"][f"{j+1}"]["Dynamips_ID"]

        with open("R" + str(num_router) + "_configs_i" + str(num_router) + "_startup-config.cfg",'w') as fichier_cfg :

            fichier_cfg.writelines(['!\n', 'hostname ' + config[liste_AS[i]]["Donnees_routeurs"][f"{j+1}"]["Nom"] + '\n', '!\n'])
            
            fichier_cfg.writelines(["ipv6 unicast-routing\n", '!\n'])

            ######### loopback ########

            fichier_cfg.writelines([
                    "interface Loopback0\n",
                    " no ip address\n",
                    " ipv6 address 5000::" + str(num_router) + "/128\n"
                            ])
            if config[liste_AS[i]]["Routage_intraAS"]["Protocol"] == "OSPF" : 
                fichier_cfg.writelines([
                    " ipv6 enable\n", 
                    " ipv6 ospf " + liste_AS[i] + " area " + liste_AS[i] + "\n"
                ])
            elif config[liste_AS[i]]["Routage_intraAS"]["Protocol"] == "RIPng" :
                fichier_cfg.write(" ipv6 rip RIPng enable\n")
            fichier_cfg.write('!\n')

            ######### interfaces ########

            num=1
            for k in range(config[liste_AS[i]]["Nombre_routeur"]) :
                if config[liste_AS[i]]["Matrice_adjacence"][j][k] == 1 : #s'il y a un lien on crée une interface
                    fichier_cfg.writelines([
                        "interface GigabitEthernet" + str(num) + "/0\n",
                        " no ip address\n"
                        " negotiation auto\n",
                        " ipv6 address " + config[liste_AS[i]]["Matrice_adressage"][j][k] + "\n",
                    ])
                    if config[liste_AS[i]]["Routage_intraAS"]["Protocol"] == "RIPng" :
                        fichier_cfg.writelines([
                            " ipv6 enable\n",
                            " ipv6 rip RIPng enable\n"
                        ])
                    elif config[liste_AS[i]]["Routage_intraAS"]["Protocol"] == "OSPF" :
                        fichier_cfg.writelines([
                            " ipv6 enable\n",
                            " ipv6 ospf " + liste_AS[i] + " area " + liste_AS[i] + "\n"
                        ])
                    fichier_cfg.write("!\n")
                    num+=1

            ######### routage bgp ########
            
            fichier_cfg.writelines([
                "router bgp " + liste_AS[i] + "\n",
                " bgp router-id " + 3*(str(num_router) + ".") + str(num_router) + "\n",
                " bgp log-neighbor-changes\n",
                " no bgp default ipv4-unicast\n",
            ])

            #si cest un router de bordure, il faut rajouter une route bgp ici

            for k in range(config[liste_AS[i]]["Nombre_routeur"] - 1) :
                fichier_cfg.writelines([
                    " neighbor 5000::" + str([e for e in liste_router if e != num_router][k]) + " remote-as " + liste_AS[i]
                                              + "\n",
                    " neighbor 5000::" + str([e for e in liste_router if e != num_router][k]) + " update-source Loopback0\n"
                ])

            fichier_cfg.write(" !\n")

            fichier_cfg.write(" address-family ipv6\n")
            if config[liste_AS[i]]["Routage_interAS"]["Num_routeur_bordeur"] != j :
                for k in range(nombre_routers_AS) :
                    if config[liste_AS[i]]["Matrice_adjacence"][j][k] == 1 and config[liste_AS[i]]["Routage_interAS"]["Num_routeur_bordeur"] != k+1 :  #on recupere le masque reseau
                        fichier_cfg.write("  network " + masque_reseau(config[liste_AS[i]]["Matrice_adressage"][j][k]) + "\n")
            else : #il s'agit du router border
                liste_masque=[]
                for k in range(nombre_routers_AS) :
                    for l in range(nombre_routers_AS) :
                        if config[liste_AS[i]]["Matrice_adjacence"][k][l] == 1 and masque_reseau(config[liste_AS[i]]["Matrice_adressage"][k][l]) not in liste_masque :
                            fichier_cfg.write("  network " + masque_reseau(config[liste_AS[i]]["Matrice_adressage"][k][l]) + "\n")
                            liste_masque.append(masque_reseau(config[liste_AS[i]]["Matrice_adressage"][k][l]))



            
            ######### end ########
                
            fichier_cfg.writelines([
                "!\n",
                "end"
            ])