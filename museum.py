import requests
from bs4 import BeautifulSoup

categories = [
    "collezioni-etnografiche",
    "preistoria",
    "antiquarium",
    "archeologia-marina",
    "collezioni-egizie",
    "collezioni-etrusche",
    "collezioni-longobarde",
    "lapidario",
    "acquarium",
    "musei-di-geologia-italiani",
    "malacologia",
    "mineralogia",
    "paleontologia",
    "zoologia",
]

for category in categories:
    print("Starting category:", category)
    museums = []
    prefix = "https://www.museionline.info/musei/"
    page = 1
    while True:
        link = prefix + category + "/" + str(page) 
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', class_='el-item')
        if not cards:
            break
        for card in cards:
            museums.append(card.find('a')['href'])
        page += 1
    
    with open("museum.txt", "a", encoding="utf-8") as file:
            file.write("\n#" * 20 + "\n")
            file.write(f"Category: {category}\n")
            file.write("#" * 20 + "\n")

    prefix = "https://www.museionline.info"        
    for museum in museums:
        link = prefix + museum
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('h1').text.strip()
        data = soup.find_all('div', class_='uk-h6 uk-margin-small', recursive=True)[-3:]
        description = []
            
        for line in data:
            description.append(line.text.strip())
        
        with open("museum.txt", "a", encoding="utf-8") as file:
            file.write(f"Name: {name}\n")
            file.write(f"Description: {description}\n")
            file.write("-" * 20 + "\n")