
# -*- coding: utf-8 -*-
# set tabstop=4

import os
import sys
import json
import random
import argparse
import traceback
import pprint
import re
import langdetect
import pygments
import copy
#from pygments import highlight
#from pygments.lexers import get_lexer_by_name
#from pygments.lexers import get_lexer_for_code
from pygments.lexers import guess_lexer
from pygments.formatters import TerminalFormatter
from pygments.formatters import Terminal256Formatter
from pygments.lexers import get_lexer_for_mimetype
from pygments.lexers import CppLexer

import magic
import llm


import warnings
warnings.simplefilter("ignore",category=Warning)

args=[]
rcFile="~/.airc"

# Dictionnaire pour stocker les confurations
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

#conf["model"]="llama3-groq-70b-8192-tool-use-preview"
conf['provider']="groq"
conf["model"]="llama-3.1-70b-versatile"
conf["temperature"]=0.1
conf["seed"]=""
conf["length_history"]=100
conf["current_filename"]=""
conf["verbose"]=False
conf["multi_lines"]=False
conf["ansi"]=True
conf['files']=[]
conf['background']="light" # light
conf['colors_style']="default"


context_window=8192

parser=None

def error(msg) :
    print(msg, file=sys.stderr)

    
def printChatHistory() :
    global chat_history

    print(json.dumps(chat_history, indent=4, ensure_ascii=False))






def setOption(option) :
    key, value = option.split("=")
    if key in conf.keys():
        conf[key]=value
    else :
        error(f"{key} n'est pas une option valide !")
        exit(1)


def parseArgs() :
    global args
    global parser

    parser = argparse.ArgumentParser(add_help=False,description='Chat with an AI helper')
    parser.add_argument('-c', '--conversation', help='Créer/reprendre une discussion')
    parser.add_argument('-f', '--file', action='append', help='File(s) to be loaded')
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
    parser.add_argument('-l', '--length_history', type=int, help='Set the length of history')
    parser.add_argument('-m', '--model', help='Choose a model')
    parser.add_argument('-o', '--option',action='append', help='Set one or more option(s)')
    parser.add_argument('-p', '--provider', help='Provider')
    parser.add_argument('-q', '--question', nargs='+', action='append', help='Ask a question and quit')
    parser.add_argument('-r', '--system-file', help='Définir le type d\'assistant à partir d\'un ou plusieurs fichiers')
    parser.add_argument('-s', '--system', help='Définir le type d\'assistant')
    parser.add_argument('-t', '--temperature', type=float, default=0.1, help='Set the temperature for the model')
    parser.add_argument('-v', '--verbose', action='store_true', help='Affiche des informations supplémentaires')
    parser.add_argument('-x', '--multi-lines', action='store_true', help='Question sur plusieurs lignes (CTRL D) pour finir la question')
    parser.add_argument('-z', '--compress', action='store_true', help='Mémorise les réponses de l\'IA sous forme courte')

    args = parser.parse_args()
    return args



def highlightCode(code):

    #print("********************************************************")
    #print("CODE:"+code)
    #code="\n".join(code)

    # Déterminez le langage du code
    m = magic.Magic(mime=True)
    file_type = m.from_buffer(code).replace("script.", "")

    #print("file_type: "+file_type)

    #return code

    # Créez un objet Lexer à partir du type MIME
    #print("Try : get_lexer_for_mimetype")
    try:
        # Créez un objet Lexer à partir du type MIME
        lexer = get_lexer_for_mimetype(file_type)
        #lexer = get_lexer_for_code(code)
        #lexer=guess_lexer(code)
    except ValueError as e:
        #print(f"Erreur : get_lexer_for_mimetype ({file_type}) - {e}")
        #print("Try : guess_lexer");
        try :
            lexer=guess_lexer(code)
        except ValueError as e:
            print(f"Erreur : guess_lexer ({file_type}) - {e}")
            return code



    # Mettez en évidence le code
    try:
        style=conf['colors_style']
    except :
        conf['colors_style']="default"

    if conf['background'] == "dark" :
        formatter = Terminal256Formatter(fg='dark', bg='light', style=conf['colors_style'])
    else :
        formatter = Terminal256Formatter(fg='light', bg='dark', style=conf['colors_style'])

    highlighted_code = pygments.highlight(code, lexer, formatter)

    # Renvoyez le code colorisé
    #print("highlighted_code :"+highlighted_code)
    return highlighted_code #.replace(r"\033", chr(27))

def highlightBloc(lines, change):
    in_code = False
    new = []
    bloc = []

    for line in lines:
        #print("    ---> line: "+line)
        if re.match(r'^```', line):
            #print("MATHC")

            if in_code:
                # Bloc de code terminé, appliquer la fonction change
                #modified_bloc = change("\n".join(bloc))
                modified_bloc = change("\n".join(bloc))
                #new.extend(modified_bloc)
                #new.extend(modified_bloc.split('\n'))
                new.append(modified_bloc)
                new.append(line)
                in_code = False
                bloc = []
            else:
                # Début d'un bloc de code
                in_code = True
                new.append(line)
        else:
            if in_code:
                # Ajouter la ligne au bloc de code
                bloc.append(line)
                #new.append(line)
            else:
                # Ajouter la ligne au résultat
                new.append(line)
    return "\n".join(new)

    #return "".join(new)



def loadRc() :
    rc={}
    if os.path.exists(os.path.expanduser(rcFile)):
        print(f"Load {rcFile}")
        with open(os.path.expanduser(rcFile), 'r') as f:
            rc = json.load(f)
        #print(json.dumps(rc, indent=4, ensure_ascii=False)+"\n")
        conf.update(rc)

def saveRc() :
    rc=copy.deepcopy(conf)
    del rc["system"]
    with open(os.path.expanduser(rcFile), 'w') as f:
        #f.write("# Fichier généré automatiquement\n\n")
        f.write(json.dumps(rc, indent=4, ensure_ascii=False)+"\n")

        
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
            line=input()
        except EOFError :
            break

        if line=="" :
            print("")
        lines.append(line)


    return '\n'.join(lines).replace(chr(10),'\\n')


