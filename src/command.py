# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
#from tools import error as error  
def error(msg): tools.error(msg)    



command_list = []
commands={}

help_message = """
# Aide

Cette aide présente les différentes commandes et sous commandes disponibles pour interagir avec l'assistant.

## Commandes

### $config
Affiche la configuration actuelle de l'assistant.

* $config write : sauvegarde la configuration actuelle.
* $config <clé> : affiche la valeur de la clé de configuration spécifiée.
* $config <clé> <valeur> : modifie la valeur de la clé de configuration spécifiée.

### $conversation
Sauvegarde ou charge une conversation.

* $conversation save <fichier> : sauvegarde la conversation dans un fichier.
* $conversation load <fichier> : charge une conversation à partir d'un fichier.

### $file
Gère la liste des fichiers.

* $file : affiche la liste des fichiers.
* $file add <fichier> : ajoute un fichier à la liste des fichiers.
* $file save : enregistre le programme/fichier actuel.
* $file save <fichier> : enregistre le programme/fichier spécifié.
* $file set <fichier> : fixe le fichier courant.
* $file open <fichier> : ouvre le fichier spécifié.
* $file close : ferme le fichier courant.
* $file close <fichier> : ferme le fichier spécifié.

### $git
Exécute une commande git.

* $git <commande> : exécute la commande git spécifiée.

### $help
Affiche cette aide.

### $history
Affiche l'historique des conversations avec l'assistant.

* $history purge : purge l'historique des conversations.

### $info
Affiche "ok".

### $keys
Affiche les clés.

* $keys : affiche les clés.
* $keys next : affiche les clés suivantes.

### $load
Ouvre un fichier (idem $open).

* $load <fichier> : ouvre le fichier spécifié.

### $model
Affiche les informations sur le modèle de langage utilisé par l'assistant.

* $model list : affiche la liste des modèles de langage disponibles.
* $model <nom_du_modèle> : sélectionne le modèle de langage spécifié.

### $open
Charge un fichier (idem $load).

* $open <fichier> : ouvre le fichier spécifié.

### $print
Affiche les lignes du programme sans les numéroter.

### $purge
Purge l'historique des conversations.

### $rc
Sauvegarde ou charge la configuration.

* $rc save : sauvegarde la configuration actuelle.
* $rc load : charge la configuration sauvegardée.

### $shell
Exécute une commande shell.

* $shell : lance un shell.
* $shell <commande> : exécute la commande shell spécifiée.

### $system
Exécute une commande système.

* $system <commande> : exécute la commande système spécifiée.

### $test
Exécute la commande spécifiée dans la variable d'environnement AI_TEST_COMMAND.

### $toggle
Active ou désactive le mode multi-lignes.

* $toggle : active ou désactive le mode multi-lignes.
* $toggle <clé> : active ou désactive la clé de configuration spécifiée.

### $undo
Récupère la sauvegarde du programme.

### $write
Enregistre le programme/fichier (une sauvegarde du programme/fichier est effectuée) et met à jour le contenu du programme avec la réponse de l'assistant.
* $write : enregistre le fichier courant
* $write <local_file> : enregistre le fichier spécifié.

### $exit
Quitte l'application.

### $quit
Quitte l'application.
"""

def complete_command(text, state):
    global help_message
    
    line = readline.get_line_buffer()
    words = line.split(" ")
    n=len(words)
    #print(words, n)
    if line[0] != "$" :
        return []

    if n == 1 :
        options = command_list
        matches = [option for option in options if option.startswith(text)]
        #print(type(matches[state])) 
        return matches[state]
        
    #print(f"n: {n} line: {line} text: {text}, state: {state}", file=sys.stderr)
    if n == 2 :
        regexp=r'\* *\$'+words[0][1:]+' ([^ :]+)'
        options= re.findall(regexp, help_message)
        if '<fichier>' in options :
            #options = glob.glob(words[1]+'*')
            options = [chemin + '/' if os.path.isdir(chemin) else chemin for chemin in glob.glob(words[1]+'*')]
        if '<local_file>' in options :
            #options = glob.glob(words[1]+'*')
            options = config.conf['files']
        matches = [option for option in options if option.startswith(text)]
        return matches[state]

    if n == 3 :
        regexp=r'\* *\$'+words[0][1:]+" "+words[1]+' ([^ :]+)'
        options= re.findall(regexp, help_message)
        if '<fichier>' in options :
            #options = glob.glob(words[1]+'*')
            options = [chemin + '/' if os.path.isdir(chemin) else chemin for chemin in glob.glob(words[2]+'*')]
        matches = [option for option in options if option.startswith(text)]
        return matches[state]
        
