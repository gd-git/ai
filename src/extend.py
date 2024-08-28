# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
#from tools import error as error  
def error(msg): tools.error(msg)

def load_files(list_file):
    dirname = os.environ.get('DIR_NAME')
    dirname=os.path.expanduser(dirname)
    rcname=os.path.expanduser("~/.ai/")
    
    def read_file(file):
        file=file.replace("//", "/")
        tools.verbose(f"readfile list: {file}")
        content = ""
        
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('%'):
                    #print(f"ACCEPT : {file} : {line}")
                    content += line + "\n"
                elif line and line.startswith('#'):
                    nop=1
                    #print(f"REJECT : {file} : {line}")
        return content

    list_file=list_file.replace("//", "/")
    tools.verbose(f"Load system : {list_file}")
    content = read_file(list_file)

    final_content = ""
    for file in content.splitlines():
        #tools.verbose(f"   file: {file}")
        filename =rcname+"/extend/"+file
        if not os.path.exists(filename) :
            filename=dirname+"/extend/"+file
            
        #print(f"File : {filename}")
        
        final_content += read_file(filename)

    return final_content

def initSystem():
    dirname = os.environ.get('DIR_NAME')
    dirname=os.path.expanduser(dirname)
    rcname=os.path.expanduser("~/.ai/")

    if config.conf['extend'] == True :
        list_file =rcname+"/extend/extend.list"
        if not os.path.exists(list_file):
            list_file = dirname+"/"+"extend/extend.list"
    else:
        list_file =rcname+"/extend/basic.list"
        if not os.path.exists(list_file):
            list_file = dirname+"/"+"extend/basic.list"

    config.conf['system'] = load_files(list_file)
