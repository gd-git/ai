#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# set tabstop=4

import os
import readline
import argparse
import json
import subprocess
import sys
import time
import magic
import re
import random

import config
from config import config as conf 
from config import models as models
from config import chat_history as chat_history
from config import nbHistoryInit as nbHistoryInit
import traceback

from groq import Groq

import container

# Create the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

config.loadRc()
#config.printToStderr()

config.initModels()
#print(config.models)
for m in config.models["data"] :
    print(m["id"], m["context_window"], file=sys.stderr)

#config.getContextWindow(conf["model"])

from extend import extend

# type : document ou programme
def loadFile(type, fileName) :
    global nbHistoryInit
    global chat_history

    print("Load "+type+" "+fileName+" ...",end="", file=sys.stderr)
    sys.stderr.flush()

    #time.sleep(3)
    try :
        type_mime = magic.from_file(fileName, mime=True)

    except FileNotFoundError:
        print(f"Erreur: le fichier {fileName} n'existe pas ou est illisible.", file=sys.stderr)
        exit(1)


    print(type_mime)

    if type == "programme" :
        os.environ["PROG_NAME"]=fileName
    elif type == "document" :
        os.environ["DOC_NAME"]=fileName

    if type_mime=="application/pdf" :

        contenu = subprocess.run(f"pdftotext -layout {fileName} -", shell=True, capture_output=True, text=True,
                                 universal_newlines=True).stdout
        #, universal_newlines=True)

        #with open(fileName, 'rb') as pdf_file:
        #    pdf_reader = PyPDF2.PdfReader(pdf_file)
        #    num_pages = len(pdf_reader.pages)
        #    contenu = ''
        #    for page_num in range(num_pages):
        #        page = pdf_reader.pages[page_num]
        #        if page.extract_text():
        #            contenu += page.extract_text() + " "

            # Normalize whitespace and clean up text
         #   contenu = re.sub(r'\s+', ' ', contenu).strip()
    else :
        with open(fileName, 'r') as fichier:
            contenu = fichier.read()

    print(contenu)

    nbHistoryInit=nbHistoryInit+1

    content="Pour cette requête tu ne répondras pas et tu n'afficheras rien. Apprend simplement que toutes les lignes du "+type+" "+fileName+" sont les suivantes :" +chr(10) + contenu

    ia_request(content)

    #chat_history.append({"role": "user", "content": content})
    #try:
    #    response = client.chat.completions.create(model=conf["model"],
    #                                           messages=chat_history,
    #                                           max_tokens=5000,
    #                                           temperature=conf["temperature"],
    #                                           )
    #except Exception as e:
    #    traceback.print_exc()
    #    print("Erreur lors de la génération de la réponse : ", str(e))
    #    exit(2)

 
    #except FileNotFoundError:
    #    print(f"Erreur: le fichier {fileName} n'existe pas ou est illisible.", file=sys.stderr)
    #    exit(1)

    #nbHistoryInit=nbHistoryInit+1

    #print("OK", file=sys.stderr)
    #json.dumps(chat_history, indent=4)


def whenQuit():
    print
    print("bye")
    exit(0)

