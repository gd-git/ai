# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
#from tools import error as error  
def error(msg): tools.error(msg)
    
def error(msg) :
    print(f"\033[1;31m{msg}\033[0m", file=sys.stderr)
    config.last_error=msg

def warning(msg) :
    print(f"\033[38;5;208m{msg}\033[0m", file=sys.stderr)

def verbose(msg) :
    if config.conf['verbose'] == True or config.conf['verbose'] == "True":
        
        print(Fore.MAGENTA+msg+Style.RESET_ALL)

def red(msg) :
    print(Fore.RED+msg+Style.RESET_ALL)
    
def confirmation(command):
    print(f"Exécuter "+Fore.RED+command+""+Style.RESET_ALL, end='' ) 
    reponse = input(f" ? [Yn] ")
    return reponse.strip().upper() in ["Y", "O", ""]
    
def extract_current_filename(chaine):
    motif = r'\[\[\[([^{]]*)\]\]\]'
    #print(f"TRACE recherche filename dans : {chaine}") 
    correspondance = re.search(motif, chaine)
    #print(f"TRACE Résultat de la recherche du pattern : {correspondance}")
    if correspondance:
        filename=correspondance.group(1)
        #print(f"TRACE Nom du fichier extrait : {filename}")
        return filename
    return None

def extract_code(contents):
    lines = contents.splitlines()
    code = []
    in_code = False

    for line in lines:
        if line.strip().startswith('```'):
            in_code = not in_code
        elif in_code:
            code.append(line)

    if code and not code[-1].endswith("\n"):
        code[-1] += "\n"  # Ajoute un retour à la ligne à la dernière ligne si nécessaire

    return '\n'.join(code)


def toBool(s):
    if s in ["True", "true"]:
        return True
    elif s in ["False", "false"]:
        return False
    else:
        return s



def loadFile(fileName, test=False) :

    tools.verbose(f"Chargement de {fileName}")
    parsed_url=urlparse(fileName)
    cache_dir="~/.ai/cache"

    print("Schéma :", parsed_url.scheme)
    print("Hôte :", parsed_url.netloc)
    print("Chemin :", parsed_url.path)
    print("Paramètres :", parsed_url.params)
    print("Query :", parsed_url.query)
    print("Fragment :", parsed_url.fragment)


    if parsed_url.netloc != "" :
        path=parsed_url.netloc
        basename=os.path.basename(parsed_url.path)
        dirname=os.path.dirname(parsed_url.path)
        local_dir=cache_dir+"/"+parsed_url.netloc+"/"+dirname
        local_dir=os.path.expanduser(local_dir)
        local_file=local_dir+"/"+basename
        
        os.makedirs(local_dir, exist_ok=True)
       
        #os.path.expanduser(chemin)
        command="lynx -dump "+fileName+" | gawk '/^ *Notes et références/{exit} 1' > "+local_file
        
        print(f"Commands : {command}")
        
        code_retour = subprocess.call(command, shell=True)
        if code_retour != 0 :
            tools.error(f"Le téléchargement {fileName} à échoué :")
            return False
        else :
            fileName=local_file
            
        
    type=""

    try :
        type_mime = magic.from_file(fileName, mime=True)

    except FileNotFoundError:
        error(f"Erreur: le fichier {fileName} n'existe pas ou est illisible.")
        return False

    if type_mime=="application/pdf" :
        print(f"Convert {fileName} to text...")
        contenu = subprocess.run(f"pdftotext -layout {fileName} -", shell=True, capture_output=True, text=True, universal_newlines=True).stdout
        
    else :
        with open(fileName, 'r') as fichier:
            contenu = fichier.read()

    if test == True :
        return True
        
    print(f"Load {fileName} ({type_mime}) ...")
    #print(contenu)

    longName=os.path.expanduser(fileName)

    content=f"Pour cette question uniquement tu ne répondras pas et tu n'afficheras rien " \
        f"à l'exception d'une ligne : [[[{longName}]]]. " \
        f" Apprend simplement que toutes les lignes du {type} {longName} " \
        f" (qui devient le document courant) sont les suivantes :" +chr(10) + contenu

    #print(f"DEBUG ai_user_request : {content}")

    try :
        response = llm.ai_user_request(content, llm.ai_user_request)
    except Exception as e:
        config.last_chunk=response
        traceback.print_exc()
        raise e
            
    if response is None:
        error("Erreur lors de la génération de la réponse")
        return ""
 
   # print(f"DEBUG ai_user_request : config.conf['current_filename'] = {longName}")
    config.conf['current_filename'] = longName
    
    if longName not in config.conf['files']:
        config.conf['files'].append(longName)

