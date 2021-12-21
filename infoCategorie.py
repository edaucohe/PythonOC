import requests
from bs4 import BeautifulSoup

page = 'http://books.toscrape.com/catalogue/category/books/mystery_3/page-1.html'
reponse = requests.get(page)

if reponse.ok:
    print("Le request marche bien\n")
    soup = BeautifulSoup(reponse.text, "html.parser")

    print(soup)

    ###  titre des livres dans une liste  ###
    h3 = soup.find_all('h3')
    # print(h3)
    # print(len(h3))
    titre = []

    for i in range(0, len(h3)):
        titre.append(h3[i].find_next('a')['title'])  # "h3" contient "a", dont l'attribut "title" va dans une liste vide

    print(titre)
    pager = soup.findAll('li')
    print(len(pager))

    pager = pager[len(pager) - 1].text
    if pager == 'next':
        print("Texte du next : ", pager)

    else:
        print("Il n'y a pas une deuxième page")

else:
    print("Il y a un problème de request")