def ia_request(user_input) :
    global chat_history
    global nbHistoryInit
    global args

    #print("IA request :"+user_input)
    #print("raw : "+user_input)
    if user_input.startswith("$"):
        user_input = extend(user_input, client, chat_history)
        print("ext : "+user_input)

    if user_input == "" :
        return ""

    chat_history.append({"role": "user", "content": user_input}) #if chat_history 

    #print("+°+°+°+°+°+")
    #print(chat_history)

    if conf["seed"] :
        seed=conf["seed "]
    else :
        seed = random.randint(0, 1000000)

    #print(f"max_tokens={config.context_window} seed={seed} temperature={conf['temperature']}")
    #max_tokens=config.context_window,

    try:
        response = client.chat.completions.create(model=conf["model"],
            messages=chat_history,
            max_tokens=8000,
            seed=seed,
            temperature=conf["temperature"],
            )
    except Exception as e:
        traceback.print_exc()
        print("Erreur lors de la génération de la réponse : ", str(e))
        response = None
        return None

    # Save the last response to last_response.txt
    with open("last_response.txt", "w") as f:
        f.write(response.choices[0].message.content)

    responseMsg=response.choices[0].message.content

    if conf["compress"] and len(responseMsg) > 78 :
        responseMsg=responseMsg[:78]+"…"

    # Append the response to the chat history
    chat_history.append({ "role": "assistant", "content": responseMsg })
    # Print the response

    #nbHistoryInit=nbHistoryInit+1

    hlen=len(chat_history)
    currentLen=int(((len(chat_history)-1)/2 - nbHistoryInit)) # Nombre de couples (user+assistant) sans "system"
    numKeep=min(conf['length_history'], currentLen)

    debug=0

    if debug==1 :

        print(f"hlen: {hlen}")
        print(f"length_history: {conf['length_history']}")
        print(f"nbHistoryInit: {nbHistoryInit}")
        print(f"currentLen: {currentLen}")
        print(f"numKeep: {numKeep}")

        print("&&&&&&&&&&&& begin : chat_history")
        print(json.dumps(chat_history, indent=4).encode('utf-8').decode('unicode_escape'))
        print("&&&&&&&&&&&& end")

    new=chat_history[:nbHistoryInit*2+1] # system + program/documents
    #print(new)
    #print("&&&&&&&&&&&& new 2")
    numKeep=min(conf['length_history'], currentLen)
    #print(f"======================== numKeep 1 : {numKeep}")

    if numKeep > 0 :

        v=(numKeep)*2
        if debug==1 :
            print(f"v: {v}")
        new=new+chat_history[-v:]

    chat_history=new

    if debug==1 :

        print(json.dumps(chat_history, indent=4).encode('utf-8').decode('unicode_escape'))
        print("+++++++++++++++++++")

    if args.conversation :
        s=json.dumps(chat_history, indent=4)
        s=s.replace(chr(10),chr(92)+chr(110))
        s=s.replace('"', chr(92)+chr(34))
        #json_string=json_string.encode('utf-8').decode('unicode_escape')

        with open(os.path.expanduser(args.conversation), 'w') as f:
            #f.write(json_string.encode('utf-8').decode('unicode_escape').replace(chr(10),chr(10)) )

            f.write(s.encode('utf-8').decode('unicode_escape'))

    if debug==1 :
        print("&&&&&&&&&&&&-------------------")
    return response

####################################################################

def main():
    global args

    if args.question:
        response=ia_request(args.question)
        if response :
            print
            print(response.choices[0].message.content)
            exit(2)
        else :
            exit(1)

    auto_question=""

    while True:
        if auto_question == "" :
            prompt=f"{conf['model']} {config.getContextWindow(conf['model'])}"
            # Get user input from the console
            if sys.stdin.isatty():
                if conf["extend"] :
                    print(f"\n>>> ({prompt}) >>> Ctrl D pour terminer l'entrée, CTRL C pour quitter le programme")
                else :
                    print(f"\n>>> ({prompt}) >>>")

            try:
                if conf["extend"] :
                    user_input = config.multiInput()
                else:
                    try :
                        user_input =input()
                    except EOFError :
                        continue

            except (KeyboardInterrupt) :
                whenQuit()
                exit()
        else :
            user_input=auto_question
            auto_question=""
            print(user_input)

        if not user_input:
            continue

        #print("user_input :" + user_input)

        print("Send...")

        response=ia_request(user_input) 

        if response :
            # Save the last response to last_response.txt
            last_response=response.choices[0].message.content
            #with open("last_response.txt", "w") as f:
            #    f.write(response.choices[0].message.content)

            print("------------------------------------------")
            print()
            print(response.choices[0].message.content)

            exec=1
            if exec == 1 :
                pattern = r"\$exec\('(.*)', *'(.*)'\)"
                matches = re.findall(pattern, last_response, re.DOTALL)

                if matches:
                    user = matches[0][0]
                    contenu = matches[0][1]
                    # Recherche sur Internet les IA accessible en ligne gratuitement via une requete lunx -dump
                    # Recherche sur Internet les IA accessibles par curl
                    # Recherche sur Internet avec une commande lynx -dump les IA accessibles par l'API curl.
                    # Crée le fichier /tmp/aaa/f.txt contenant la chaine "Super cool !"
                    auto_question=container.exec(user, contenu)
        if not sys.stdin.isatty():
            break

