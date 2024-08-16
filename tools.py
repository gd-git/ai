import re
import config

def extract_current_filename(chaine):
    motif = r'\[\[\[([^{]*?)\]\]\]'
    correspondance = re.search(motif, chaine)
    if correspondance:
        return correspondance.group(1)
    return None

def extract_code(contents):
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
