# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
#from tools import error as error  
def error(msg): tools.error(msg)
    
def system_raw(contenu) :
    command=f"bash -c '{contenu}'"

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
    print(msg)

    return msg

def system(contenu) :
    print("°°°°°°°°°°°°°°°°°°")
    print(contenu)
    print("°°°°°°°°°°°°°°°°°°")
    if tools.confirmation(contenu) :
        return system_raw(contenu)
    else :
        return "Abandon !"


def write_raw(contenu) :
    command.command_write(contenu)
    
def write(contenu) :    
    print("°°°°°°°°°°°°°°°°°°")
    print(contenu)
    print("°°°°°°°°°°°°°°°°°°")
    if tools.confirmation(contenu) :
        return write_raw(contenu)
    else :
        return "Abandon !"
