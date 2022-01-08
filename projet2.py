import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple
import csv

tous_urls_categories = []

def fetch_html(url) -> str:
    '''
    Récupérer le code html de la page web et confirmer si requete http OK
    :param url: le contenu html
    :return: le contenu html en format texte
    '''
    contenu = requests.get(url)
    if contenu.ok:
        contenu_texte = BeautifulSoup(contenu.text, "html.parser")

    else:
        contenu_texte = ''
        print("Il y a un problème de request")

    return contenu_texte

def recuperer_donnees_livres(html_page: str): #->:
    soup = fetch_html(html_page)
    ### titre du livre ###
    titre = soup.find('h1')
    titre = titre.text
    print("Titre: ", titre)

    ### UPC, Prix sans taxe, Prix avec taxe, disponibilité et Review ###
    td = soup.findAll('td')

    upc = td[0].text
    prix_exc = td[2]
    prix_inc = td[3]
    dispo = td[5]
    review = td[6].text

    prix_exc = prix_exc.text.replace('Â', '')
    prix_inc = prix_inc.text.replace('Â', '')
    dispo = dispo.text.replace('In stock (', '')  # Au début, dispo a un type : <class 'bs4.element.Tag'>
    dispo = dispo.replace(' available)', '')  # Mais après avoir utilisé "replace", c'est du type <class 'str'>, c'est pour ça qu'il accepte pas .text

    ### Description ###
    p = soup.find_all('p')
    description = p[3].text


    ### Categorie ###
    a = soup.find_all('a')
    categorie = a[3].text


    ### URL Image ###
    img = soup.find_all('img')
    image = img[0]
    image_url = image['src']  # Pour recuperer un attribut
    image_url = image_url.replace('../../', '')
    image_url = 'http://books.toscrape.com/' + image_url

    info_livre = {
        'titre': titre,
        'upc': upc,
        'prix_exc': prix_exc,
        'prix_inc': prix_inc,
        'stock': dispo,
        'review': review,
        'description': description,
        'categorie': categorie,
        'image': image_url
    }

    return info_livre

def recuperer_liste_categories(html_page): # -> List[Tuple[str, str]]:
    list_html_categories = html_page.find('aside').find_next('li').find_all('li')

    index_categorie = 'http://books.toscrape.com/catalogue/category/'
    information_categories = []

    for nb_elements in range(0, len(list_html_categories)):
        '''
        Recuperer elements des categories
        '''
        titre = list_html_categories[nb_elements].find_next('a').text.replace(' ', '').replace('\n', '')
        racine = index_categorie + list_html_categories[nb_elements].find_next('a')['href'].replace('../', '').replace('index.html', '')
        information_categories.append((titre, racine))

    return information_categories


def recuperer_url_page_suivante(html_page: str, nb_de_pages: int): #-> :
    nouvelle_page = []
    if nb_de_pages == 0:
        nouvelle_page = html_page + 'index.html'

    else:
        for nb_page in range(nb_de_pages):
            nouvelle_page.append(html_page + ('page-' + str(nb_page+1) + '.html'))

    return nouvelle_page

def recuperer_nb_page_suivantes(html_page: str) -> int:
    contenu_html = fetch_html(html_page)
    pager = contenu_html.findAll('li')
    next = pager[len(pager) - 1]['class']
    if 'next' in next:
        nb_page = pager[len(pager) - 2].text
        nb_page = nb_page.replace('Page 1 of ', '').replace(' ', '').replace('/n', '')
        nb_page = int(nb_page)
    else:
        nb_page = 0

    return nb_page

def recuperer_livres_par_categorie(html_page: str) -> list[str]:
    contenu_html = fetch_html(html_page)
    list_html_livres = contenu_html.find_all('h3')

    index_livres = 'http://books.toscrape.com/catalogue/'

    racine_livres = []

    for nb_elements in range(0, len(list_html_livres)):
        '''
        Recuperer elements des livres
        '''
        racine_livres.append(index_livres + list_html_livres[nb_elements].find_next('a')['href'].replace('../../../', ''))

    return racine_livres

def info_par_categorie(html_page: str): #-> Tuple[List[Dict[str, str]], bool, str]:
    '''
    Entrée :
    - url de l'index d'une categorie

    Sorie :
    - Tous les livres d'une page d'une categorie
    - S'il y a une page suivante dans une categorie
    - L'url de la page suivante d'une categorie si c'est le cas

    :param html_page:
    :return: livres_par_categorie
    '''

    nombre_pages_par_categorie = recuperer_nb_page_suivantes(html_page)

    urls_pages_suivantes = recuperer_url_page_suivante(html_page, nombre_pages_par_categorie)
    print('\nurls des pages suivantes d une categorie : ', urls_pages_suivantes)

    livres_par_categorie = []
    for url_page_suivante in urls_pages_suivantes:
        if nombre_pages_par_categorie == 0:
            livres_par_categorie = recuperer_livres_par_categorie(urls_pages_suivantes)
            break
        else:
            livres_par_categorie.extend(recuperer_livres_par_categorie(url_page_suivante))

    return livres_par_categorie, nombre_pages_par_categorie

def recuperer_urls_livres_par_categorie(lien_page: str): #-> Tuple[List[Dict[str, str]], bool, str]:

    urls_livres_par_categorie, nombre_pages_par_categorie = info_par_categorie(lien_page)

    return urls_livres_par_categorie

