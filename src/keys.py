# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
#from tools import error as error  
def error(msg): tools.error(msg)

keysConf = {
    "keys": [],
    "key": 0
}
def command_keys(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $keys :
  $keys : affiche les clés
  $keys next : affiche les clés suivantes
  $keys num : sélectionne la clé à l'indice num
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    if len(args) == 1:
        keys.printKeys()
    elif len(args) == 2 and args[1] == "next":
        keys.nextKeys()
    elif len(args) == 2 and args[1].isdigit():
        setKey(int(args[1]))
    else:
        error("Erreur : commande $keys inconnue")
        print(help_message)
    return ""


    
def loadKeys():
    global keysConf

    if config.conf['provider'].startswith("ollama") :
        return
        
    #print("Load keys...")
    try:
        filename = f"~/.ai/keys-{config.conf['provider']}"
        filename=os.path.expanduser(filename)
        if os.path.exists(filename):
            if os.stat(filename).st_mode & stat.S_IRUSR != stat.S_IRUSR:
                print("Erreur : fichier de configuration non lisible")
                return
            if os.stat(filename).st_mode & stat.S_IWUSR != stat.S_IWUSR:
                print("Erreur : fichier de configuration non modifiable (chmod)")
                return
        with open(filename, 'r') as f:
            keysConf = json.load(f)
    except FileNotFoundError:
        print("Warning : fichier de configuration des clés non trouvé")

        if config.conf['provider'] == "groq" :
            key=os.getenv('GROQ_API_KEY')
            if key != "" :
                addKeys(key)
            else :
                error("GROQ_API_KEY empty !")
            
    except json.JSONDecodeError:
        print("Erreur : fichier de configuration mal formé")

"""
saveKeys sauvegarde la variable globale keysConf dans le fichier de configuration
via une mise en forme par : json.dumps(keys, indent=4, ensure_ascii=False)
"""
def saveKeys():
    global keysConf
    try:
        filename = f"~/.ai/keys-{config.conf['provider']}"
        filename=os.path.expanduser(filename)
        with open(filename, 'w') as f:
            json.dump(keysConf, f, indent=4, ensure_ascii=False)
        os.chmod(filename, stat.S_IRUSR | stat.S_IWUSR)
    except Exception as e:
        print(f"Erreur : {e}")

"""
printKeys affiche la variable globale keysConf via une mise en forme par :
json.dumps(keys, indent=4, ensure_ascii=False)
"""
def printKeys():
    global keysConf
    try:
        print(json.dumps(keysConf, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Erreur : {e}")

"""
setKeys fixe key de keysConf à l'indice passé en paramètre num. Si num est un indice non valide
car en dehors de la liste keys alors un message d'erreur est affiché
"""
def setKey(num):
    global keysConf
    try:
        if num < len(keysConf["keys"]):
            keysConf["key"] = num
        else:
            error("Erreur : indice invalide")
    except Exception as e:
        error(f"Erreur : {e}")

"""
Ajoutes une clé à la liste des clés keys 
"""
def addKeys(key):
    global keysConf
    #key = input("Entrez la nouvelle clé : ")
    keysConf["keys"].append(key)
    #saveKeys()

"""
delKeys supprime la clé à l'indice num de keys 
"""
def delKeys(num):
    global keysConf
    try:
        if num < len(keysConf["keys"]):
            del keysConf["keys"][num]
            saveKeys()
        else:
            print("Erreur : indice invalide")
    except Exception as e:
        print(f"Erreur : {e}")

"""
Si llm.provider est de type GroqProvider alors
getKeys retourne la clé de keys à l'indice key si elle existe sinon :
si retourne la valeur de la variable dans  
"""
def getKey():
    global keysConf
    print("keys.getKey()")
    try:
        if "key" in keysConf and keysConf["key"] < len(keysConf["keys"]):
            print(f"ret : {keysConf['keys'][keysConf['key']]}")
            return keysConf['keys'][keysConf['key']]
        else:
            print(f"ret : None")
            return None
    except Exception as e:
        print(f"Erreur : {e}")

"""
nextKeys sélectionne la clé suivante de keys en rebouclant 
"""
def nextKeys():
    global keysConf
    try:
        old=keysConf["key"]
        if "key" in keysConf and keysConf["key"] < len(keysConf["keys"]):
            keysConf["key"] = (keysConf["key"] + 1) % len(keysConf["keys"])

            if keysConf["key"] != old :
                #print(f"new key in use: {keysConf['key']}")
                saveKeys()
               #printKeys()
                llm.provider.setKey(keysConf["keys"][keysConf["key"]])
                print(f"new key in use: {keysConf['key']}")
                llm.provider.initClient()
                
        else:
            print("Erreur : indice invalide")
    except Exception as e:
        print(f"Erreur : {e}")

