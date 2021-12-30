import requests
from bs4 import BeautifulSoup
from typing import Dict
import csv
import sys

tous_urls_categories = []

def fetch_html(url) -> str:
    '''
    Récupérer le code html de la page web et confirmer si requete http OK
    :param url: le contenu html
    :return: le contenu html en format texte
    '''
    contenu = requests.get(url)
    if contenu.ok:
        print("Le request marche bien\n")
        contenu_texte = BeautifulSoup(contenu.text, "html.parser")
        # print(soup)

    else:
        contenu_texte = ''
        print("Il y a un problème de request")

    return contenu_texte

def recuperer_elements(index: str, list_html: str) -> list[str]:
    '''
    Les éléments à récupérer sont "les liens", "leurs racines" et "les textes" des categories et des livres
    :param index:
    :param list_html:
    :return:
    '''
    # liens_elements = []
    titres_elements = []
    racine_elements = []

    for nb_elements in range(0, len(list_html)):
        if index == 'http://books.toscrape.com/catalogue/category/':
            '''
            Recuperer elements des categories
            '''
            # liens_elements.append(index + list_html[nb_elements].find_next('a')['href'].replace('../',''))
            racine_elements.append(index + list_html[nb_elements].find_next('a')['href'].replace('../', '').replace('index.html',''))
            titres_elements.append(list_html[nb_elements].find_next('a').text.replace(' ','').replace('\n',''))

        else:
            '''
            Recuperer elements des livres
            '''
            racine_elements.append(index + list_html[nb_elements].find_next('a')['href'].replace('../../../',''))
            titres_elements.append(list_html[nb_elements].find_next('a')['title'].replace('â\x80\x99',''))

    # return liens_elements
    return racine_elements, titres_elements

def recuperer_elements_categories(url_index: str) -> list[str]:
    retour = fetch_html(url_index)
    list_html_categories = retour.find('aside').find_next('li').find_all('li')

    index_principal = 'http://books.toscrape.com/catalogue/category/'
    racine_categories, titres_categories = recuperer_elements(index_principal, list_html_categories) # liens_categories
    # liens_categories
    return racine_categories, titres_categories

def recuperer_elements_livres(url_categories: list[str]) -> list[str]:
    retour = fetch_html(url_categories)
    list_html_livres = retour.find_all('h3')

    index_categories = 'http://books.toscrape.com/catalogue/'
    racine_livres, titres_livres  = recuperer_elements(index_categories, list_html_livres) # liens_livres

    print("nb des livres : ", len(titres_livres))
    # print(liens_livres)

    # return liens_livres
    return racine_livres, titres_livres

def nb_pages_categories(url_categories, nb_next) -> list[str]:
    global tous_urls_categories
    nouvelle_page = url_categories + ('page-' + str(nb_next) + '.html')
    tous_urls_categories.append(nouvelle_page)

    retour = fetch_html(nouvelle_page)
    # if 'pager' in retour:
    #     pager = retour.findAll('li')
    #     pager = pager[len(pager) - 1].text
    # else:
    #     pager = ''
    pager = retour.findAll('li')
    pager = pager[len(pager) - 1].text
    if pager == 'next':
        nb_next += 1
        nb_pages_categories(url_categories, nb_next)

    else:
        print('nb de next', nb_next)
        print('tous les urls d une categories : ', tous_urls_categories)

    return tous_urls_categories

def recuperer_infos_livres():
    pass

# def extract_categorie_info(soup):
#     '''
#     titre des livres dans une liste
#     :param soup:
#     :return:
#     '''
#
#     liste_livres, pager = enregistrer_livres(soup)
#
#     while pager == 'next':
#         global n
#         n += 1
#         nouvelle_page = url_categorie.replace('index.html', 'page-' + str(n) + '.html')
#         print(nouvelle_page)
#         reponse = fetch_html(nouvelle_page)
#         liste_livres, pager = enregistrer_livres(reponse)
#
#     print("TITRES : ", liste_livres)
#     print("Nb de livres : ", len(liste_livres))

# def enregistrer_livres(soup):
#     h3 = soup.find_all('h3')
#
#     for i in range(0, len(h3)):
#         titre.append(h3[i].find_next('a')['title'])  # "h3" contient "a", dont l'attribut "title" va dans une liste vide
#
#     print(titre)
#     pager = soup.findAll('li')
#     pager = pager[len(pager) - 1].text
#     print(pager)
#     return titre, pager


