import json

with open("config.json", 'r') as fichier:
    # Charger le contenu JSON dans une variable Python (ici, un dictionnaire)
    config = json.load(fichier)


nombre_routers = 0
liste_AS = list(config.keys())
print(liste_AS)
nombre_AS = len(liste_AS)

for i in range(nombre_AS):
    nombre_routers += int(config[liste_AS[i]]["Nombre_routeur"])

for i in range(nombre_routers) :
    with open("R" + str(i+1) + "_configs_i" + str(i+1) + "_startup-config.cfg",'w') as fichier_cfg :
        fichier_cfg.writelines(['!\n','\n', '!\n', 'version 15.2\n', 'service timestamps debug datetime msec\n',
                                'service timestamps log datetime msec\n', '!\n'])
        
        fichier_cfg.writelines('hostname R' + str(i+1) + '\n')
        fichier_cfg.writelines([
                            "! \n",
                            "boot-start-marker\n",
                            "boot-end-marker\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "no aaa new-model\n",
                            "no ip icmp rate-limit unreachable\n",
                            "ip cef\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "no ip domain lookup\n",
                            "ipv6 unicast-routing\n",
                            "ipv6 cef\n",
                            "!\n",
                            "!\n",
                            "multilink bundle-name authenticated\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "ip tcp synwait-time 5\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n",
                            "!\n"
                        ])
        
