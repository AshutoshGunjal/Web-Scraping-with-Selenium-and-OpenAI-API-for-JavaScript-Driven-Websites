import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import ollama

#Constants
OLLAMA_API="http://localhost:11434/api/chat"
HEADERS={"Content-Type": "application.json"}
MODEL="llama3.2"

# Create a message list using the same format that we used for OpenAI
messages = [
    {"role": "user",
     "content": "Describe some of the business applications of Gen AI"}
]

payload = {
    "model": MODEL,
    "messages": messages,
    "stream": False
}

response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
print(response.json()['message']['content'])

print("######### Printing response from Ollama #########")

response = ollama.chat(model=MODEL, messages=messages)
print(response['message']['content'])

