import os
import sys

import ollama
#from ollama import Client
from openai import OpenAI
from groq import Groq

# le module OpenAI permet d'utilser une API standard comprise à la fois
# par Groq et Ollama

import requests
import random
import config
import tools
import json

import traceback

def error(msg) :
    print(msg, file=sys.stderr)

provider=None

class Provider:
    def __init__(self):
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
        
    def getContextWindow(self, model):
        raise NotImplementedError("Cette méthode doit être implémentée par la classe fille")

    def chat(self, model, messages, seed, temperature):
        return self.client.chat.completions.create(model=model, messages=messages,
            #max_tokens=8000,
            seed=seed,
            temperature=temperature)

class GroqProvider(Provider):
    def __init__(self):
        super().__init__()
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/"
        self.initModels()
        self.initClient()
        
    def initModels(self) :
        url = self.url + "models"
        headers = { "Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json" }

        response = requests.get(url, headers=headers)
        self.models = response.json()
        
    def getContextWindow(self, model) :
        for m in self.models["data"] :
            if m["id"] == model :
                return m["context_window"]
        return None

    def initClient(self) :
        self.client = Groq(api_key=self.api_key)
    


class OllamaProvider(Provider):
    def __init__(self):
        super().__init__()
        self.api_key = None  # ou une autre valeur par défaut
        self.url = 'http://localhost:11434/v1/'  # url de Ollama par défaut
        self.initClient()

    def initClient(self):
        #self.client = ollama.Client()
        self.client = OpenAI(
            base_url = self.url,
            api_key='ollama', # required, but unused
            )
    def getContextWindow(self, model):
        #embeddings = self.client.embeddings(model=model, prompt="test")
        return None

    
def initProvider(p) :
    global provider
    
    if p == "groq" :
        provider=GroqProvider()
    elif p=="ollama" :
        provider=OllamaProvider()
    else :
        error("Provider non géré !")
        exit(1)
        
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

    responseMsg=response.choices[0].message.content

    filename=tools.extract_current_filename(responseMsg)

    if filename :
        print(f"current_filename from extract_current_filename : {filename}")
        config.conf['current_filename']=filename
        print(f"Set current_filename: {config.conf['current_filename']}")


    config.chat_history.append({"role": "assistant", "content": responseMsg})

    return response
