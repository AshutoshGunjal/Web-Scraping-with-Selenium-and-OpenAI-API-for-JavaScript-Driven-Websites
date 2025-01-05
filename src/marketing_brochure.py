"""
Creating a product that builds a marketing brochure for a
company to be used for prospective clients, investors and
potential recruits.

We will provide a company name and their primary website.

"""
import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
import openai

# Initialize and constants

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key) > 10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key!!")

MODEL = 'gpt-4o-mini'
# Set OpenAI API Key
openai.api_key = api_key

# A class to represent a Webpage

class website:
    """
    A utility class to represent a Website that we have scraped, now with links
    """

    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.body = response.content
        soup = BeautifulSoup(self.body, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        if soup.body:
            for irrelavant in soup.body(["script", "style", "img", "input"]):
                 irrelavant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""
        links = [link.get('href') for link in soup.find_all('a')]
        self.links = [link for link in links if link]

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"
        
site = website("https://edwarddonner.com")
# print(site.get_contents())
print(site.links)
        
"""
FIRST STEP: Have GPT-4o-mini figure out which links are relevant
Using a call to gpt-4o-mini to read the links on a webpage, and respond in structured json
"""

link_system_prompt = "You are provided witha list of links found on a webpage. \
    You are able to decide which of the links would be most relavant to include in a brochure about the company. \
    such as links to an About page, or a Company page, or Careers/Jobs pages \n"
link_system_prompt += "Youd should respond in JSON as in this example:"
link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""
print (link_system_prompt)

def get_links_user_prompt(website):
    user_prompt = f"Here is the links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links:\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += json.dumps(website.links, indent=2) # convert links to JSON format
    return user_prompt

print(get_links_user_prompt(site))

def get_links(url):
    web_site = website(url)
    response = openai.ChatCompletion.create(
        model = MODEL,
        messages = [
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(web_site)},
        ],
        response_format = {"type": "json_object"}
    )
    result = response.choices[0].message['content']
    return json.loads(result)

anthropic = website("https://anthropic.com")
print(anthropic.links)
print(get_links("https://anthropic.com"))

"""
SECOND STEP: Make The Brochure
"""

def get_all_details(url):
    result = "Landing Page:\n"
    result += website(url).get_contents()
    links = get_links(url)
    print("Found Links: ", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += website(link["url"]).get_contents()
    return result

print(get_all_details("https://anthropic.com"))

system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."

# Or uncomment the lines below for a more humorous brochure - this demonstrates how easy it is to incorporate 'tone':

# system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
# and creates a short humorous, entertaining, jokey brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
# Include details of company culture, customers and careers/jobs if you have the information."

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:20_000] # Truncate if more than 20,000 characters
    return user_prompt

print(get_brochure_user_prompt("Anthropic", "https://anthropic.com"))

def create_brochure(company_name, url):
    response = openai.ChatCompletion.create(
        model = MODEL,
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ],
    )
    result = response.choices[0].message['content']
    display(Markdown(result))

print(create_brochure("Anthropic", "https://anthropic.com"))