def initCommand() :
    global commands, command_list

       
    commands = {
        "help": command_help,
        "history": command_history,
        "close": command_close,
        "open": command_open,
        "set": command_set,
        "config": command_config,
        "model": command_model,
        "write": command_write,
        "undo": command_undo,
        "print": command_print,
        "test": command_test,
        "toggle": command_toggle,
        "rc": command_rc,
        "conversation": command_conversation,
        "file": command_file,
        "git": command_git,
        "system": command_system,
        "ls": command_ls,
        "shell": command_shell,
        "keys": command_keys,
        "exit": command_exit,
        "quit": command_exit,
        "purge": command_purge,
        "load": command_open,
        "info": command_info,
    }
    
    #command_list = list(commands.keys())
    command_list = ['$' + key for key in commands.keys()]

def get_command(user_input):
    global commands
    
    possible_commands = []
    first_word = user_input.split()[0]
    for command in commands:
        if command.startswith(first_word):
            possible_commands.append(command)
            
    if len(possible_commands) == 1:
        return commands[possible_commands[0]] # {user_input.split()[1:]}" 
    elif len(possible_commands) > 1:
        error("Conflit de commande : plusieurs commandes possibles")
        for command in possible_commands:
            print(command)
        return None
    else:
        error(f"Erreur : commande '{first_word}' inconnue")
        return None

def command_keys(user_input) :
    return keys.command_keys(user_input)

def command_help(user_input):
    global help_message
    
    lexer = MarkdownLexer() #stripnl=False)
    #lexer = mistletoe.lexer.MarkdownLexer()
    
    if config.conf['background'] == "dark" :
        formatter = Terminal256Formatter(fg='dark', bg='light', style=config.conf['colors_style'])
    else :
        formatter = Terminal256Formatter(fg='light', bg='dark', style=config.conf['colors_style'])

    highlighted_code = pygments.highlight(help_message, lexer, formatter)

    print(highlighted_code)
    #print(help_message)
    return ""

def alias_helper(user_input, command, str) :
    if len(user_input.split()) > 1 and user_input.split()[1] == "help" :
        print(f"{user_input.split()[0]} est un alias vers {str}") 
        str=str.split()[0]+ " help"
        user_input="none"
    return command(str+" "+" ".join(user_input.split()[1:]))
    
def purge_filename(filename):
    # Code pour purger l'historique du chat en fonction du fichier spécifié
    config.chat_history = [msg for msg in config.chat_history if filename not in msg['content']]
    #command_conversation("$conversation save")
    save_conversation()

