import requests

link = "https://newsapi.org/v2/everything?"
params = {
    'apiKey': 'API KEY',
    'q': 'personal finance',
}
r = requests.get(link, params)
data = r.json()

print(data)
