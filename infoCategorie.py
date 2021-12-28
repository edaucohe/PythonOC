#### LIBRARIES ####
import requests
from bs4 import BeautifulSoup

#### CONSTANTS ####
page = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'


#### FUNCTIONS ####
## Récupérer le code html du site web ##
def fetch_html(url):
    # contenu = requests.get(url)
    # return contenu
    pass

# def liste_livres(html_contenu: str):
#     h3 = soup.find_all('h3')
#     titres_livres = []
#     for i in range(0, len(h3)):
#         titres_livres.append(h3[i].find_next('a')['title'])  # "h3" contient "a", dont l'attribut "title" va dans une liste vide
#
#     return titres_livres

# page = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'
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
    n = 1

    for i in range(0, len(h3)):
        titre.append(h3[i].find_next('a')['title'])  # "h3" contient "a", dont l'attribut "title" va dans une liste vide

    print(titre)
    pager = soup.findAll('li')
    # print(len(pager))

    pager = pager[len(pager) - 1].text
    print(pager)

    while pager == 'next':
        n += 1

        nouvelle_page = page.replace('index.html', 'page-' + str(n) + '.html')
        print(nouvelle_page)
        reponse = requests.get(nouvelle_page)
        soup = BeautifulSoup(reponse.text, "html.parser")
        h3 = soup.find_all('h3')
        # print(h3)
        # print(len(h3))

        for i in range(0, len(h3)):
            titre.append(h3[i].find_next('a')['title'])  # "h3" contient "a", dont l'attribut "title" va dans une liste vide

        pager = soup.findAll('li')
        pager = pager[len(pager) - 1].text
        print(pager)

    print("TITRES : ", titre)
    print("Nb de livres : ", len(titre))
    # if pager == 'next':
    #     print("Texte du next : ", pager)
    #     url = page.replace('index.html','page-' + str(2) + '.html')
    #     # url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/' + 'page-' + str(2)
    #     # page = 'http://books.toscrape.com/catalogue/category/books/mystery_3/page-2.html'
    #     print(url)

    # else:
    #     print("Il n'y a pas une deuxième page")

else:
    print("Il y a un problème de request")

#### MAIN FUNCTION ####
# def main():
#     reponse = fetch_html(url_livre)
#     print(reponse.text)
#
# if __name__ == '__main__':
#     main()