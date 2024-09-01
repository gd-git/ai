# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
#from tools import error as error
def error(msg): tools.error(msg)
def warning(msg): tools.warning(msg)

def verbose(msg) :
    tools.verbose(msg)
    
def extraire_lignes(chaine):
    lignes = []
    for ligne in chaine.split('\n'):
        if ligne.strip().startswith('$') :
            lignes.append(ligne.strip())
    return lignes


def system_raw(contenu) :

    #contenu=contenu.lstrip("(")
    #contenu=contenu.lstrip(")")

    #print("SYSTEM_RAW ################# ...")

    command=contenu
    

    command=f"bash -c '"+command+"'"
    #print(f"EXECUTION CMD RAW: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout, stderr = process.communicate()

    #stdout = codecs.iconv('utf-8', stdout, 'utf-8').decode('utf-8')

    msg=f"""
## commande
{contenu}
## code de retour
{process.returncode} 
## stdout
{stdout.decode('utf-8',errors='ignore')}
## stderr
{stderr.decode('utf-8')}
    """
    #print(msg)

    return msg

def auto_report(cmd) :
    if config.last_error != "" :
        msg=f"""
## commande
{cmd}
## code de retour
1
## stdout
## stderr
{config.last_error}
"""
    else :
        msg=f"""
## commande
{cmd}
## code de retour
0 
## stdout
## stderr
"""
    return msg

# Retourne un tuple (auto_question, user_question)
# response

def analyse_response(auto_question, user_input) :
    auto=False
    if auto_question != "" :
        auto=True

    verbose(f"Analyse de la réponse auto: {auto}  auto_question: {auto_question}  user_input {user_input}")

    #if auto_question == "" and user_input == "" and auto == True :
    #    print("RETURN empty (but auto)")
    #    return("", === auto_q")
    
    resp=config.last_response
    #print(config.last_response)
    
    cmds=extraire_lignes(resp)
    #print(f"cmds: {cmds}")

    if len(cmds) == 0 :
        verbose("RETURN len(cmds) == 0 : aucune commande")
        return ("", "")
    elif len(cmds) > 1 :
        # Trop de demandes
        
        error("Trop de demandes d'exécution dans la réponse ! Corrige !")
        print(cmds)
        report=auto_report("")
        verbose("RETURN len(cmds) >1 0 : trop de demandes. Corrige !")
        return (report, "")

    #if auto == True :
        # Juste un auto_report à faire
    if 1 == 0 :
        pass   
    else :
        cmd=cmds[0]

        if "$file" in cmd :

            cmd=cmd.replace("$file ", "")

            #print(f"cmd: {cmd}")
            
            if tools.confirmation(cmd) :
                config.last_error=""
                cmd=f"command.command_file(\"$file {cmd}\")"
                print(f"cmd: {cmd}")
                eval(cmd)
                rapport = auto_report(cmd)
                #print("AUTO REPORT")
                verbose("RETURN $file report")
                return (rapport, "")
                
                #auto_question="Rapport d'écécution : $rapport"
                #config.user_input = ""
                
            else :
                auto_question="Rapport d'éxécution : Abandon !"
                user_input = ""
                verbose("RETURN Rapport d'éxécution : Abandon !")
                #return(auto_question, user_input)
                return("", "")
                
        elif "$system" in cmd :

            #command=f"{cmd}"
            #print(f"CMD RAW: {command}")

            #match=re.match('^ *$system\((.*)\)$', command)

            match=re.search("^.*\$system\([\" '](.*)[\" ']\)$", cmd)
            
            #print(f"MATCH : {match}")

            if not match :
                error("invalide system_raw !")
                
                report=auto_report
                verbose("RETURN $system invalide system_raw")
                verbose(report)
                
            command=match.group(1)
            
            print(f"CMD EXTRACT: {command}")
            
            #tools.red("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            tools.red(command)
            #tools.red("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            
            if tools.confirmation(command) :
                #print(f"CMD: {cmd} command: {command}")
                rapport=system_raw(command)

                #print(f"#RAPPORT: {rapport}")

                auto_question=rapport
                user_input = ""
                verbose("RETURN after system_raw")
                return(auto_question, user_input)
            else :
            
                auto_question="Rapport d'éxécution : Abandon !"
                user_input = ""
                verbose("RETURN Rapport d'éxécution : Abandon !")
                return(auto_question, user_input)
                
    verbose("RETURN default (empty)!") 
    return ("", "")  # Ajouter un retour par défaut       
                
                
            
        


                
