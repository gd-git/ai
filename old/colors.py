# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
#from tools import error as error  
def error(msg): tools.error(msg)

def add_chunk(chunk):

    # Variable locales static
    
    # Cumule les chunks jusqu'à atteindre une ligne complète
    if not hasattr(add_chunk, 'cumul'):
        add_chunk.cumul = ''

    if not hasattr(add_chunk, 'context'):
        add_chunk.context = ''

    print(f"CHUNK: {chunk}")

    add_chunk.cumul += chunk
    resultats = []
    
    



