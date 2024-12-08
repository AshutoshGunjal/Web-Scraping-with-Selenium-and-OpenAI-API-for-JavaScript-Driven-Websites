import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from IPython.display import Markdown, display
import openai

# Load environment variables in a file called .env
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Check the key
if not api_key: 
    print("No API key was found")
elif not api_key.startswith("sk-"):
    print("API Key was found, but it doesn't start with sk-: please check you're using the right key")
elif api_key.strip() != api_key:
    print("API key was found, but it looks like it might have a space or tab character at the start or end")
else:
    print("API key found and looks good so far!")

# Set OpenAI API Key
openai.api_key = api_key

# Selenium Setup
def setup_driver():
    options = Options()
    options.add_argument("--headless")  # Run browser in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("/Users/ashutoshgunjal/Downloads/chromedriver") # Use default ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# A class to represent a Webpage
class Website:
    url: str
    title: str
    text: str

    def __init__(self, url):
        """
        Create this website object from the given URL using Selenium and BeautifulSoup
        """
        self.url = url
        driver = setup_driver()
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            self.title = soup.title.string if soup.title else "No title found"
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        except Exception as e:
            print(f"Error loading URL {url}: {e}")
            self.title = "No title found"
            self.text = "No content found"
        finally:
            driver.quit()

# OpenAI Prompt and Summarization Functions
system_prompt = (
    "You are an assistant that analyzes the contents of a website "
    "and provides a short summary, ignoring text that might be navigation related. "
    "Respond in markdown."
)

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}.\n"
    user_prompt += (
        "The contents of this website are as follows; "
        "please provide a short summary of this website in markdown. "
        "If it includes news or announcements, then summarize these too.\n\n"
    )
    user_prompt += website.text
    return user_prompt

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)},
    ]

def summarize(url):
    website = Website(url)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages_for(website)
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error during summarization: {e}"

def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))

# Example Usage with OpenAI's Website
display_summary("https://openai.com")
