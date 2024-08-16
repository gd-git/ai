from config import error as error

import os
import readline
import json
import subprocess
import sys
import time
import magic
import re
import traceback

import llm

import extend
import config
import pygments
#from config import config as conf 
#from config import models as models
#from config import system as system
#from config import chat_history as chat_history
#from config import nbHistoryInit as nbHistoryInit
#from config import parseArgs as parseArgs
#from config import args as args
#from config import last_response as last_response
#from config import backup_filename as backup_filename


#from extend import ai_user_request as ai_user_request
#from extend import ai_extend_request as ai_extend_request

import container

config.loadRc()
#config.printToStderr()

#print(config.models)
#for m in config.models["data"] :
#    print(m["id"], m["context_window"], file=sys.stderr)

# type : document ou programme
def loadFile(fileName) :

    type=""

    #time.sleep(3)
    try :
        type_mime = magic.from_file(fileName, mime=True)

    except FileNotFoundError:
        error(f"Erreur: le fichier {fileName} n'existe pas ou est illisible.")
        exit(1)

    print(type_mime)

    if type_mime=="application/pdf" :
        #type="txt/plain"
        print(f"Convert {fileName} to text...")
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

    #if type == "" :
    #    type = type_mime

    print(f"Load {fileName} ({type_mime}) ...")
    #print(contenu)

    longName=os.path.expanduser(fileName)

    content=f"Pour cette requête uniquement tu ne répondras pas et tu n'afficheras rien à l'exception d'une la ligne : [[[{longName}]]]. Apprend simplement que toutes les lignes du {type} {longName} (qui devient le document courant) sont les suivantes :" +chr(10) + contenu
    config.conf['current_filename'] = longName

    llm.ai_user_request(content, llm.ai_user_request)


def whenQuit():
    print
    print("bye")
    exit(0)

def loop_stdin() :
    auto_question=""

    #print("type code : "+type(code))
    #code=code.split("\n")
    #highlighted_code = config.highlightBloc(code, config.highlightCode)
    #print("===")
    #print(highlighted_code)
    #print("===")

    while True:
        if auto_question == "" :
            prompt=f"\033[34m{config.conf['model']} {llm.provider.getContextWindow(config.conf['model'])}\033[0m [[[{config.conf['current_filename']}]]]"
            # Get user input from the console
            if sys.stdin.isatty():
                if config.conf["multi_lines"] == "True" or config.conf["multi_lines"] == True :
                    print(f"\n>>> ({prompt}) >>> Ctrl D pour terminer l'entrée, CTRL C pour quitter le programme")
                else :
                    print(f"\n>>> ({prompt}) >>>")

            try:
                if config.conf["multi_lines"] == "True" or config.conf["multi_lines"] == True:
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

        response=llm.ai_user_request(user_input, extend.ai_extend_request) 

        if response :
            # Save the last response to last_response.txt
            config.last_response=response.choices[0].message.content
            #with open("last_response.txt", "w") as f:
            #    f.write(response.choices[0].message.content)

            print("------------------------------------------")
            #print()
            lines=response.choices[0].message.content
            #print("type lines : "+type(lines))
            #print(lines)

            lines=lines.split("\n")
            lines_colored=""

            #styles = pygments.styles.get_all_styles()
            #for style in styles :
            #    config.conf['colors_style']=style
            #    lines_colored=lines_colored+config.highlightBloc([f"===STYLE: {style}\n"]+lines, config.highlightCode)

            lines_colored=config.highlightBloc(lines, config.highlightCode)


            #lines=config.highlightBloc('\n'.split(lines), config.highlightCode)
            #lines=config.highlightBloc(lines, config.highlightCode)
            #lines='\n'.split(lines)
            #print("END")

            #if config.conf["ansi"]==True :
                #lines=lines.replace(r"\033", chr(27))

            print(lines_colored)
            #print(lines)
            #print("...........................................")
            
            #print(response.choices[0].message.content)

            exec=1
            if exec == 1 :
                pattern = r"\$exec\('(.*)', *'(.*)'\)"
                matches = re.findall(pattern, config.last_response, re.DOTALL)

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


####################################################################

def main():

    if config.args.question:
        response=llm.ai_user_request(config.args.question)
        if response :
            print
            print(response.choices[0].message.content)
            exit(0)
        else :
            exit(1)
            
    cont=1
    while cont==1:
        try:
            loop_stdin()
        except Exception as e:
            print(f"Erreur : {e}")
            traceback.print_exc()
            cont=0

    
# Main

config.args=config.parseArgs()

#print(f"args: {config.args}")

if config.args.help:
        config.parser.print_help()
        exit()

if config.args.system :
    config.conf["system"]=config.args.system
  
if config.args.question :
    print(json.dumps(config.args.question, indent=4, ensure_ascii=False))

if config.args.provider :
    config.conf["provider"]=config.args.provider
    
#print(config.args)

if config.args.system_file :
    cat=""
    for file in config.args.system_file.split(",") :
        with open(file, 'r') as f:
            cat=cat+"\n"+f.read()
    config.conf["system"]=cat


#v=vars(config.args)
#v=config.args

#print(config.args)
#print(config.conf)

#for a in ["system", "multi_lines", "model", "temperature", "seed", "length_history", "compress"] :
#    if v[a]!=None :
#        print(f"a: {a} {v[a]}")
#        #print(":",a, "=", v[a])
#        config.conf[a]=v[a]

#print("======", file=sys.stderr)
#config.context_window=config.getContextWindow(config.conf["model"])
#config.printToStderr()
#print("======", file=sys.stderr)
#print(f"context_window={config.context_window}", file=sys.stderr)
#print("======", file=sys.stderr)

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
    extend.load_conversation(file)


if config.args.multi_lines :
    config.conf["multi_lines"]=True
    
llm.initProvider(config.conf["provider"])


if config.args.file:
    for l in config.args.file:
        for file in l.split(",") :
            if file == "" :
                continue
            loadFile(file)

if __name__ == "__main__":
    main()
