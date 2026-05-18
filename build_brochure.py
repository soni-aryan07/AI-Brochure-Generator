import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display, update_display
import requests
from bs4 import BeautifulSoup
import json

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key[:5]:
    print('OpenAI API key found!')
else: 
    print('No API key was fouund')

openai = OpenAI()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_content(url):
    '''Fetch the content of the website and truncate
    it to 2000 characters'''
    
    #print(f"Fetching the content of the website at {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevance in soup(['script', 'style', 'img', 'input']):
            irrelevance.decompose()
        text = soup.body.get_text(separator='\n', strip=True)

    else:
        text = ""

    return (title + "\n\n" +text)[:2_000]

def fetch_website_links(url):
    '''Fetch all the links on the webpage at this given url'''

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get('href') for link in soup.find_all('a')]
    result = [link for link in links if link]

    return result

links_system_prompt = """
You are a helpful assistant and your task is to decide which links could be related to the company which we can include 
in the brochure about the company at this given url.
For example: the links can be to the About page, or Jobs/Careers page, or Company's page.
And i repeat, take this as just an example and select other links which could be useful as well.
You should answer in the json object as follows:
{
    "links": [
        {"type": "about page", 'url': "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""

def get_links_user_prompt(url):
    user_prompt = f"Here is the website {url}:\
    Decide which links could be useful to create the\
    brochure about the company. Reply in the Json format with full https url\
    and do not include links such as terms of services, Privacy, email links\
    \
    Links[Some might be useful or relative]"

    links = fetch_website_links(url)
    user_prompt += '\n'.join(links)

    return user_prompt

def get_relevant_links(url):
    print(f"Selelting relevant links for {url}")
    response = openai.chat.completions.create(
        model="gpt-5-mini",
        messages= [
            {'role': 'system', 'content':links_system_prompt},
            {'role': 'user', 'content': get_links_user_prompt(url)}
            ],
            response_format={"type": "json_object"}
            )
    
    result = response.choices[0].message.content
    links = json.loads(result)
    print(f"Found {len(links['links'])} relevant links")
    return links

def fetch_page_and_links(url):
    content = fetch_website_content(url)
    relevant_links = get_relevant_links(url)

    result = F"## Landing Page!: \n\n{content}\nRelevant Links:\n"
    for link in relevant_links['links']:
        result += f"\n\n### Link Type: {link['type']}\n"
        result += fetch_website_content(link['url'])

    return result

brochure_system_promt = """
You are a helpful assistant and you are provided with the information about a 
company and the contents of all its relevant links. You are tasked to use this information
and create a brief brochure about this company.
Respond in Markdown without codeblocks.
You can include company's culture, customers, and jobs/careers if you have the information.
"""

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"""
You are looking at a company called {company_name}: 
Here are the contents of its landing page and all of its
relevant links and pages. Use this informartion to build a
short brochure about the company.
Be a little attentive here and respond in Markdown without codeblocks.\n\n
"""
    user_prompt += fetch_page_and_links(url)

    return user_prompt[:5_000]

def build_brochure(company_name, url):
    response = openai.chat.completions.create(
        model= 'gpt-5-mini',
        messages= [
            {'role': 'system', 'content': brochure_system_promt},
            {'role':'user', 'content': get_brochure_user_prompt(company_name, url)}
        ]
    )
    result = response.choices[0].message.content
    display(Markdown(result))

def stream_brochure(company_name, url):
    stream = openai.chat.completions.create(
        model= 'gpt-5-mini',
        messages= [
            {'role': 'system', 'content': brochure_system_promt},
            {'role':'user', 'content': get_brochure_user_prompt(company_name, url)}
        ],
        stream=True
    )
    for chunk in stream:
        text = chunk.choices[0].delta.content or ""
        sys.stdout.write(text)
        sys.stdout.flush()

    print()

stream_brochure("Vercel", "https://vercel.com")
