# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
#from tools import error as error  
def error(msg): tools.error(msg)


"""
Contraintes sur initSystem

Si -s est précisée ne rien faire

Si ni l'option -s, ni l'option -x ne sont pas précisées alors config.conf['system'] est initialisé avec la concaténation des fichiers précisés dans extend/basic.list

Si l'option -x est précisé alors config.conf['system'] est initialisé avec la concaténation des fichiers
précisés dans extend/extend.list

"""
def initSystem():

    if config.args.extend:
        # Si l'option -x est précisée, initialiser config.conf['system'] avec la concaténation des fichiers précisés dans extend/extend
        files = []
        print("Load system : extend/extend.list")
        with open("extend/extend/list", 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    files.append(line)
        content = ""
        for file in files:
            print(f"File : {file}")
            with open("extend/"+file, 'r') as f:
                content += f.read() + "\n"
        config.conf['system'] = content
    else:
        # Si ni l'option -s, ni l'option -x ne sont précisées, initialiser config.conf['system'] avec la concaténation des fichiers précisés dans extend/basic
        files = []
        print("Load system : extend/basic.list")
        with open("extend/basic.list", 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    files.append(line)
        content = ""
        for file in files:
            print(f"File : {file}")
            with open("extend/"+file, 'r') as f:
                content += f.read() + "\n"
        config.conf['system'] = content
