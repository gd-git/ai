from config import error as error

import os
import readline
import json
import subprocess
import sys
import time
import re
import traceback
import pygments

import llm
import extend
import config
import tools
import container

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


def whenQuit():
    print
    print("bye")
    exit(0)

def loop_stdin() :
    auto_question=""

    while True:
        if auto_question == "" :
            prompt=f"\033[34m{config.conf['model']} {llm.provider.getContextWindow(config.conf['model'])}\033[0m [[[{config.conf['current_filename']}]]]"

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
            print("------------------------------------------")
            config.last_response=response.choices[0].message.content
           
            lines=response.choices[0].message.content

            lines=lines.split("\n")
            
            lines_colored=""
            lines_colored=config.highlightBloc(lines, config.highlightCode)

            print(lines_colored)


            exec=1
            if exec == 1 :
                pattern = r"\$exec\('(.*)', *'(.*)'\)"
                matches = re.findall(pattern, config.last_response, re.DOTALL)

                if matches:
                    user = matches[0][0]
                    contenu = matches[0][1]
                    auto_question=container.exec(user, contenu)
        if not sys.stdin.isatty():
            break


####################################################################

def main():
    
    config.loadRc()

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
                tools.loadFile(file)

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

    


if __name__ == "__main__":
    main()
