import config
from config import error as error
import llm
import tools
import json
import subprocess

def command_help(user_input):
    help_message = """
# Aide

Cette aide présente les différentes commandes disponibles pour interagir avec l'assistant.

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

### $help
Affiche cette aide.

### $history
Affiche l'historique des conversations avec l'assistant.

* $history purge : purge l'historique des conversations.

### $model
Affiche les informations sur le modèle de langage utilisé par l'assistant.

* $model list : affiche la liste des modèles de langage disponibles.
* $model <nom du modèle> : sélectionne le modèle de langage spécifié.

### $print
Affiche les lignes du programme sans les numéroter.

### $rc
Sauvegarde ou charge la configuration.

* $rc save : sauvegarde la configuration actuelle.
* $rc load : charge la configuration sauvegardée.

### $test
Exécute la commande spécifiée dans la variable d'environnement AI_TEST_COMMAND.

### $toggle
Active ou désactive le mode multi-lignes.

### $undo
Récupère la sauvegarde du programme.

### $write
Enregistre le programme/fichier (une sauvegarde du programme/fichier est effectuée) et met à jour le contenu du programme avec la réponse de l'assistant.

### $extend
Affiche les lignes du programme extend.py sans les numéroter.

### $enregistre_fichier
Enregistre le fichier spécifié.

"""
    print(help_message)
    return ""

def command_history(user_input):
    args = user_input.split()
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
        config.chat_history = []
        print("Historique du chat purgé")
    else:
        error("Erreur : mauvais nombre d'arguments pour la commande $history")
    return ""

def command_config(user_input):
    args = user_input.split()
    if len(args) == 1:
        # Si aucun argument n'est fourni, affiche la configuration actuelle
        print(json.dumps(config.conf, indent=4, ensure_ascii=False))
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
        error("Erreur : mauvais nombre d'arguments pour la commande $config")
    return ""

def command_model(user_input):
    args = user_input.split()
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


def ia_set_current_file(filename) :
    response = llm.ai_user_request(\
        f"N'affiche rien pour cette requête. Apprend juste que le fichier courant est maintenant {filename}."
    )
    
    if response is None:
        error("Erreur lors de la génération de la réponse")
        return ""

    print(response.choices[0].message.content)
    

def command_write(user_input):
    args = user_input.split()

    if len(args) == 1 :
        filename=config.conf['current_filename']
    elif len(args) == 2 :
        filename=args[1]
        config.conf['current_filename']
        ia_set_current_file(filename)
        
    else :
        error("Erreur : mauvais nombre d'arguments pour la commande $write")
        return ""

            
    config.conf["current_filename"]=filename
    print(f"config['current_filename']: {config.conf['current_filename']}")

    response = llm.ai_user_request(f"Affiche entre 2 lignes contenant '```' les lignes de {filename} que tu as mémorisé sans les numéroter. Si la dernière ligne ne possède pas de retour à la ligne, ajoute le. Tu termineras ta réponse par une ligne contenant [[[{filename}]]]")
    if response is None:
        error("Erreur lors de la génération de la réponse")
        return ""

    print(response.choices[0].message.content)
    
    code=tools.extract_code(response.choices[0].message.content)

    if code == "" :
        error("Pas de code !")
        return ""

    # Crée le fichier s'il n'existe pas
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        with open(filename, 'w') as f:
            pass
        print(f"Fichier {filename} créé")

    # Enregistre le programme/fichier (une sauvegarde du programme/fichier est effectuée)
    backup_filename = filename + ".keep"
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except Exception as e:
        error(f"Erreur lors de la lecture du fichier {filename} : {str(e)}")
        return ""

    try:
        with open(backup_filename, 'w') as f:
            f.write(content)
    except Exception as e:
        error(f"Erreur lors de la création de la sauvegarde {backup_filename} : {str(e)}")
        return ""

    print(f"Backup created: {backup_filename}")

    # Modifie le fichier associé au programme
    try:
        with open(filename, 'w')  as f:
            print(response.choices[0].message.content)
            f.write(code)
    except Exception as e:
        error(f"Erreur lors de l'écriture dans le fichier {filename} : {str(e)}")
        return ""

    print(f"Fichier {filename} mis à jour avec le contenu du programme.")
    return ""

def command_undo(user_input):
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

    return f"Affiche les lignes du programmme/document {config.conf['current_filename']} entre 2 lignes '```' sans les numéroter. Affiche ensuite sur une nouvelle ligne : [[[{config.conf['current_filename']}]]]"

