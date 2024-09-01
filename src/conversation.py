# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
#from tools import error as error  
def error(msg): tools.error(msg)

def makedir():
    global conversations_dir
    if not os.path.exists(conversations_dir):
        os.makedirs(conversations_dir)
        print(f"Répertoire {conversations_dir} créé")

def load_conversation(file) :
    makedir()
    try:    
        with open(os.path.join(conversations_dir, file), 'r') as f:
            conv = json.load(f)
            tools.readline_set_history(conv['readline'])
            config.conf.update(conv["config"])
            config.chat_history = conv["chat_history"]
            print(f"Conversation chargée depuis {file}")
            config.conf['conversation']=file
    except FileNotFoundError:
        # Créer un fichier de conversation valide si celui-ci n'existe pas
        conv = {"readline": [], "config": config.conf, "chat_history": config.chat_history}
        with open(os.path.join(conversations_dir, file), 'w') as f:
            json.dump(conv, f, indent=4, ensure_ascii=False)
        print(f"Fichier de conversation créé : {file}")
        config.conf['conversation']=file
    except json.JSONDecodeError:
        error(f"Fichier {file} non valide")

def save_conversation(file=""):
    makedir()
    if file=="" :
        file=config.conf['conversation']

    readlineHistory=tools.readline_get_history()
    n=50
    if len(readlineHistory) > n :
        readlineHistory = readlineHistory[-n:]
    conv = {"readline": readlineHistory, "config": config.conf, "chat_history": config.chat_history}
    with open(os.path.join(conversations_dir, file), 'w') as f:
        json.dump(conv, f, indent=4, ensure_ascii=False)
    config.conf['conversation'] = file

def command_conversation(user_input):
    makedir()
    args = user_input.split()
    help_message = """
Aide sur la commande $conversation :
  $conversation save <fichier> : sauvegarde la conversation dans un fichier
  $conversation load <fichier> : charge une conversation à partir d'un fichier
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    if len(args) >= 2 and args[1] == "save":
        # Sauvegarde la conversation
        filename = args[2] if len(args) == 3 else config.conf.get('conversation')
        if filename is None:
            error("Erreur : fichier de conversation non défini")
            print(help_message)
            return
        save_conversation(filename)
        print(f"Conversation sauvegardée dans {filename}")
    elif len(args) == 3 and args[1] == "load":
        # Charge la conversation
        load_conversation(args[2])
    elif len(args) == 2 and args[1] == "ls":
        # Liste toutes les conversations
        conversations = [f for f in os.listdir(conversations_dir) if os.path.isfile(os.path.join(conversations_dir, f))]
        if conversations:
            print("Conversations sauvegardées :")
            for conversation in conversations:
                print(conversation)
        else:
            print("Aucune conversation sauvegardée")
    elif len(args) == 3 and args[1] == "rm":
        # Supprime une conversation
        filename = args[2]
        if os.path.isfile(os.path.join(conversations_dir, filename)):
            os.remove(os.path.join(conversations_dir, filename))
            print(f"Conversation {filename} supprimée")
        else:
            error(f"Erreur : conversation {filename} non trouvée")

    else:
        error("Erreur : commande $conversation inconnue")
        print(help_message)
    return ""

conversations_dir = os.path.expanduser('~/.ai/conversations')
