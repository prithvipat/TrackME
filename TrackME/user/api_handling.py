import requests
import random
import json

def get_api():
    page = random.randint(1, 5) # Total of 5 pages
    link = "https://newsapi.org/v2/everything?"
    params = {
    'apiKey': 'b2b40e6d388a4263bf8a15ad481c724e',
    'q': '"personal finance" OR "budgeting" OR "saving money"',
    'page': page
    }

    r = requests.get(link, params)
    data = r.json()
    return data

def send_data():
    data = get_api()
    article=[]
    organized_data = {}
    current_data = {}

    for i in range(24):
        ran = random.randint(0, 95)
        if ran not in article:
            article.append(ran)
        
        else: i -= 1
    
    for i in article:
        name = data['articles'][article[i]]['source']['title']
        print(name)
        description = data['articles'][article[i]]['description']
        print(description)
        title = data['articles'][article[i]]['title']
        author = data['articles'][article[i]]['author']
        link = data['articles'][article[i]]['url']
        current_data = {
            'name': name,
            'description': description,
            'author': author,
            'title': title,
            'link': link,
        }
        organized_data += current_data

        print(organized_data)


send_data()






"""
link = "https://newsapi.org/v2/everything?"
params = {
    'apiKey': 'the key',
    'q': '"personal finance" OR "budgeting" OR "saving money"', # Keyword or phrase
    'page': page # Page number (random)
}

data['articles'][number/index][author,title,description] The actual article
data['articles'][number/index]['source']['name'] To get the article name


ex.

"status": "ok",
"totalResults": 657,
"articles": [
{
    "source": {
        "id": "the-verge",
        "name": "The Verge"
    },
    "author": "Jay Peters",
    "title": "Epic has a plan for the rest of the decade",
    "description": blah blah blah
}

"""