# Main

parser = argparse.ArgumentParser(add_help=False,description='Chat with an AI helper')
parser.add_argument('-c', '--conversation', help='Créer/reprendre une discussion')
parser.add_argument('-d', '--document', action='append', help='Documents to be loaded')
parser.add_argument('-g', '--seed', type=int, help='Set the seed for the model')
parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
parser.add_argument('-l', '--length_history', type=int, help='Set the length of history') 
parser.add_argument('-m', '--model', help='Choose a model')
parser.add_argument('-p', '--program',action='append', help='Program to be loaded')
parser.add_argument('-q', '--question', help='Ask a question and quit')
parser.add_argument('-s', '--system', help='Définir le type d\'assistant')
parser.add_argument('--system-file', help='Définir le type d\'assistant à partir d\'un fichier')
parser.add_argument('-t', '--temperature', type=float, default=0.1, help='Set the temperature for the model')
parser.add_argument('-v', '--verbose', action='store_true', help='Affiche des informations supplémentaires')
parser.add_argument('-x', '--extend', action='store_true', help='Question sur plusieurs lignes (CTRL D) pour finir la question')
parser.add_argument('-z', '--compress', action='store_true', help='Mémorise les réponses de l\'IA sous forme courte')

args = parser.parse_args()

#print(f"args: {args}")

if args.length_history!=None :
    print(f"length_history: {args.length_history}")

if args.help:
        parser.print_help()
        exit()

if args.verbose :
    config.verbose=True

if args.system :
    conf["system"]=args.system

print(args)

if args.system_file :
    cat=""
    for file in args.system_file.split(",") :
        with open(file, 'r') as f:
            cat=cat+"\n"+f.read()
    conf["system"]=cat


v=vars(args)
for a in ["system", "extend", "model", "temperature", "seed", "length_history", "compress"] :
    if v[a]!=None :
        print(f"a: {a} {v[a]}")
        #print(":",a, "=", v[a])
        conf[a]=v[a]

print("======", file=sys.stderr)
config.context_window=config.getContextWindow(conf["model"])
config.printToStderr()
print("======", file=sys.stderr)
print(f"context_window={config.context_window}", file=sys.stderr)
print("======", file=sys.stderr)


# Set the system prompt
system = {
    "role": "system",
    "content": conf["system"]
}

# Initialize the chat history
chat_history = [ system ]
    

if args.program:
    for file in args.program:
        loadFile("programme", file)

if args.document:
    for file in args.document:
        loadFile("document", file)

if args.conversation :
    file=os.path.expanduser(args.conversation)
    if os.path.exists(file) :
        with open(file, 'r') as f:
            json_string = f.read()
            json_string = json_string.replace(chr(92), chr(92)+chr(92))
            json_string = json_string.replace(chr(10), chr(92)+chr(110))
            json_string = json_string.replace(chr(10), chr(92)+chr(110))
            json_string = json_string.rstrip(chr(10))
            json_string = json_string.strip(chr(92)+chr(110))
            #print("||||||||||||||||||")
            #print(json_string)
            chat_history = json.loads(json_string)
            #print("||||||||||||||||||")
            #print(chat_history)
                #pickle.load(f)
            #except EOFError:
            #    pass

#nbHistoryInit=nbHistoryInit=len(chat_history)

#print("°°°°°°°°°°°°°°°°°°°°")
#print(f"nbHistoryInit: {nbHistoryInit}")
#print(chat_history)


#print("args:",args)
#print("args:",vars(args))
#print("conf:",conf)

if __name__ == "__main__":
    main()
