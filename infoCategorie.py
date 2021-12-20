import requests
from bs4 import BeautifulSoup

page = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'
reponse = requests.get(page)

if reponse.ok:
    print("Le request marche bien\n")
    soup = BeautifulSoup(reponse.text, "html.parser")

    print(soup)


else:
    print("Il y a un problème de request")