def closeFile(filename) :    
    if filename in config.conf['files']:
        config.conf['files'].remove(filename)

    command.purge_filename(filename)
    config.conf['current_filename'] = ""

def saveFile(source, destination):

    print(f"~~~ tools.saveFile {source} {destination}")

    if source == "" :
        source=config.conf["current_filename"]
        print(f"~~~ tools.saveFile {source} {destination}")
        
    if destination == "" :
        destination=source
        print(f"~~~ tools.saveFile {source} {destination}")
        
    if not source:
        error("Erreur : nom de fichier non défini")
        return

    config.conf["current_filename"]=source
    
    print(f"config['current_filename']: {config.conf['current_filename']}")

    content=f"Affiche entre 2 lignes contenant '```' les lignes de {source} " \
        f"que tu as mémorisé sans les numéroter. " \
        f"Si la dernière ligne ne possède pas de retour à la ligne, ajoute le. " \
        f"Tu termineras ta réponse par une ligne contenant [[[{source}]]]"

    #print(f"DEBUG ai_user_request : {content}")

    response = llm.ai_user_request(content)
    if response is None:
        error("Erreur lors de la génération de la réponse")
        return ""

    code=tools.extract_code(response.choices[0].message.content)

    if code == "" :
        error("Pas de code !")
        return ""

    # Crée le fichier s'il n'existe pas
    
    try:
        with open(destination, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        with open(destination, 'w') as f:
            pass
        print(f"Fichier {destination} créé")

    # Enregistre le programme/fichier (une sauvegarde du programme/fichier est effectuée)
    backup_filename = destination + ".keep"
    try:
        with open(destination, 'r') as f:
            content = f.read()
    except Exception as e:
        error(f"Erreur lors de la lecture du fichier {destination} : {str(e)}")
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
        with open(destination, 'w')  as f:
            #print(response.choices[0].message.content)
            f.write(code)
    except Exception as e:
        error(f"Erreur lors de l'écriture dans le fichier {destination} : {str(e)}")
        return ""

    print(f"Fichier {destination} mis à jour avec le contenu du programme.")
    return ""

def taille_en_octets_humaine(taille):
    if taille < 1024:
        return f"{taille} o"
    elif taille < 1024**2:
        return f"{taille/1024:.0f} Ko"
    elif taille < 1024**3:
        return f"{taille/1024**2:.0f} Mo"
    else:
        return f"{taille/1024**3:.0f} Go"

def readline_get_history():
    history = []
    for i in range(readline.get_current_history_length()):
        history.append(readline.get_history_item(i + 1))
    return history

def readline_set_history(lines):
    for line in lines:
        readline.add_history(line)

def readline_purge_history():
    readline.clear_history()
    
def url_to_filename(url):
    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename

"""        
def color(color, type_color):
    colors = {"black":0, "red":1, "green":2, "yellow":3, "blue":4, "magenta":5, "cyan":6, "white":7}
    if type_color == "foreground": return f"\033[38;5;{colors[color]}m"
    elif type_color == "background": return f"\033[48;5;{colors[color]}m"

def reset():
    return "\033[0m"

def pcol(text, foreground_color=None, background_color=None):
    if foreground_color: text = color(foreground_color, "foreground") + text
    if background_color: text = color(background_color, "background") + text
    text += reset()
    print(text)
"""

def beep() :

    return
    
    stream = config.audio.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
    frequency = 1000
    duration = 0.05
    t = np.linspace(0, duration, int(44100 * duration), False)
    note = np.sin(frequency * t * 2 * np.pi)
    note *= 0.5
    stream.write(note.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()
    #p.terminate()

