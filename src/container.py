
# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
#from tools import error as error  
def error(msg): tools.error(msg)
    
import subprocess
import tools

#import codecs

def exec_raw(user, contenu) :
    command=f"podman exec -u {user} ai bash -c '{contenu}'"

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

def exec(user, contenu) :
    # Crée le fichier /tmp/aaa/f.txt contenant la chaine "Super cool !"
    print("°°°°°°°°°°°°°°°°°°")
    print(contenu)
    print("°°°°°°°°°°°°°°°°°°")
    if tools.confirmation() :
        return exec_raw(user, contenu)
    else :
        return "Abandon !"
