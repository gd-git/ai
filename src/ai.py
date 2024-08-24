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

    ctx_num_byte=llm.provider.getContextWindow(config.conf['model'])
    ctx_num=tools.taille_en_octets_humaine(ctx_num_byte)

    size_color=Fore.YELLOW
    if hist_size_bytes > 10*1024 or hist_size_bytes*100/ctx_num_byte > 80 :
        size_color=Fore.RED

    if config.conf['background']=="dark" :
        FORE=f"{Fore.LIGHTWHITE_EX}"
        BACK=f"{Back.BLACK}"
    else :
        FORE=f"{Fore.BLACK}"
        BACK=f"{Back.LIGHTWHITE_EX}"
    
    prompt = (
        BACK + FORE + config.conf['provider'] + " "
        + Fore.LIGHTBLUE_EX + config.conf['model'] + " "
        + size_color + str(hist_size)+"/"+str(ctx_num) + " "
        + FORE + "[" + config.conf['current_filename'] + "] "
        + FORE + "stream:" + str(config.conf['stream']) + ", "
        
    )
    
    if sys.stdin.isatty():
        if config.conf["multi_lines"] == "True" or config.conf["multi_lines"] == True :
            print(f">>> {prompt} >>> Ctrl D pour terminer l'entrée")
        else :
            print(f">>> {prompt} >>>")

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
    sys.stdout.flush()

    user_input = user_input.replace('$$', config.conf['current_filename'])
    response=llm.ai_user_request(user_input, command.ai_extend_request) 
    user_input=""
    
    if response :            
        config.last_response=response.choices[0].message.content
        if config.conf['stream'] == False :
           
            #lines=response.choices[0].message.content

            #lines=lines.split("\n")
            lines_colored=""
            #lines_colored=colors.scanForBlocs(lines)
            
            #print(lines_colored)
            #print(config.last_response)
            #print(pygments.highlight(config.last_response, llm.markdownLexer, llm.formatter))

            

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
