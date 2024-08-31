# -*- coding: utf-8 -*-
# set tabstop=4

import os
dirname=os.path.dirname(__file__)
with open(f"{dirname}/imports", 'r') as f:
    exec(f.read())
#from tools import error as error
def error(msg): tools.error(msg)


# le module OpenAI permet d'utilser une API standard comprise à la fois
# par Groq et Ollama


provider=None

# Pour la couleur
cumul=""
context=[]


class FakeResponse:
    def __init__(self, choices):
        self.choices = choices

class Choice:
    def __init__(self, message):
        self.message = message

class Message:
    def __init__(self, content):
        self.content = content

class Provider():
    def __init__(self):
        super().__init__()
        self.model = ""
        self.models = {}
        self.client = None
        self.api_key = None
        self.url = None

    def list(self):
        url = self.url + "models"
        headers = { "Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json" }
        response = requests.get(url, headers=headers)
        data = response.json()
        print(json.dumps(data, indent=4))

    def setKey(self, key) :
        print(f"llm setKey : {key}")
        self.api_key=key
                
    def getContextWindow(self, model):
        raise NotImplementedError("Cette méthode doit être implémentée par la classe fille")

    def chunk_to_ANSI(text) :
        
        regexp = r"\033\[(\d+)(;\d+)*m"

        if re.search(regexp, texte):
            print("Le texte contient des codes ANSI")
        else:
            print("Le texte ne contient pas de codes ANSI")

    def chat(self, model, messages, seed, temperature):
        global markdownLexer, formatter
        global cumul, context
        #print(f"Provider client : {self.client}")
        #stream=False
        streamConf=config.conf['stream']
        #stream=False
        #max_tokens=8000,
        tools.verbose(f"CHAT QUESTION")
        print("Sending...");
        #print(f"CHAT QUESTION: {json.dumps(messages,indent=4, ensure_ascii=False)}")
        #print("START")

        report=None
        
        try :
            report=self.client.chat.completions.create(
                model=model,
                messages=messages,
                seed=seed,
                temperature=temperature,
                stream=streamConf)
            #print(f"CHAT RESPONSE: {json.dumps(response.to_dict(),indent=4, ensure_ascii=False)}")
            #print(f"CHAT RESPONSE: {response}")

            #print(f"REPORT : {report}")
        except Exception as e:
            config.last_chunk=report
            traceback.print_exc()
            raise e
            #return
            
        if streamConf : # stream == True
            response=""
            cumul=''
            context=[]
            for chunk in report:
                #print(f"CHUNK: {chunk.choices[0].delta.content}")
                config.last_chunk=chunk
                if chunk.choices[0].delta.content == None:
                    #conf.last_chunk=chunk;
                    #print()
                    #print(chunk)
                    #config.last_chunk=chunk
                    #print("BREAK")
                    #config.last_chunk=response
                    break

                response=response + f"{chunk.choices[0].delta.content}"
                #print('\n', end='')
                #stream.collectAndPrint(chunk.choices[0].delta.content)
                #print(colors.add_chunk(chunk.choices[0].delta.content), end='')
                #, llm.markdownLexer, llm.formatter

                print(add_chunk(chunk.choices[0].delta.content), end='')

                #code=pygments.highlight(chunk.choices[0].delta.content, llm.markdownLexer, llm.formatter)
                #print(code, end='')


                #print(json.dumps(add_chunk(chunk.choices[0].delta.content), indent=4, ensure_ascii=False), end='')
                #time.sleep(0.1)

            # To flush last line
            print(add_chunk('\n'), end='')
            
            #print('\n', end='')    
            #stream.collectAndPrint("\n")    
            #print("\n")
            response=FakeResponse([Choice(Message(f"{response}"+'\n'))])
            #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            #print(response.choices[0].message.content)
            
        else : # stream == False
            config.last_chunk=report
            response=report
            #print(colors.add_chunk(response.choices[0].message.content), end='')
            code=pygments.highlight(response.choices[0].message.content, llm.markdownLexer, llm.formatter)
            print(code, end='')
            #print(response.choices[0].message.content)
            
        return response
        
    def initModels(self) :
        pass
        
class GroqProvider(Provider):
    def __init__(self):
        super().__init__()
        #self.api_key = os.environ.get("GROQ_API_KEY")
        
        self.url = "https://api.groq.com/openai/v1/"
        self.initModels()
        #self.initClient()

    def setKey(self, key) :
        self.api_key = key
        #self.api_key = keys.getKey(key)
        #print(f"GroqProvider : key : {self.api_key}")
        
    def initModels(self) :
        #print(f"llm groq initModels (key :{self.api_key})")
        url = self.url + "models"
        headers = { "Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json" }

        response = requests.get(url, headers=headers)
        self.models = response.json()
        
    def getContextWindow(self, model) :
        #print(self.models)
        try :
            for m in self.models["data"] :
                if m["id"] == model :
                    return m["context_window"]
        except :
            return 4096
        return None

    def initClient(self) :
        #print(f"Groq initClient")
        #print(f"Groq initClient {self.api_key}")
        self.client = Groq(api_key=self.api_key)
        #print(f"Groq client {self.client}")
    


