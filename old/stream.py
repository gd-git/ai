# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
#from tools import error as error
def error(msg): tools.error(msg)

collected = ""
buf=""
in_code = False
near_in_code = False
lang = None
lexer=None
formatter=None
need_endl=False
context=[]
#TrueColor

def createFormatter() :
    if config.conf['background'] == "dark" :
        formatter = Terminal256Formatter(fg='dark', bg='light', style=config.conf['colors_style']) #, stripnl=False, hl_lines=[1])
    else :
        formatter = Terminal256Formatter(fg='light', bg='dark', style=config.conf['colors_style']) #, stripnl=False, hl_lines=[1])
    return formatter


def toColor(line, lang) :
    global lexer, formatter
    global collected
    global context

    #print(f"line: {line}")
    
    #context+=line

    context+=[line]

    if lexer :
        if line != "\n" :
            #print(f"lexer : {context}")
            result = pygments.highlight('\n'.join(context), lexer, formatter) 
            
            result = re.split('\n',result)
            result = result[-2:-1] 
            line=result[0]+'\n'
            #print(line, end='')
            print(pygments.highlight(line, llm.markdownLexer, llm.formatter))
    else :
        print(pygments.highlight(line, llm.markdownLexer, llm.formatter))
        #print(line, end='')
        

    n=1000
    if len(context) > n :
        context=context[:-n]
    

# Pour tous les chunks de la réponse
 
def collectAndPrint(chunk):
    global collected, in_code, near_in_code, lang
    global lexer, formatter, markdownLexer
    global buf
    global need_endl
    global context

    buf+=chunk
    #print(f"!!! chunk : {c} ({len(chunk_buf)})")

    while buf != "" :

        # start=extract first part
        lines=buf.split('\n')
        start=lines[0]
        if '\n' in buf :
            start+='\n'
        else :
            buf=""
            
        if len(lines) > 1 :
            buf='\n'.join(lines[1:])

        if len(start.lstrip()) < 4 and '\n' not in start :
            buf=start+buf
            return

        #print(f"=== buf: {buf} start: {start}")
            
        if in_code:
            #print(f"=== in_code :{chunk}")

            # fin de in_code
            #if start.startswith("```") or start.startswith(" ```"):
            
            if re.match(r'^ *```', start) :
                in_code=False
                #print(start, end='')
                print(pygments.highlight(start, llm.markdownLexer, llm.formatter), end='')
                context=[]
                return
            
            if start.endswith('\n') :
                toColor(start, lang)
            else :
                buf=start+buf
                return

        else: # NOT in code
            #print(f"=== not in_code :{chunk}")
            
            #if start.startswith("```") or start.startswith(" ```"):
            if re.match(r'^ *```', start) or re.match(r'^ * #', start) :
                if '\n' not in start :
                    buf=start+buf
                    return
                else :
                    #print("FOUND ```")
                    match = re.match(r'^ *``` *([a-zA-Z0-9]+) *$', start)
                    if match :
                        lang = match.group(1)
                    else :
                        lang = ""

                    if lang != "" :
                        #print(f"CREATE LEXER {lang}")
                        context=[]
                        lexer = get_lexer_by_name(lang)
                        formatter=createFormatter()
                    else :
                        context=[]
                        lexer = MarkdownLexer(stripnl=False)
                        formatter=createFormatter()
                        
                    in_code=True
                    #print(start, end='')
                    print(pygments.highlight(start, llm.markdownLexer, llm.formatter), end='')
                    continue
            else : # NOT in_code AND NOT re.match(r'^ *```', start)

                
                #print(start, end='')

                if start[-1] == '\n' :
                    #print("&")
                    #print(pygments.highlight(start, llm.markdownLexer, llm.formatter), end='')
                    colored=pygments.highlight(start, llm.markdownLexer, llm.formatter)
                    print(colored, end='')
                else :
                    colored=pygments.highlight(start, llm.markdownLexer, llm.formatter)
                    print(colored[:-1], end='')
                    
                sys.stdout.flush()
  
