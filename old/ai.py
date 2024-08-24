# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
#from tools import error as error
def error(msg): tools.error(msg)

def whenQuit():
    print("$quit to quit !")
    #print("bye")
    #exit(0)

def request(question) :
    print("request...")
        
def get_stdin() :
    
    user_input=""
    hist_bytes = tools.taille_en_octets_humaine(config.chat_history)
    
    prompt = (
        f"{config.conf['provider']} "
        f"\033[34m{config.conf['model']} "
        f"{llm.provider.getContextWindow(config.conf['model'])}\033[0m "
        f"[{config.conf['current_filename']}] "
        f"stream:{config.conf['stream']}, "
        f"hist size: {hist_bytes}"
        )

    
    if sys.stdin.isatty():
        if config.conf["multi_lines"] == "True" or config.conf["multi_lines"] == True :
            print(f"\n>>> {prompt} >>> Ctrl D pour terminer l'entrée, CTRL C pour quitter le programme")
        else :
            print(f"\n>>> {prompt} >>>")

    try:
        if config.conf["multi_lines"] == "True" or config.conf["multi_lines"] == True:
            user_input = config.multiInput()
        else:
            try :
                #user_input =readline.input()
                user_input =input()
                
            except EOFError :
                return ""

    except (KeyboardInterrupt) :
        whenQuit()
        return ""
        
    
    return user_input
    
def one(auto_question, user_input) :

    config
    if auto_question == "" :
        if user_input == "" :
            user_input=get_stdin()
    else :
        user_input=auto_question
        auto_question=""
        
    if user_input == "":
        return

    print(f"Sending... (stream: {config.conf['stream']})")
    print("------------------------------------------")
    response=llm.ai_user_request(user_input, command.ai_extend_request) 
    user_input=""
    
    if response :            
        config.last_response=response.choices[0].message.content
        if config.conf['stream'] == False :
           
            lines=response.choices[0].message.content

            lines=lines.split("\n")
            lines_colored=""
            lines_colored=colors.scanForBlocs(lines)
            print(lines_colored)

        else :
            pass # mode stream
            
        exec=1
        if exec == 1 :
            pattern = r"\$exec\('(.*)', *'(.*)'\)"
            matches = re.findall(pattern, config.last_response, re.DOTALL)

            if matches:
                user = matches[0][0]
                contenu = matches[0][1]
                auto_question=container.exec(user, contenu)
                user_input = ""
                
        if 1 == 1 :
            
            pattern = r"^\$write\('(.*)'\)"
            matches = re.findall(pattern, config.last_response, re.DOTALL)

            if matches:
                print(f"*: {matches[0]}")
                cmd = "$write "+matches[0]
                
                auto_question=system.write(cmd)
                user_input = ""
            
            pattern = r"\$system\('(.*)'\)"
            matches = re.findall(pattern, config.last_response, re.DOTALL)

            if matches:
                cmd = matches[0]                
                auto_question=system.system(cmd)
                user_input = ""
                

def loop_question() :
    for question in config.args.question:
        question_str = ' '.join(question)
        
        one("", question_str)

    exit(0)

def loop_stdin() :
    auto_question=""
    user_input=""
    while True:
        one(auto_question, user_input)



####################################################################

def main():

    config.init()
    
    
    try:
        if config.args.question:
            loop_question()
        else:
            loop_stdin()
    except Exception as e:
        #print(f"Erreur : {e}")
        #error(e.__str__())
        traceback.print_exc()


if __name__ == "__main__":
    main()
