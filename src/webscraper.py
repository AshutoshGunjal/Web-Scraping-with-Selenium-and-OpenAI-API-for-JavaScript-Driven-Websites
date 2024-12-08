import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import openai

# Load environment variables in a file called .env

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Check the key

if not api_key: 
    print("No API key was found")
elif not api_key.startswith("sk-proj-"):
    print("API Key was found, but it doesn;t start with sk-proj-: please check you're using the right key")
elif api_key.strip() != api_key:
    print("API key was found, but it looks like it might have space or tab character at the start or end")
else:
    print("API key found and looks good so far!")

OPENAI_API_KEY = openai

# A class to represent a Webpage

class Website:
    url: str
    title: str
    text: str

    def __init__(self, url):
        """
        Create this website object from the given url using Beautifulsoap library
        """
        self.url = url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

site = Website("https://edwarddonner.com")
print(site.title)
print(site.text)

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

system_prompt

# A function that writes a User promt that asks for summaries of websites:
def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt

print(user_prompt_for(site))

# To see how this function creates exactly the format above

def messages_for(website):
    return [
        { "role": "system", "content": system_prompt},
        { "role": "user", "content": user_prompt_for(website)}
    ]

messages_for(site)

def summarize(url):
    website = Website(url)
    response = openai.ChatCompletion.create (
        model = "gpt-4",
        messages = messages_for(website)
    )
    return response.choices[0].message["content"]

summarize("https://edwarddonner.com")

def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))

display_summary("https://edwarddonner.com")