def command_test(user_input):
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
    if len(args) == 2:
        if args[1] == "save":
            config.saveRc()
        elif args[1] == "load":
            config.loadRc()
    return ""

def command_file(user_input):
    args = user_input.split()
    if len(args) == 1:
        print(json.dumps(config.conf['files'], indent=4, ensure_ascii=False))
    elif len(args) == 3 and args[1] == "add":
        if args[2] not in config.conf['files']:
            config.conf['files'].append(args[2])
            print(f"Fichier {args[2]} ajouté à la liste des fichiers")
        else:
            error(f"Fichier {args[2]} déjà présent dans la liste des fichiers")
    elif len(args) == 2 and args[1] == "save":
        filename=config.conf['current_filename']
        config.conf["current_filename"]=filename
        print(f"config['current_filename']: {config.conf['current_filename']}")

        response = llm.ai_user_request(f"Affiche entre 2 lignes contenant '```' les lignes de {filename} que tu as mémorisé sans les numéroter. Si la dernière ligne ne possède pas de retour à la ligne, ajoute le. Tu termineras ta réponse par une ligne contenant [[[{filename}]]]")
        if response is None:
            error("Erreur lors de la génération de la réponse")
            return ""

        code=tools.extract_code(response.choices[0].message.content)

        if code == "" :
            error("Pas de code !")
            return ""

        # Crée le fichier s'il n'existe pas
        try:
            with open(filename, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            with open(filename, 'w') as f:
                pass
            print(f"Fichier {filename} créé")

        # Enregistre le programme/fichier (une sauvegarde du programme/fichier est effectuée)
        backup_filename = filename + ".keep"
        try:
            with open(filename, 'r') as f:
                content = f.read()
        except Exception as e:
            error(f"Erreur lors de la lecture du fichier {filename} : {str(e)}")
            return ""

        try:
            with open(backup_filename, 'w') as f:
                f.write(content)
        except Exception as e:
            error(f"Erreur lors de la création de la sauvegarde {backup_filename} : {str(e)}")
            return ""

        print(f"Backup created: {backup_filename}")

        # Modifie le fichier associé au programme
        try:
            with open(filename, 'w')  as f:
                print(response.choices[0].message.content)
                f.write(code)
        except Exception as e:
            error(f"Erreur lors de l'écriture dans le fichier {filename} : {str(e)}")
            return ""

        print(f"Fichier {filename} mis à jour avec le contenu du programme.")
    elif len(args) == 3 and args[1] == "save":
        filename = os.path.expanduser(args[2])
        config.conf["current_filename"]=filename
        print(f"config['current_filename']: {config.conf['current_filename']}")

        response = llm.ai_user_request(f"Affiche entre 2 lignes contenant '```' les lignes de {filename} que tu as mémorisé sans les numéroter. Si la dernière ligne ne possède pas de retour à la ligne, ajoute le. Tu termineras ta réponse par une ligne contenant [[[{filename}]]]")
        if response is None:
            error("Erreur lors de la génération de la réponse")
            return ""

        code=extract_code(response.choices[0].message.content)

        if code == "" :
            error("Pas de code !")
            return ""

        # Crée le fichier s'il n'existe pas
        try:
            with open(filename, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            with open(filename, 'w') as f:
                pass
            print(f"Fichier {filename} créé")

        # Enregistre le programme/fichier (une sauvegarde du programme/fichier est effectuée)
        backup_filename = filename + ".keep"
        try:
            with open(filename, 'r') as f:
                content = f.read()
        except Exception as e:
            error(f"Erreur lors de la lecture du fichier {filename} : {str(e)}")
            return ""

        try:
            with open(backup_filename, 'w') as f:
                f.write(content)
        except Exception as e:
            error(f"Erreur lors de la création de la sauvegarde {backup_filename} : {str(e)}")
            return ""

        print(f"Backup created: {backup_filename}")

        # Modifie le fichier associé au programme
        try:
            with open(filename, 'w')  as f:
                print(response.choices[0].message.content)
                f.write(code)
        except Exception as e:
            error(f"Erreur lors de l'écriture dans le fichier {filename} : {str(e)}")
            return ""

        print(f"Fichier {filename} mis à jour avec le contenu du programme.")
    elif len(args) > 1:
        error(f"Erreur : sous commande '{args[1]}' inconnue pour la commande $file")
    else:
        error("Erreur : mauvais nombre d'arguments pour la commande $file")
    return ""

def command_git(user_input):
    args = user_input.split()
    if len(args) < 2:
        error("Erreur : mauvais nombre d'arguments pour la commande $git")
        return ""

    command = "git " + " ".join(args[1:])
    print(f"Executing command: {command}")
    subprocess.run(command, shell=True)
    return ""

def command_system(user_input):
    args = user_input.split()
    if len(args) != 2:
        error("Erreur : mauvais nombre d'arguments pour la commande $system")
        return ""

    command = args[1].split()[0]
    authorized_commands = ["save", "load", "touch", "rm", "rmdir", "ls", "mkdir"]
    if command not in authorized_commands:
        error(f"Erreur : commande '{command}' non autorisée")
        return ""

    print(f"Executing command: {args[1]}")
    return f"$system {args[1]}"

def command_toggle(user_input):
    args = user_input.split()
    if len(args) == 2:
        key = args[1]
        if key in config.conf and isinstance(config.conf[key], bool):
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
    return ""

def load_conversation(file) :
    try:
        with open(os.path.expanduser(file), 'r') as f:
            conv = json.load(f)
            config.conf = conv[0]
            #config.system = conv[1]
            config.chat_history = conv[1:]
            print(f"Conversation chargée depuis {file}")
    except FileNotFoundError:
        error(f"Fichier {file} non trouvé")

def command_conversation(user_input):
    args = user_input.split()
    if len(args) == 3:
        if args[1] == "save":
            # Sauvegarde la conversation
            #conv=[config.conf]+[{"role" : "system", "content": config.conf["system"]}]+config.chat_history
            conv=[config.conf]+config.chat_history
            with open(os.path.expanduser(args[2]), 'w') as f:
                json.dump(conv, f, indent=4, ensure_ascii=False)
            print(f"Conversation sauvegardée dans {args[2]}")
        elif args[1] == "load":
            # Charge la conversation
            load_conversation(os.path.expanduser(args[2]))
        else:
            error("Erreur : commande $conversation inconnue")
    else:
        error("Erreur : mauvais nombre d'arguments pour la commande $conversation")
    return ""

def get_command(user_input):
    commands = {
    "help": command_help,
    "history": command_history,
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
    }

    # Recherche de la commande la plus proche
    possible_commands = []
    first_word = user_input.split()[0]
    for command in commands:
        if command.startswith(first_word):
            possible_commands.append(command)

    if len(possible_commands) == 1:
        return commands[possible_commands[0]]
    elif len(possible_commands) > 1:
        error("Conflit de commande : plusieurs commandes possibles")
        for command in possible_commands:
            print(command)
        return None
    else:
        return None

def common_prefix(s1, s2):
    return ''.join(c[0] for c in zip(s1, s2) if c[0] == c[1])

def ai_extend_request(user_input, client, chat_history):
    if user_input.startswith("$"):
        command = get_command(user_input[1:])
        if command:
            return command(user_input)
        else:
            return ""
    else:
        return user_input

def enregistre_fichier(fichier):
    config.conf["current_filename"]=fichier
    print(f"config['current_filename']: {config.conf['current_filename']}")

    response = llm.ai_user_request(f"Affiche entre 2 lignes contenant '```' les lignes de {fichier} que tu as mémorisé sans les numéroter. Si la dernière ligne ne possède pas de retour à la ligne, ajoute le. Tu termineras ta réponse par une ligne contenant [[[{fichier}]]]")
    if response is None:
        error("Erreur lors de la génération de la réponse")
        return ""

    code=tools.extract_code(response.choices[0].message.content)

    if code == "" :
        error("Pas de code !")
        return ""

    # Crée le fichier s'il n'existe pas
    try:
        with open(fichier, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        with open(fichier, 'w') as f:
            pass
        print(f"Fichier {fichier} créé")

    # Enregistre le programme/fichier (une sauvegarde du programme/fichier est effectuée)
    backup_filename = fichier + ".keep"
    try:
        with open(fichier, 'r') as f:
            content = f.read()
    except Exception as e:
        error(f"Erreur lors de la lecture du fichier {fichier} : {str(e)}")
        return ""

    try:
        with open(backup_filename, 'w') as f:
            f.write(content)
    except Exception as e:
        error(f"Erreur lors de la création de la sauvegarde {backup_filename} : {str(e)}")
        return ""

    print(f"Backup created: {backup_filename}")

    # Modifie le fichier associé au programme
    try:
        with open(fichier, 'w')  as f:
            print(response.choices[0].message.content)
            f.write(code)
    except Exception as e:
        error(f"Erreur lors de l'écriture dans le fichier {fichier} : {str(e)}")
        return ""

    print(f"Fichier {fichier} mis à jour avec le contenu du programme.")
    return ""

