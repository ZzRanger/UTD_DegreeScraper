from ast import parse
import bs4
import requests
from bs4 import BeautifulSoup
import json

page = requests.get(
    "https://catalog.utdallas.edu/2021/undergraduate/programs/ah/visual-and-performing-arts-dance")

soup = BeautifulSoup(page.content, "html.parser")

# List of all relevant html elements
content: "list[bs4.element.Tag]" = list(
    x.get('href') for x in soup.find_all("a", href=True) if '/2021/undergraduate/programs/' in x.get('href'))
json_str = json.dumps(content)

with open("urls" + '.json', 'w') as outfile:
    outfile.write(json_str)
