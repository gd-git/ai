
# -*- coding: utf-8 -*-
# set tabstop=4

import os
import sys
import json

import warnings
warnings.simplefilter("ignore",category=Warning)
import requests

nbHistoryInit=0

rcFile="~/.iarc"

# Dictionnaire pour stocker les configurations
config = {}

chat_history=[]

# llama3-groq-70b-8192-tool-use-preview
# llama-3.1-70b-versatile
# mixtral-8x7b-32768
# llama-3.1-405b-reasoning
# llama3-8b-8192

# Tu afficheras AVANT chaque réponse l'estimation de son taux de fiablité et sa justification.

config["assistant"]="""
Tu es un assistant utile. 
Tu es capable d'afficher beaucoup de lignes. 
Tu répondras avec des réponses courtes. 
Tu me vouvoyeras. 
Si ma demande n'est pas assez claire ou si elle est ambigüe de me demanderas des précisions PLUTÔT QUE D'Y RÉPONDRE !
Tu répondras en français !
"""
#config["model"]="llama3-groq-70b-8192-tool-use-preview"
config["model"]="llama-3.1-70b-versatile"
config["temperature"]=0.1
config["seed"]=""
config["length_history"]=100

context_window=8192

models={}

def initModels() :
    global models

    api_key = os.environ.get("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/models"

    headers = { "Authorization": f"Bearer {api_key}", "Content-Type": "application/json" }

    response = requests.get(url, headers=headers)
    models = response.json()
    #print(models)
    #print(json.dumps(models, indent=4))
    #print("=====")

def getContextWindow(model) :
    global models

    #print (json.dumps(models,indent=4))
    for m in models["data"] :
        #print(m["id"])
        if m["id"] == model :
            return m["context_window"]
    return None



def loadRc() :
    if os.path.exists(rcFile):
        with open(os.path.expanduser(rcFile), 'r') as f:
            for line in f:
                if chaine.strip().startswith("#") or chaine.strip() == '' :
                    continue
                line = line.strip()
                if line:
                    var, value = line.split('=')
                    config[var] = value

def saveRc() :
    print("iarc : os.path.expanduser(rcFile)")
    with open(os.path.expanduser(rcFile), 'w') as f:
        f.write("# Fichier généré automatiquement\n\n")
        for var, value in config.items():
            try:
                v=float(value)
                value=v

                v=int(value)
                if v==value :
                    value=v
            except ValueError:
                pass

            if isinstance(config[var], str):
                f.write(f"{var}=\"{value}\"\n")
            else :
                f.write(f"{var}={value}\n")

def printToStderr() :
    for var, value in config.items():
        if isinstance(config[var], str):
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


    #return '\n'.join(lines)
    return '\n'.join(lines).replace(chr(10),'\\n')


