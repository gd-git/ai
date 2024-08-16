import re
import magic
import os

import config
import llm


def extract_current_filename(chaine):
    motif = r'\[\[\[([^{]*?)\]\]\]'
    correspondance = re.search(motif, chaine)
    if correspondance:
        return correspondance.group(1)
    return None

def extract_code_OLD(contents):
    start_tag = '^```'
    end_tag = '^```'

    lines = contents.splitlines()
    start_line = None
    end_line = None

    for i, line in enumerate(lines):
        if re.match(start_tag, line):
            if start_line is None:
                start_line = i + 1
            else:
                end_line = i
                break

    if start_line is not None and end_line is not None:
        code='\n'.join(lines[start_line:end_line])
        if not code.endswith("\n"):
            code += "\n"
        return code
    else:
        return ""
        
def extract_code(contents):
    lines = contents.splitlines()
    code = []
    in_code = False

    for line in lines:
        if line.strip().startswith('```'):
            in_code = not in_code
        elif in_code:
            code.append(line)

    if not code.endswith("\n"):
        code.append("\n")

    return '\n'.join(code)


def loadFile(fileName) :

    type=""

    try :
        type_mime = magic.from_file(fileName, mime=True)

    except FileNotFoundError:
        error(f"Erreur: le fichier {fileName} n'existe pas ou est illisible.")
        exit(1)

    if type_mime=="application/pdf" :
        print(f"Convert {fileName} to text...")
        contenu = subprocess.run(f"pdftotext -layout {fileName} -", shell=True, capture_output=True, text=True,
                                 universal_newlines=True).stdout
        
    else :
        with open(fileName, 'r') as fichier:
            contenu = fichier.read()

    print(f"Load {fileName} ({type_mime}) ...")
    #print(contenu)

    longName=os.path.expanduser(fileName)

    content=f"Pour cette requête uniquement tu ne répondras pas et tu n'afficheras rien à l'exception d'une la ligne : [[[{longName}]]]. Apprend simplement que toutes les lignes du {type} {longName} (qui devient le document courant) sont les suivantes :" +chr(10) + contenu
    config.conf['current_filename'] = longName

    llm.ai_user_request(content, llm.ai_user_request)