class OllamaProvider(Provider):
    def __init__(self, provider):
        super().__init__()
        self.provider = provider
        ollama="ollama"
        host="localhost"
        port="11434"
        try :
            ollama,host,port = provider.split(':')
        except :
            pass
            #error(f"Bad specification: {provider}")

        
        print(f"ollama: {ollama} host: {host} port: {port}")
        keys.addKeys('None')
        #self.api_key = None  # ou une autre valeur par défaut
        url=f'http://{host}:{port}/v1/'
        print(url)
        self.url = url  # url de Ollama par défaut
        #self.initClient()

    def initClient(self):
       
        #self.client = ollama.Client()
        self.client = OpenAI(
            base_url = self.url,
            api_key='ollama', # required, but unused
            )
            
    def getContextWindow(self, model):
        #embeddings = self.client.embeddings(model=model, prompt="test")
        #curl http://localhost:11434/api/show -d '{
        #  "name": "llama3"
        #  }'
        return 4096

def ai_user_request(user_input, ai_extend_request=None) :
    global provider

    if user_input.startswith("$") and ai_extend_request :
        user_input = ai_extend_request(user_input, provider.client, config.chat_history)
        print("ext : "+user_input)

    if user_input == "" :
        return ""

    config.chat_history.append({"role": "user", "content": user_input}) 
    
    if config.conf["seed"] :
        seed=config.conf["seed "]
    else :
        seed = random.randint(0, 1000000)
    try:
        response = provider.chat(model=config.conf["model"], 
            messages=[{"role" : "system", "content":  config.conf["system"]}]+config.chat_history,
            seed=seed,
            temperature=config.conf["temperature"])
    except Exception as e:
        traceback.print_exc()
        print("Erreur lors de la génération de la réponse : ", str(e))
        response = None
        return None

    #print(f"+++ dict response :")
    #print(f"dict : {response.__dict__}") #if config.conf['verbose'] else None


    #print("+++++++++++++")
    #choice_label = response.choices[0].message.content #.label
    #print(json.dumps({'choice': choice_label}))
    #print(json.dumps(response.__dict__))
    #print("+++++++++++++")

    #print(json.dumps(response.__dict__, indent=4, ensure_ascii=False))
    responseMsg=response.choices[0].message.content

    #print(f"DEBUG ai_user_request : Set current_filename: {config.conf['current_filename']}")
    #print(f"DEBUG ai_user_request : responseMsg: {responseMsg}")
    filename=tools.extract_current_filename(responseMsg)

    if filename :
        config.conf['current_filename']=filename
        #print(f"DEBUG ai_user_request : Set current_filename: {config.conf['current_filename']}")


    config.chat_history.append({"role": "assistant", "content": responseMsg})
    command.save_conversation()
    return response
    
def initProvider(p) :
    global provider, markdownLexer, formatter

    #print(f"provider: {p}")
    if p.startswith("groq") :
        provider=GroqProvider()
    elif  p.startswith("ollama") :
        provider=OllamaProvider(p)
    else :
        error("Provider non géré !")
        exit(1)
    #print(f"provider: {provider}")
    #print(f"provider: {provider.__dict__}") if config.conf['debug'] else None
    #content=provider.__dict__
    # Bad print(json.dumps(content, indent=4, ensure_ascii=False))
    # bad print(json.dumps(provider.to_dict(), indent=4, ensure_ascii=False))
    # bad print(json.dumps(dataclasses.asdict(provider), indent=4, ensure_ascii=False))
        
    keys.loadKeys()
    #print(f"initProvider setKey : {keys.keysConf}")
    provider.setKey(keys.keysConf['keys'][keys.keysConf['key']])
    provider.initClient()
    provider.initModels()

    markdownLexer = MarkdownLexer(stripnl=True)
    if config.conf['background'] == "dark" :
        formatter = Terminal256Formatter(fg='dark', bg='light', style=config.conf['colors_style'])
    else :
        formatter = Terminal256Formatter(fg='light', bg='dark', style=config.conf['colors_style'])

def add_chunk(chunk):
    global cumul, context

    cumul += chunk
    resultats = []
    
    lines = cumul.split('\n')
    
    for line in lines[:-1] :
        
        context.append(line+'\n')
        n=100
        if len(context) > n :
            context=context[:-n]
        #print(f"N CONTEXT: {len(context)}")
        code=pygments.highlight(''.join(context+["```\n"]), llm.markdownLexer, llm.formatter).split('\n')
        #print(f"N CODE: {len(code)}")
        #print("CODE:")
        #print('\n'.join(code))
        try :
            line=code[-3]
        except :
            line=""
        #print(f"LINE : {line}")
        resultats.append(line+'\n')

    cumul=lines[-1]

    # Remplace les code ANSI
    # ...
    
    return ''.join(resultats)