def command_history(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $history :
  $history : affiche l'historique des conversations
  $history purge : purge l'historique des conversations
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    if len(args) == 1:
        #global chat_history

        dumps=json.dumps(config.chat_history, indent=4, ensure_ascii=False)        
        config.printChatHistory()
        #print(dumps)
        #pprint(config.chat_history)
        #print(dumps.encode('utf-8').decode('unicode_escape'))
        #with open("last_response.txt", "w") as f:
        #    f.write(dumps)

    elif len(args) == 2 and args[1] == "purge":
        if len(args) == 3:
            purge_filename(args[2])
        else:
            config.chat_history = []
            config.conf['current_filename']=""
            config.conf['files']=[]
            #tools.readline_purge_history()
            save_conversation()            
            print("Historique du chat purgé")
    else:
        error("Erreur : commande $history inconnue")
        print(help_message)
    return ""

def command_config(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $config :
  $config : affiche la configuration actuelle
  $config write : sauvegarde la configuration actuelle
  $config <clé> : affiche la valeur de la clé de configuration spécifiée
  $config <clé> <valeur> : modifie la valeur de la clé de configuration spécifiée
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    if len(args) == 1:
        # Si aucun argument n'est fourni, affiche la configuration actuelle
        print(json.dumps(config.conf, indent=4, ensure_ascii=False))
        print("")
        #print("Last chunk:")
        #print(config.last_chunk);
        #for key, value in config.conf.items():
        #    if key != "system":
        #        print(f"{key} {value}")
    elif len(args) == 2:
        if args[1] == "write":
            # Si l'argument est "write", sauvegarde la configuration
            config.conf.saveRc()
        else:
            # Si l'argument est une clé de configuration, affiche la valeur de la clé de configuration spécifiée
            key = args[1]
            if key in config.conf:
                print(f"Valeur de la clé '{key}' : {config.conf[key]}")
            else:
                error(f"Erreur : clé '{key}' non trouvée dans la configuration")
    elif len(args) == 3:
        # Si 2 arguments sont fournis, configure la variable de configuration
        key = args[1]
        value = args[2]
        config.conf[key] = value
    else:
        error("Erreur : commande $config inconnue")
        print(help_message)
    return ""

def command_model(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $model :
  $model : affiche le modèle de langage actuel
  $model list : affiche la liste des modèles de langage disponibles
  $model <nom du modèle> : sélectionne le modèle de langage spécifié
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    if len(args) == 1:
        print(config.conf["model"])
    elif len(args) == 2:
        if args[1] == "list":
            llm.provider.list()
        else:
            pass
            #print("model: ",arg)
            #conf["model"]
            config.conf["model"]=args[1]

    return ""
    
def command_undo(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $undo :
  $undo : récupère la sauvegarde du programme
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    # Récupère la sauvegarde du programme
    backup_filename = os.environ.get("PROG_NAME") + ".keep"
    if backup_filename == "" :
        error("Pas de fichier backup définit !")
        return

    try:
        with open(backup_filename, 'r') as f:
            backup_content = f.read()
        with open(os.environ.get("PROG_NAME"), 'w') as f:
            f.write(backup_content)
            content = backup_content
            content = content.join(chr(10), chr(10))
            content = content.replace('"', chr(92)+chr(34))

            print(f"Backup restored: {backup_filename}")
            return "Le contenu du programme est maintenant : "+content
    except FileNotFoundError:
        error(f"No backup found: {backup_filename}")
    return ""

def command_print(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $print :
  $print : affiche les lignes du programme sans les numéroter
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    return f"Affiche les lignes du programmme/document {config.conf['current_filename']} entre 2 lignes '```' sans les numéroter. Affiche ensuite sur une nouvelle ligne : [[[{config.conf['current_filename']}]]]"

def command_test(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $test :
  $test : exécute la commande spécifiée dans la variable d'environnement AI_TEST_COMMAND
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    # Execute the command in the AI_TEST_COMMAND environment variable
    command = os.environ.get("AI_TEST_COMMAND")
    if command:
        print(f"Executing command: {command}")
        subprocess.run(command, shell=True)
    else:
        error("No command to execute.")
    return ""

def command_rc(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $rc :
  $rc : affiche la configuration actuelle
  $rc save : sauvegarde la configuration actuelle
  $rc load : charge la configuration sauvegardée
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    if len(args) == 1:
        config.printRc()
    elif len(args) == 2:
        if args[1] == "save":
            config.saveRc()
        elif args[1] == "load":
            config.loadRc()
    else:
        error("Erreur : commande $rc inconnue")
        print(help_message)
    return ""
    
def command_close(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $close :
  $close : ferme le fichier courant
  $close <fichier> : ferme le fichier spécifié
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    if len(args) == 2:
        filename = args[1]
        tools.closeFile(filename)
    else:
        tools.closeFile(config.conf['current_filename'])
    return ""

def command_write(user_input):
    return alias_helper(user_input, command_file, "file save")
    #return command_file("file save " + " ".join(user_input.split()[1:]))
    
def command_open(user_input):
    return alias_helper(user_input, command_file, "file open")
    

def command_set(user_input):
    return alias_helper(user_input, command_file, "file set")
    #return command_file("file set " + " ".join(user_input.split()[1:]))

def command_ls(user_input):
    return alias_helper(user_input, command_file, "file list")
    #return command_file("file list" + " ".join(user_input.split()[1:]))

def command_file(user_input):
    #print("COMMAND_FILE : {user_input}")
    args = user_input.split()
    help_message = """
Aide sur la commande $file :
  $file : affiche la liste des fichiers
  $file add <fichier> : ajoute un fichier à la liste des fichiers
  $file save : enregistre le programme/fichier actuel
  $file save <fichier> : enregistre le programme/fichier spécifié
  $file save <source> <destination> : copie le fichier source vers le chemin de destination
  $file set <fichier> : fixe le fichier courant
  $file open <fichier> : ouvre le fichier spécifié
  $file close : ferme le fichier courant
  $file close <fichier> : ferme le fichier spécifié
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    if len(args) == 2 and args[1] == "list":
        print(json.dumps(config.conf['files'], indent=4, ensure_ascii=False))
    elif len(args) == 3 and args[1] == "add":
        if args[2] not in config.conf['files']:
            config.conf['files'].append(args[2])
            print(f"Fichier {args[2]} ajouté à la liste des fichiers")
        else:
            error(f"Fichier {args[2]} déjà présent dans la liste des fichiers")
    elif len(args) == 2 and args[1] == "save":
        filename=config.conf['current_filename']
        tools.saveFile(filename)
    elif len(args) == 3 and args[1] == "save":
        filename = os.path.expanduser(args[2])
        tools.saveFile(filename, filename)
    elif len(args) == 4 and args[1] == "save":
        source = args[2]
        destination = os.path.expanduser(args[3])
        #if source in config.conf['files']:
        #    with open(source, 'rb') as f:
        #        file_content = f.read()
        command_file("$file set source")
        tools.saveFile(source, destination)
        #try :
        #    with open(destination, 'wb') as f:
        #        commande_file("$file set
        #        f.write(file_content)
                
        print(f"Fichier {source} copié vers {destination}")
        #else:
        #    error(f"Erreur : fichier {source} non trouvé")
    elif len(args) == 3 and args[1] == "set":
        filename = os.path.expanduser(args[2])
        config.conf['current_filename'] = filename
        print(f"Nom du fichier courant fixé à {filename}")
    elif len(args) == 3 and args[1] == "open":
        filename = os.path.expanduser(args[2])
        tools.loadFile(filename)
    elif len(args) >= 2 and args[1] == "close":
        if len(args) == 3 and args[2] == "*":
            for filename in config.conf['files']:
                tools.closeFile(filename)
            config.conf['files'] = []
            config.conf['current_filename'] = ""
            print("Tous les fichiers fermés")
        else:
            filename = config.conf['current_filename'] if len(args) == 2 else os.path.expanduser(args[2])
            if filename == "":
                error("Erreur : aucun fichier courant défini")
            else:
                tools.closeFile(filename)
    elif len(args) >= 2 and args[1] == "cd":
        directory = os.path.expanduser(" ".join(args[2:]))
        os.chdir(directory)
        print(f"Répertoire courant changé en {directory}")            
    elif len(args) > 1:
        error(f"Erreur : sous commande '{args[1]}' inconnue pour la commande $file")
    else:
        error("Erreur : mauvais nombre d'arguments pour la commande $file")
        print(help_message)
    return ""

def command_git(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $git :
  $git <commande> : exécute la commande git spécifiée
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    if len(args) < 2:
        error("Erreur : mauvais nombre d'arguments pour la commande $git")
        print(help_message)
        return ""

    command = "git " + " ".join(args[1:])
    print(f"Executing command: {command}")
    subprocess.run(command, shell=True)
    return ""

def command_toggle(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $toggle :
  $toggle : active ou désactive le mode multi-lignes
  $toggle <clé> : active ou désactive la clé de configuration spécifiée
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    if len(args) == 2:
        key = args[1]
        if key == "extend":
            config.conf[key] = not config.conf[key]
            extend.initSystem()
        elif key in config.conf and isinstance(config.conf[key], bool):
            config.conf[key] = not config.conf[key]
            print(f"Valeur de la clé '{key}' inversée : {config.conf[key]}")
        else:
            error(f"Erreur : clé '{key}' non trouvée dans la configuration ou non booléenne")
    elif len(args) == 1:
        if config.conf["multi_lines"]:
            config.conf["multi_lines"] = False
            print("Mode mono-ligne activé")
        else:
            config.conf["multi_lines"] = True
            print("Mode multi-lignes activé")
    else:
        error("Erreur : mauvais nombre d'arguments pour la commande $toggle")
        print(help_message)
    return ""

def load_conversation(file) :
    try:
        with open(os.path.expanduser(file), 'r') as f:
            conv = json.load(f)
            tools.readline_set_history(conv['readline'])
            config.conf.update(conv["config"])
            config.chat_history = conv["chat_history"]
            print(f"Conversation chargée depuis {file}")
            config.conf['conversation']=file
    except FileNotFoundError:
        # Créer un fichier de conversation valide si celui-ci n'existe pas
        conv = {"readline": [], "config": config.conf, "chat_history": config.chat_history}
        with open(os.path.expanduser(file), 'w') as f:
            json.dump(conv, f, indent=4, ensure_ascii=False)
        print(f"Fichier de conversation créé : {file}")
        config.conf['conversation']=file
    except json.JSONDecodeError:
        error(f"Fichier {file} non valide")

def save_conversation(file=""):
    if file=="" :
        file=config.conf['conversation']

    readlineHistory=tools.readline_get_history()
    n=50
    if len(readlineHistory) > n :
        readlineHistory = readlineHistory[-n:]
    conv = {"readline": readlineHistory, "config": config.conf, "chat_history": config.chat_history}
    with open(os.path.expanduser(file), 'w') as f:
        json.dump(conv, f, indent=4, ensure_ascii=False)    
    config.conf['conversation'] = file

def command_conversation(user_input):
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
        load_conversation(os.path.expanduser(args[2]))
    else:
        error("Erreur : commande $conversation inconnue")
        print(help_message)
    return ""

def common_prefix(s1, s2):
    return ''.join(c[0] for c in zip(s1, s2) if c[0] == c[1])

def ai_extend_request(user_input, client, chat_history):
    if user_input.startswith("$"):
        command = get_command(user_input[1:])
        if command:
            #print(command)
            #print(user_input)
            return command(user_input)
        else:
            return ""
    else:
        return user_input

def command_shell(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $shell :
  $shell : lance un shell
  $shell <commande> : exécute la commande shell spécifiée
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    if len(args) == 1:
        # Lance un shell
        subprocess.run(["/bin/bash"], shell=True)
    elif len(args) > 1:
        # Exécute la commande passée en argument dans un shell
        command = f"bash -c \"{' '.join(args[1:])}\""
        subprocess.run(command, shell=True)
    else:
        error("Erreur : mauvais nombre d'arguments pour la commande $shell")
        print(help_message)
    return ""
    
def command_exit(user_input):
    exit(0)

def command_quit(user_input):
    return command_file("exit " + " ".join(user_input.split()[1:]))

def command_purge(user_input):
    return alias_helper(user_input, command_history, "history purge")
    #return command_history("history purge " + " ".join(user_input.split()[1:]))

def command_load(user_input):
    return alias_helper(user_input, command_file, "file open")

    
def command_git(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $git :
  $git <commande> : exécute la commande git spécifiée
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    if len(args) < 2:
        error("Erreur : mauvais nombre d'arguments pour la commande $git")
        print(help_message)
        return ""

    command = "git " + " ".join(args[1:])
    print(f"Executing command: {command}")
    subprocess.run(command, shell=True)
    return ""

def command_system(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $system :
  $system <commande> : exécute la commande système spécifiée
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""
    if len(args) < 2:
        error("Erreur : mauvais nombre d'arguments pour la commande $system")
        print(help_message)
        return ""

    command = " ".join(args[1:])
    

    print(f"Executing command: {command}")
    return f"Exécute la commande : '{command}'"

def command_info(user_input):
    args = user_input.split()
    help_message = """
Aide sur la commande $info :
  $info : affiche "ok"
"""
    if len(args) == 2 and args[1] in ["help", "h"]:
        print(help_message)
        return ""

    print("Last chunk:")
    print(config.last_chunk)
    print()
    print("Last response :")
    print(config.last_response)
    
    return ""
