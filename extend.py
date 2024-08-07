
# -*- coding: utf-8 -*-
# set tabstop=4

import os
import re
import json
import config 
from config import config as conf
from config import models as models
from config import chat_history as chat_history
import traceback

from groq import Groq

import hashlib

import warnings
warnings.simplefilter("ignore",category=Warning)
import requests


def md5_sum(file_name):
    md5_hash = hashlib.md5()
    with open(file_name, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def extract_code(contents):

    start_tag = '^```'
    end_tag = '^```'

    lines = contents.splitlines()
    start_line = -1
    end_line = -1

    for i, line in enumerate(lines):
        if re.match(start_tag, line) and start_line==-1:
            if start_line == -1:
                start_line = i
        elif re.match(end_tag, line):
            end_line = i-1
            break

    if start_line != -1 and end_line != -1:
        return '\n'.join(lines[start_line+1:end_line])
    else:
        return contents

# fonction pour afficher la valeur de "context_window" associé à un ID
def get_context_window(data, id):
    for model in data["data"]:
        if model["id"] == id:
            return model["context_window"]
    return None

def extend(user_input, client, chat_history):

    #print("model :", conf["model"])

    if user_input.startswith("$h"):
        dumps=json.dumps(chat_history, indent=4)
        print(dumps.encode('utf-8').decode('unicode_escape'))
        with open("last_response.txt", "w") as f:
                f.write(dumps)
        return ""
    elif user_input.startswith("$m"):
        #print("model:", conf["model"])
        arg=""
        try:
            arg=user_input.split()[1]
        except Exception as e:
            print
            #print(e)

        if arg == "list":
            api_key = os.environ.get("GROQ_API_KEY")
            url = "https://api.groq.com/openai/v1/models"

            headers = { "Authorization": f"Bearer {api_key}", "Content-Type": "application/json" }

            response = requests.get(url, headers=headers)
            data = response.json()

            print(json.dumps(data, indent=4))

            for item in data["data"]:
                #cw=get_context_window(data["data"], id)
                cw=item["context_window"]
                print(item["id"], " ", cw)
        elif arg=="":
            print(conf["model"])
        else:
            pass
            #print("model: ",arg)
            #conf["model"]

        return ""

    elif user_input.startswith("$w"):
        # Enregistre le programme/fichier (une sauvegarde du programme/fichier est effectuée)
        backup_filename = os.environ.get("PROG_NAME") + ".keep"
        with open(os.environ.get("PROG_NAME"), 'r') as f:
            content = f.read()
        with open(backup_filename, 'w') as f:
            f.write(content)
        print(f"Backup created: {backup_filename}")

        try:
            response = client.chat.completions.create(model=conf["model"], messages=chat_history + [{"role": "user", "content": "Affiche les lignes du programme sans les numéroter."}], temperature=conf["temperature"]).choices[0].message.content

        except Exception as e:
            traceback.print_exc()
            print("Erreur lors de la génération de la réponse : ", str(e))
            response = None
            return ""

        # Modifie le fichier associé au programme
        with open(os.environ.get("PROG_NAME"), 'w')  as f:
            f.write(extract_code(response))
            print("Fichier mis à jour avec le contenu du programme.")
            return ""
    elif user_input.startswith("$u"):
        # Récupère la sauvegarde du programme
        backup_filename = os.environ.get("PROG_NAME") + ".keep"
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
            print(f"No backup found: {backup_filename}")
        return ""
    elif user_input.startswith("$p"):
        return "Affiche les lignes du programme sans les numéroter."
    elif user_input.startswith("$t"):
        # Execute the command in the AI_TEST_COMMAND environment variable
        command = os.environ.get("AI_TEST_COMMAND")
        if command:
            print(f"Executing command: {command}")
            subprocess.run(command, shell=True)
        else:
            print("No command to execute.")
        return ""
    elif user_input.startswith("$c"):
        arg=""
        try:
            arg=user_input.split()[1]
        except Exception as e:
            print(conf)
            return ""

        if arg == "write":
            print("write")
            config.saveRc()

        else :
            conf[user_input.split()[1]]=user_input.split()[2]

        return ""
    else:
        return user_input
