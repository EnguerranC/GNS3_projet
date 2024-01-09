import json

with open("config.json", 'r') as fichier:
    # Charger le contenu JSON dans une variable Python (ici, un dictionnaire)
    config = json.load(fichier)


nombre_routers = 0
num_router=1
liste_AS = list(config.keys())
print(liste_AS)
nombre_AS = len(liste_AS)

for i in range(nombre_AS):
    nombre_routers += int(config[liste_AS[i]]["Nombre_routeur"])


for i in range(nombre_AS) :
    for j in range(config[liste_AS[i]]["Nombre_routeur"]) :

        with open("R" + str(num_router) + "_configs_i" + str(num_router) + "_startup-config.cfg",'w') as fichier_cfg :

            fichier_cfg.writelines(['!\n', 'hostname R' + str(num_router) + '\n', '!\n'])
            
            ######### loopback ########

            fichier_cfg.writelines([
                    "interface Loopback0\n",
                    " no ip address\n",
                    " ipv6 address 5000::" + str(num_router) + "/128\n"
                            ])
            if config[liste_AS[i]]["Protocole"] == "RIPng" : 
                fichier_cfg.writelines([
                    " ipv6 enable\n", 
                    " ipv6 ospf " + liste_AS[i] + " area " + liste_AS[i] + "\n"
                ])
            fichier_cfg.write('!\n')

            ######### interfaces ########

            
            

            num_router += 1

