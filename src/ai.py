# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
#from tools import error as error
def error(msg): tools.error(msg)
def warning(msg): tools.warning(msg)

level=0
        
def whenQuit():
    #print("$quit to quit !")

    warning("    *******************")
    warning("    * $quit to quit ! *")
    warning("    *******************")
    #print("bye")
    #exit(0)

def request(question) :
    print("request...")

def multiInput() :
    lines=[]
    while True :
        try :
            #line=readline.input()
            line=input()
            #line=readline.readline()
            #readline.add_history(line)
            
        except EOFError :
            break

        if line=="" :
            print("")
            
        lines.append(line)


    return '\n'.join(lines).replace(chr(10),'\\n')
           
def get_stdin() :
    
    user_input=""
    hist_size_bytes = sys.getsizeof(json.dumps(config.chat_history))
    hist_size = tools.taille_en_octets_humaine(hist_size_bytes)

    try :
        ctx_num_byte=llm.provider.getContextWindow(config.conf['model'])
        ctx_num=tools.taille_en_octets_humaine(ctx_num_byte)
    except Exception as e:
        traceback.print_exc()
        #print(f"Erreur : {e}")

        exit(1)

    max_size=50*1024; # max before red
    size_color=Fore.GREEN
    if hist_size_bytes > max_size or hist_size_bytes*100/ctx_num_byte > 80 :
        # beep ?
        tools.beep()
        size_color=Fore.RED

    if config.conf['background']=="dark" :
        FORE=f"{Fore.LIGHTWHITE_EX}"
        BACK=f"{Back.BLACK}"
    else :
        FORE=f"{Fore.BLACK}"
        BACK=f"{Back.LIGHTWHITE_EX}"
    
    prompt = (
        '\n>>> '
        +BACK + FORE 
        + FORE + "stream :" + str(config.conf['stream']) + ", "
        + FORE + "extend :" + str(config.conf['extend']) + ", "
        + FORE + "multi_lines :" + str(config.conf['multi_lines'])+" "
        +'\n>>> '
        + config.conf['provider'] + " "
        + Fore.LIGHTBLUE_EX + config.conf['model'] + " "
        + FORE + config.conf['conversation'] + " "
        + size_color + str(hist_size)+"/"+str(ctx_num) + " "
        + FORE + "[" + config.conf['current_filename'] + "] "
        + Style.RESET_ALL
    )

    #print(f"+++ stdout flush config.conf['current_filename']: {config.conf['current_filename']}")
    #sys.stdout.flush()
    if sys.stdin.isatty():
        if config.conf["multi_lines"] == "True" or config.conf["multi_lines"] == True :
            print(f">>> {prompt} >>> Ctrl D")
        else :
            print(f">>> {prompt} >>>")

    #print("+++ stdout flush")
    #sys.stdout.flush()

    print(Style.RESET_ALL, end='')
    #reset_all()

    try:
        if config.conf["multi_lines"] == "True" or config.conf["multi_lines"] == True:
            user_input = multiInput()
        else:
            try :
                
                user_input = input()
                
                
            except EOFError :
                return ""

    except (KeyboardInterrupt) :
        whenQuit()
        return ""
        
    return user_input


def one(auto_question, user_input) :
    global level
    
    #print(f"Sending... (stream: {config.conf['stream']})")
    #print("------------------------------------------")
    #sys.stdout.flush()

    #input("Press Enter")
    

    tools.verbose(f"+++ one [{level}] : auto_question: {auto_question} user_input: {user_input}")
    #config


    
    if auto_question == "" :
        if user_input == "" :
            tools.verbose(f"+++ one:get_stdin() because questions is empty")
            user_input=get_stdin()
    else :
        tools.verbose(f"+++ auto_question")
        user_input=auto_question
        auto_question=""
        
    if user_input == "":
        tools.verbose("+++ Leave one (because user_input empy)")
        return

    
    
    if not user_input:
        user_input=""
        
    user_input = user_input.replace('$$', config.conf['current_filename'])
    
    resp=llm.ai_user_request(user_input, command.ai_extend_request) 
    
    if resp :            
        config.last_response=resp.choices[0].message.content
        
        (auto_question, user_input) = response.analyse_response(auto_question, user_input)
        
        tools.verbose(f"=== After analyse : auto_question: {auto_question} user_input: {user_input}" )
        if auto_question != "" :
            level+=1
            one(auto_question, user_input)
            level-=1
"""
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
"""                

def loop_question() :
    global level
    
    for question in config.args.question:
        question_str = ' '.join(question)
        level+=1
        one("", question_str)
        level-=1
    exit(0)

def loop_stdin() :
    global level
    
    auto_question=""
    user_input=""
    while True:
        level+=1
        one(auto_question, user_input)
        level-=1



####################################################################

def main():
    #conf.audio
    # init colorama
    #init(autoreset=True)
        
    config.init()
    command.initCommand()
    readline.set_completer_delims(' \t\n;') 
    readline.set_completer(command.complete_command)
    readline.parse_and_bind("tab: complete")
    
    
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
