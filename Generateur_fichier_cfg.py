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
liste_AS = [e for e in liste_AS if e != "Route_map"]
nombre_AS = len(liste_AS)

for i in range(nombre_AS):
    nombre_routers += int(config[liste_AS[i]]["Nombre_routeur"])


for i in range(nombre_AS) :
    nombre_routers_AS = config[liste_AS[i]]["Nombre_routeur"]
    liste_router = [config[liste_AS[i]]["Donnees_routeurs"][f"{j+1}"]["Dynamips_ID"] for j in range(nombre_routers_AS)]

    for j in range(config[liste_AS[i]]["Nombre_routeur"]) :
        num_router = config[liste_AS[i]]["Donnees_routeurs"][f"{j+1}"]["Dynamips_ID"]

        with open('fichiers_cfg/R' + str(config[liste_AS[i]]["Donnees_routeurs"][f"{j+1}"]["Dynamips_ID"]) + "_configs_i" + str(num_router) + "_startup-config.cfg",'w') as fichier_cfg :

            fichier_cfg.writelines(['!\n', 'hostname ' + config[liste_AS[i]]["Donnees_routeurs"][f"{j+1}"]["Nom"] + '\n', '!\n'])
            
            fichier_cfg.writelines(["ipv6 unicast-routing\n", '!\n'])

            ######### loopback ########

            fichier_cfg.writelines([
                    "interface Loopback0\n",
                    " no ip address\n",
                    " ipv6 address " + config[liste_AS[i]]["Maque_loopback"].split("::")[0] + "::" + str(num_router) + "/128\n"
                            ])
            if config[liste_AS[i]]["Routage_intraAS"]["Protocol"] == "OSPF" : # // Rajouter le protocol RIP aussi dans les loopback même si en soit c'est pas vraiment utile
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
                if config[liste_AS[i]]["Matrice_adjacence"][j][k] == 1 : # S'il y a un lien on crée une interface
                    fichier_cfg.writelines([
                        "interface " + config[liste_AS[i]]["Matrice_adressage_interface"][j][k][1] + "\n",
                        " no ip address\n",
                        " negotiation auto\n",
                        " ipv6 address " + config[liste_AS[i]]["Matrice_adressage_interface"][j][k][0] + "\n"
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

                    ######### interfaces entre les borders

            if str(j+1) in list(config[liste_AS[i]]["Routage_interAS"].keys()) : #si c'est un router de bordure
                for k in list(config[liste_AS[i]]["Routage_interAS"][str(j+1)].keys()) :
                    fichier_cfg.writelines([
                            "interface " + config[liste_AS[i]]["Routage_interAS"][str(j+1)][str(k)]["Interface"] + "\n",
                            " no ip address\n",
                            " negotiation auto\n",
                            " ipv6 address " + config[liste_AS[i]]["Routage_interAS"][str(j+1)][str(k)]["Adresse"] + "\n",
                            " ipv6 enable\n"
                        ])
                    if config[liste_AS[i]]["Routage_intraAS"]["Protocol"] == "OSPF" :
                        fichier_cfg.writelines([
                            " ipv6 ospf " + liste_AS[i] + " area " + liste_AS[i] + "\n",
                            "!\n",
                            "router ospf " + liste_AS[i] + "\n",
                            " passive-interface " + config[liste_AS[i]]["Routage_interAS"][str(j+1)][str(k)]["Interface"] + "\n"
                        ])
                    fichier_cfg.write("!\n")


            ######### routage bgp ########
            
            fichier_cfg.writelines([
                "router bgp " + "11" + liste_AS[i] + "\n",
                " bgp router-id " + 3*(str(num_router) + ".") + str(num_router) + "\n",
                " bgp log-neighbor-changes\n",
                " no bgp default ipv4-unicast\n",
            ])

            if str(j+1) in list(config[liste_AS[i]]["Routage_interAS"].keys()) : #si c'est un router de bordure
                for k in list(config[liste_AS[i]]["Routage_interAS"][str(j+1)].keys()) :
                    fichier_cfg.writelines([
                        " neighbor " + config[liste_AS[i]]["Routage_interAS"][str(j+1)][str(k)]["Adresse"].split("/")[0][:-1] + k + " remote-as " + "11" + k + "\n",
                        " neighbor " + config[liste_AS[i]]["Routage_interAS"][str(j+1)][str(k)]["Adresse"].split("/")[0][:-1] + k + " send-community\n"
                    ])

            for k in range(config[liste_AS[i]]["Nombre_routeur"] - 1) :
                fichier_cfg.writelines([
                    " neighbor 5000::" + str([e for e in liste_router if e != num_router][k]) + " remote-as " + "11" + liste_AS[i] + "\n",
                    " neighbor 5000::" + str([e for e in liste_router if e != num_router][k]) + " update-source Loopback0\n"
                ])

            fichier_cfg.write(" !\n")

                    ######### adresse-family ########

            fichier_cfg.write(" address-family ipv6\n")
            
            if str(j+1) in list(config[liste_AS[i]]["Routage_interAS"].keys()) : #il s'agit du router border
                liste_masque=[]
                for k in range(nombre_routers_AS) :
                    for l in range(nombre_routers_AS) :
                        if config[liste_AS[i]]["Matrice_adjacence"][k][l] == 1 and masque_reseau(config[liste_AS[i]]["Matrice_adressage_interface"][k][l][0]) not in liste_masque :
                            fichier_cfg.write("  network " + masque_reseau(config[liste_AS[i]]["Matrice_adressage_interface"][k][l][0]) + "\n")
                            liste_masque.append(masque_reseau(config[liste_AS[i]]["Matrice_adressage_interface"][k][l][0]))

                for k in list(config[liste_AS[i]]["Routage_interAS"][str(j+1)].keys()) :
                    fichier_cfg.writelines([
                        "  neighbor " + config[liste_AS[i]]["Routage_interAS"][str(j+1)][str(k)]["Adresse"].split("/")[0][:-1] + k + " activate\n",
                        "  neighbor " + config[liste_AS[i]]["Routage_interAS"][str(j+1)][str(k)]["Adresse"].split("/")[0][:-1] + k + " route-map from" + config[liste_AS[i]]["Type_AS"] + " in\n",
                        "  neighbor " + config[liste_AS[i]]["Routage_interAS"][str(j+1)][str(k)]["Adresse"].split("/")[0][:-1] + k + " route-map to" + config[liste_AS[i]]["Type_AS"] + " out\n"
                    ])

            for k in range(config[liste_AS[i]]["Nombre_routeur"] - 1) :
                fichier_cfg.write("  neighbor 5000::" + str([e for e in liste_router if e != num_router][k]) + " activate\n")

            fichier_cfg.writelines([" exit-address-family\n", "!\n"])

            if config[liste_AS[i]]["Routage_intraAS"]["Protocol"] == "OSPF" :
                fichier_cfg.writelines([
                    "ipv6 router ospf " + liste_AS[i] + "\n",
                    " router-id " + 3*(str(num_router) + ".") + str(num_router) + "\n",
                    "!\n"
                ])

            ######### communautées ########
            
            if config[liste_AS[i]]["Type_AS"] == "AS" :  #on ajoute les communautées pour tous les routers d'un AS avec un id que l'on peut voir dans le dico tags
                type_printed = []
                tags = {"Client" : 3, "Provider" : 2, "Peer" : 1}
                for k in range(nombre_AS) :
                    typ = config[liste_AS[k]]["Type_AS"]
                    if typ not in type_printed and typ != "AS" :
                        fichier_cfg.write("ip community-list standard " + typ + " permit " + str(tags[typ]) + "\n" )
                        type_printed.append(typ)
                fichier_cfg.write("!\n")


            ######### route-map ########
            
            if str(j+1) in list(config[liste_AS[i]]["Routage_interAS"].keys()) : #il s'agit du router border
                for k in list(config[liste_AS[i]]["Routage_interAS"][str(j+1)].keys()) :
                    if config[k]["Type_AS"] != "AS" :
                        fichier_cfg.writelines([
                            "route-map from" + config[k]["Type_AS"] + " permit " + str(20) + "\n",
                            " set community " + k + "\n",
                            "set local-preference " + 
                            "!\n"])
                        # route map to Type_AS permit
                            # Match_community 
            
            ######### Redistribute connected ########
            
            if config[liste_AS[i]]["Routage_intraAS"]["Protocol"] == "RIPng" : #si le protocole du router est RIP, on active le redistribute connected
                fichier_cfg.writelines([
                    "ipv6 router rip RIPng\n",
                    " redistribute connected\n",
                    "!\n"
                ])

            ######### end ########
                
            fichier_cfg.writelines([
                "end"
            ])