def info_livres(lien_page: str) -> Dict[str, List[Dict[str, str]]]:
    contenu_html_index = fetch_html(lien_page)

    informations_categories: List[Tuple[str, str]] = recuperer_liste_categories(contenu_html_index)
    print('informations des categories : ', informations_categories)

    info_livres_par_categorie = {}

    for titre_categorie, lien_categorie in informations_categories[0:2]:
        urls_livres_par_categorie = recuperer_urls_livres_par_categorie(lien_categorie)
        print('nb de livres de la categorie : ', len(urls_livres_par_categorie))
        print('liens complets des livres par categorie : ', urls_livres_par_categorie)

        # info_livres_par_categorie = {}
        info_livres = []

        for url_livre_par_categorie in urls_livres_par_categorie:
            donnes_du_livre = recuperer_donnees_livres(url_livre_par_categorie)
            info_livres.append(donnes_du_livre)

            # nom_du_fichier = str(titres_categories[titre_de_la_liste]) + '.csv'
            # print('nom du fichier csv : ', nom_du_fichier)

            # with open(nom_du_fichier, 'w', encoding = 'utf8', newline='') as csvfile:
            #     tetes = list(donnes_du_livre.keys())
            #     print(tetes)
            #     donnes_livres_valeurs = list(donnes_du_livre.values())
            #     print(donnes_livres_valeurs)
            #
            #     writer = csv.DictWriter(csvfile, fieldnames=tetes)
            #     writer.writeheader()
            #     writer.writerow({tetes[0]:donnes_livres_valeurs[0],tetes[1]:donnes_livres_valeurs[1],tetes[2]:donnes_livres_valeurs[2],tetes[3]:donnes_livres_valeurs[3],tetes[4]:donnes_livres_valeurs[4],tetes[5]:donnes_livres_valeurs[5],tetes[6]:donnes_livres_valeurs[6],tetes[7]:donnes_livres_valeurs[7],tetes[8]:donnes_livres_valeurs[8]})
            #     # csvfile.write("\n")
            #     csvfile.write("{},{}".format(pose_x, pose_y))
            #     csvfile.write("\n")

            # titre_de_la_liste += 1

        # titre_de_la_liste += 1
        # print('nombre de livres par categorie (compte des elements de la liste de dictionnaires) : ', len(info_livres_par_categorie))
        # print('liste des donnees des livres d une categorie : ', info_livres_par_categorie)

        info_livres_par_categorie[titre_categorie] = info_livres


        print('nombre de livres par categorie (compte des elements de la liste de dictionnaires) : ', len(info_livres))
        print('liste des donnees des livres d une categorie : ', info_livres)

        print('info des livres par categorie : ', info_livres_par_categorie)

    return info_livres_par_categorie

# def recuperer_information_d_une_page_categorie(lien_vers_la_page: str) -> Tuple[List[Dict[str, str]], bool, str]:
#     contenu_html_d_une_page_categorie = fetch_html(lien_vers_la_page)
#
#     liens_vers_des_livres: List[str] = extraire_liste_de_livre_de_la_page(contenu_html_d_une_page_categorie)
#     info_des_livres_de_la_categorie = []
#     for lien_vers_un_livre in liens_vers_des_livres:
#         info_du_livre: Dict[str, str] = recuperer_information_d_un_livre(lien_vers_un_livre)
#         info_des_livres_de_la_categorie.append(info_du_livre)
#
#     lien_vers_la_page_suivante: bool = extraire_le_lien_vers_la_page_suivante(contenu_html_d_une_page_categorie)
#     a_une_page_suivante = lien_vers_la_page_suivante is not None
#
#     return info_des_livres_de_la_categorie, a_une_page_suivante, lien_vers_la_page_suivante
#
# def recuperer_informations_livres_d_une_categorie(lien_vers_la_page_index_d_une_category) -> List[Dict[str, str]]:
#     infos_des_livres_de_la_categorie, a_une_page_suivante, lien_vers_la_page_suivante = recuperer_information_d_une_page_categorie(lien_vers_la_page_index_d_une_category)
#
#     while a_une_page_suivante:
#         infos_des_livres_de_la_page_suivante_de_la_categorie, a_une_page_suivante, lien_vers_la_page_suivante = recuperer_information_d_une_page_categorie(lien_vers_la_page_suivante)
#         infos_des_livres_de_la_categorie += infos_des_livres_de_la_page_suivante_de_la_categorie
#
#     return infos_des_livres_de_la_categorie

def main():
    url_index = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
    info_livres_par_categorie = info_livres(url_index)

    # livre_test = info_livres_par_categorie['Travel'][0]
    # img_file_name = 'data/images/' + livre_test['upc'] + '.jpg'
    # resp = requests.get(livre_test['image'])

    # with open(img_file_name, 'wb') as img_file:
    #     img_file.write(resp.content)

    for categorie, info_livres_de_la_categorie in info_livres_par_categorie.items():
        # print('categorie : ', categorie)
        # print('info des livres : ', info_livres_de_la_categorie)
        # print('info des livres cles : ', list(info_livres_de_la_categorie[0].keys()))
        # print('info des livres values : ', info_livres_de_la_categorie[0])
        # do_stuff with categorie and livres:
        nom_du_fichier = categorie + '.csv'
        # print('nom du fichier : ', nom_du_fichier)
        with open(nom_du_fichier, 'w', encoding='utf8', newline='') as csvfile:
            tetes = list(info_livres_de_la_categorie[0].keys())
            writer = csv.DictWriter(csvfile, fieldnames=tetes)
            writer.writeheader()
            for nb_livre in range(len(info_livres_de_la_categorie)):
                writer.writerow(info_livres_de_la_categorie[nb_livre])



    # return info_livres_par_categorie

    # reponse = fetch_html(url_categorie)
    # info = extract_categorie_info(reponse)
    # print(info)

    # reponse = fetch_html(url_livre)
    # info = extract_book_info(reponse)
    # print(info)

    # for categorie, info_livres_de_la_categorie in infos.items():
    #    do stuff with categorie and livres
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
