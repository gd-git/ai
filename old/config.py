# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
def error(msg): tools.error(msg)

warnings.simplefilter("ignore",category=Warning)

args=[]
rcFile="~/.airc"

# Dictionnaire pour stocker les configurations

conf = {}

chat_history=[]
last_response=""
backup_filename=""

# Tu afficheras AVANT chaque réponse l'estimation de son taux de fiablité et sa justification.

system="""
Tu es un assistant utile.
Tu es capable d'afficher beaucoup de lignes.
Tu répondras avec des réponses courtes.
Si ma demande n'est pas assez claire ou si elle est ambigüe de me demanderas des précisions PLUTÔT QUE D'Y RÉPONDRE !
Tu répondras en français !
"""

conf["system"]=system

conf['provider']="groq"
conf["model"]="llama-3.1-70b-versatile"
conf["temperature"]=0
conf["seed"]=""
conf["current_filename"]=""
conf["verbose"]=False
conf['debug']=False
conf["multi_lines"]=False
conf["ansi"]=True
conf['files']=[]
conf['background']="light" # light
conf['colors_style']="default"
conf['stream']=True

context_window=8192

parser=None

def init() :
    config.loadRc()

    config.args=config.parseArgs()

    if config.args.help:
        config.parser.print_help()
        exit()

    if config.args.debug :
        config.conf["debug"]=True

    if config.args.verbose :
        config.conf["verbose"]=True

    if config.args.system :
        config.conf["system"]=' '.join(config.args.system)        

    if config.args.system_file :
        cat=""
        for file in config.args.system_file.split(",") :
            with open(file, 'r') as f:
                cat=cat+"\n"+f.read()
        config.conf["system"]=cat

    if config.args.option:
        for l in config.args.option:
            for o in l.split(",") :
                if o == "":
                    continue
                config.setOption(o)

    if config.args.model:
        config.conf["model"]=config.args.model

    if config.args.conversation :
        file=os.path.expanduser(config.args.conversation)
        command.load_conversation(file)

    if config.args.multi_lines :
        config.conf["multi_lines"]=True
        
    if config.args.provider :
        config.conf["provider"]=  config.args.provider
        
    llm.initProvider(config.conf["provider"])
    
    if config.args.file:
        if config.args.file:
            for l in config.args.file:
                for file in l.split(",") :
                    if file == "" :
                        continue
                    if not os.path.exists(file):
                        print(f"Erreur : le fichier '{file}' n'existe pas.")
                        exit(1)
            for l in config.args.file:
                for file in l.split(",") :
                    if file == "" :
                        continue
                    tools.loadFile(file)

    extend.initSystem()
    
def printChatHistory() :
    global chat_history

    print(json.dumps(chat_history, indent=4, ensure_ascii=False))

def setOption(option) :
    key, value = option.split("=")
    if key in conf.keys():
        conf[key]=tools.toBool(value)
    else :
        error(f"{key} n'est pas une option valide !")
        exit(1)


def parseArgs() :
    global args
    global parser

    parser = argparse.ArgumentParser(add_help=False,description='Chat with an AI helper')
    parser.add_argument('-d', '--debug', action='store_true', help='Mode debug')
    parser.add_argument('-c', '--conversation', help='Créer/reprendre une discussion')
    parser.add_argument('-f', '--file', action='append', help='File(s) to be loaded')
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
    parser.add_argument('-m', '--model', help='Choose a model')
    parser.add_argument('-o', '--option',action='append', help='Set one or more option(s)')
    parser.add_argument('-p', '--provider', help='Provider')
    parser.add_argument('-q', '--question', nargs='+', action='append', help='Ask a question and quit')
    parser.add_argument('-r', '--system-file', help='Définir le type d\'assistant à partir d\'un ou plusieurs fichiers')
    parser.add_argument('-s', '--system', nargs='+', help='Définir le type d\'assistant')
    parser.add_argument('-t', '--temperature', type=float, default=0.0, help='Set the temperature for the model')
    parser.add_argument('-v', '--verbose', action='store_true', help='Affiche des informations supplémentaires')
    parser.add_argument('-l', '--multi-lines', action='store_true', help='Question sur plusieurs lignes (CTRL D) pour finir la question')
    parser.add_argument('-x', '--extend', action='store_true', help='Mode étendu (extend/extend')
    parser.add_argument('-z', '--raz', action='store_true', help='Supprime le fichier ~/.ia-conversation')
    parser.add_argument('-z', '--compress', action='store_true', help='Mémorise les réponses de l\'IA sous forme courte')

    args = parser.parse_args()
    return args

def loadRc() :
    rc={}
    if os.path.exists(os.path.expanduser(rcFile)):
        with open(os.path.expanduser(rcFile), 'r') as f:
            rc = json.load(f)
        conf.update(rc)

def saveRc() :
    rc=copy.deepcopy(conf)
    del rc["system"]
    with open(os.path.expanduser(rcFile), 'w') as f:
        f.write(json.dumps(rc, indent=4, ensure_ascii=False)+"\n")

def printRc() :
    rc=copy.deepcopy(conf)
    del rc["system"]
    print(json.dumps(rc, indent=4, ensure_ascii=False)+"\n")


    
def printToStderr() :
    for var, value in conf.items():
        if isinstance(conf[var], str):
            print(f"{var}=\"{value}\"", file=sys.stderr)
        else :
            print(f"{var}={value}", file=sys.stderr)


def multiInput() :
    lines=[]
    while True :
        try :
            #line=readline.input()
            line=input()
            
        except EOFError :
            break

        if line=="" :
            print("")
        lines.append(line)


    return '\n'.join(lines).replace(chr(10),'\\n')