# def extract_book_info(soup: str):
#     '''
#     Récupérer l'info du livre et le retourner comme un dictionnaire
#     :param soup:
#     :return:
#     '''
#     # titre du livre #
#     titre = soup.find('h1')
#     titre = titre.text
#     print("Titre: ", titre)
#
#     # UPC, Prix sans taxe, Prix avec taxe, disponibilité et Review #
#     td = soup.findAll('td')  # UPC, les prix, la dispo et les reviews se trouvent dans les seuls "td" qu'il y a dans le code
#     # print(td)
#     upc = td[0].text
#     prix_exc = td[2]
#     prix_inc = td[3]
#     dispo = td[5]
#     review = td[6].text
#     # print(type(dispo))
#     prix_exc = prix_exc.text.replace('Â', '')
#     prix_inc = prix_inc.text.replace('Â', '')
#     dispo = dispo.text.replace('In stock (', '')  # Au début, dispo a un type : <class 'bs4.element.Tag'>
#     dispo = dispo.replace(' available)',
#                           '')  # Mais après avoir utilisé "replace", c'est du type <class 'str'>, c'est pour ça qu'il accepte pas .text
#
#     # print(type(dispo))
#     print("UPC : ", upc)
#     print("Prix sans taxe : ", prix_exc)
#     print("Prix avec taxe : ", prix_inc)
#     print("Disponibilité : ", dispo + " livres")
#     print("Reviews : ", review + " reviews")
#
#     # Description #
#     p = soup.find_all('p')
#     description = p[3].text
#     print("Description : ", description)
#
#     # Categorie #
#     a = soup.find_all('a')
#     categorie = a[3].text
#     print("Categorie : ", categorie)
#
#     # URL Image #
#     img = soup.find_all('img')
#     image = img[0]
#     image_url = image['src']  # Pour recuperer un attribut
#     image_url = image_url.replace('../../', '')
#     image_url = 'http://books.toscrape.com/' + image_url
#     # URL = 'http://books.toscrape.com/'
#     print("URL de l'image : ", image_url)
#
#     info_livre = {
#         'titre': titre,
#         'upc': upc,
#         'prix_exc': prix_exc,
#         'prix_inc': prix_inc,
#         'stock': dispo,
#         'review': review,
#         'description': description,
#         'categorie': categorie,
#         'image': image_url
#     }
#
#     return info_livre

def main():

    url_index = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
    # url_categorie = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'
    # url_livre = 'http://books.toscrape.com/catalogue/i-had-a-nice-time-and-other-lies-how-to-find-love-sht-like-that_814/index.html'

    racine_categories, titres_categories = recuperer_elements_categories(url_index) # urls_categories
    # print("liens des categories : ", urls_categories)
    print("titres des categories : ", titres_categories)
    print("racine des categories : ", racine_categories)

    nb = 1
    tous_les_urls_categories = nb_pages_categories(racine_categories[3], nb)
    urls_livres_tous = []
    titres_livres_tous = []

    for nb_categorie in range(len(tous_les_urls_categories)):
        print('iteration : ', nb_categorie)
        urls_livres, titres_livres = recuperer_elements_livres(tous_les_urls_categories[nb_categorie])
        urls_livres_tous.extend(urls_livres)
        titres_livres_tous.extend(titres_livres)

    # urls_livres, titres_livres = recuperer_elements_livres(tous_les_urls_categories)
    print("nb de pages : ", len(urls_livres_tous))
    print("liens des livres : ", urls_livres_tous)
    print("titres des livres : ", titres_livres_tous)
    print('numero de livres : ', len(titres_livres_tous))

    # reponse = fetch_html(url_categorie)
    # info = extract_categorie_info(reponse)
    # print(info)

    # reponse = fetch_html(url_livre)
    # info = extract_book_info(reponse)
    # print(info)
    #
    # with open('livre.csv', 'w', encoding = 'utf8', newline='') as csvfile:
    #     tetes = list(info.keys())
    #     print(tetes)
    #     donnes_livres = list(info.values())
    #     print(donnes_livres)
    #
    #     writer = csv.DictWriter(csvfile, fieldnames=tetes)
    #     writer.writeheader()
    #     writer.writerow({tetes[0]:donnes_livres[0],tetes[1]:donnes_livres[1],tetes[2]:donnes_livres[2],tetes[3]:donnes_livres[3],tetes[4]:donnes_livres[4],tetes[5]:donnes_livres[5],tetes[6]:donnes_livres[6],tetes[7]:donnes_livres[7],tetes[8]:donnes_livres[8]})

if __name__ == '__main__':
    main()