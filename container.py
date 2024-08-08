# -*- coding: utf-8 -*-
# set tabstop=4

import subprocess
#import codecs

def confirmation():
    reponse = input("Exécuter ? [Yn] ")
    return reponse.strip().upper() in ["Y", "O", ""]

def exec_raw(user, contenu) :
    command=f"podman exec -u {user} ai bash -c '{contenu}'"
    #print(f"command : {command}")
    #subprocess.run(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #process.wait()
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

def exec(user, contenu) :
    # Crée le fichier /tmp/aaa/f.txt contenant la chaine "Super cool !"
    print("°°°°°°°°°°°°°°°°°°")
    print(contenu)
    print("°°°°°°°°°°°°°°°°°°")
    if confirmation() :
        return exec_raw(user, contenu)
    else :
        return "Abandon !"
