import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple
import csv

def fetch_html(url: str) -> BeautifulSoup:
    '''
    Récupérer le code html de la page web et s'assurer que la requete http est OK
    '''
    contenu = requests.get(url)
    if contenu.ok:
        contenu_texte = BeautifulSoup(contenu.text, "html.parser")
        return contenu_texte
    else:
        # Si on arrive pas à recuperer la page, on arrete le script en erreur
        raise Exception(f'Il y a un problème de request pour la page url={url}, reponse={contenu.status_code}')


def recuperer_donnees_livres(html_page_url: str) -> Dict[str, str]:
    '''
    Récupérer l'info demandée des livres
    '''
    soup = fetch_html(html_page_url)

    titre = soup.find('h1')
    titre = titre.text
    print("Titre: ", titre)

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

    p = soup.find_all('p')
    description = p[3].text

    a = soup.find_all('a')
    categorie = a[3].text

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


def recuperer_liste_categories(html_page: BeautifulSoup) -> List[Tuple[str, str]]:
    '''
    Récupérer les liens et les titres de chaque catégorie
    '''
    list_html_categories = html_page.find('aside').find_next('li').find_all('li')
    index_categorie = 'http://books.toscrape.com/catalogue/category/'
    information_categories = []

    for nb_elements in range(0, len(list_html_categories)):
        titre = list_html_categories[nb_elements].find_next('a').text.replace(' ', '').replace('\n', '')
        racine = index_categorie + list_html_categories[nb_elements].find_next('a')['href'].replace('../', '').replace('index.html', '')
        information_categories.append((titre, racine))

    return information_categories

def recuperer_url_page_suivante(html_page: str, nb_de_pages: int) -> str:
    '''
    S'il y a une page suivante dans une catégorie, récupérer ce lien
    '''
    nouvelle_page = []
    if nb_de_pages == 0:
        nouvelle_page = html_page + 'index.html'

    else:
        for nb_page in range(nb_de_pages):
            nouvelle_page.append(html_page + ('page-' + str(nb_page+1) + '.html'))

    return nouvelle_page

def recuperer_nb_page_suivantes(html_page: str) -> int:
    '''
    Savoir le nombre de pages suivantes d'une catégorie et récupérer ce numéro
    '''
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

def recuperer_livres_par_categorie(html_page: str) -> List[str]:
    '''
    Récupérer les liens des livres d'une page d'une catégorie
    '''
    contenu_html = fetch_html(html_page)
    list_html_livres = contenu_html.find_all('h3')

    index_livres = 'http://books.toscrape.com/catalogue/'
    racine_livres = []

    for nb_elements in range(0, len(list_html_livres)):
        racine_livres.append(index_livres + list_html_livres[nb_elements].find_next('a')['href'].replace('../../../', ''))

    return racine_livres

def recuperer_urls_livres_par_categorie(lien_page: str) -> List[str]:
    '''
    Récupérer les liens des livres de toutes les pages d'une catégorie
    '''
    nombre_pages_par_categorie = recuperer_nb_page_suivantes(lien_page)
    urls_pages_suivantes = recuperer_url_page_suivante(lien_page, nombre_pages_par_categorie)

    livres_par_categorie = []
    for url_page_suivante in urls_pages_suivantes:
        if nombre_pages_par_categorie == 0:
            livres_par_categorie = recuperer_livres_par_categorie(urls_pages_suivantes)
            break
        else:
            livres_par_categorie.extend(recuperer_livres_par_categorie(url_page_suivante))

    return livres_par_categorie

def info_livres(lien_page: str) -> Dict[str, List[Dict[str, str]]]:
    '''
    Obtenir l'info de tous les livres de toutes les catégories en format de dictionnaire
    '''
    contenu_html_index: BeautifulSoup = fetch_html(lien_page)

    informations_categories: List[Tuple[str, str]] = recuperer_liste_categories(contenu_html_index)
    print('informations des categories : ', informations_categories)

    info_livres_des_categories = {}

    for titre_categorie, lien_categorie in informations_categories:
        urls_livres_par_categorie = recuperer_urls_livres_par_categorie(lien_categorie)
        print('nb de livres de la categorie : ', len(urls_livres_par_categorie))
        print('liens complets des livres par categorie : ', urls_livres_par_categorie)

        info_livres = []

        for url_livre_par_categorie in urls_livres_par_categorie:
            donnes_du_livre = recuperer_donnees_livres(url_livre_par_categorie)
            info_livres.append(donnes_du_livre)

        info_livres_des_categories[titre_categorie] = info_livres

        print('info des livres de toutes les categories : ', info_livres_des_categories)

    return info_livres_des_categories

def main():
    url_index = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
    info_livres_par_categorie = info_livres(url_index)

    for categorie, info_livres_de_la_categorie in info_livres_par_categorie.items():
        '''
        Création des fichiers CSV par catégorie
        '''
        nom_du_fichier = 'data/fichiers-csv/' + categorie + '.csv'
        with open(nom_du_fichier, 'w', encoding='utf8', newline='') as csvfile:
            tetes = list(info_livres_de_la_categorie[0].keys())
            writer = csv.DictWriter(csvfile, fieldnames=tetes)
            writer.writeheader()
            for nb_livre in range(len(info_livres_de_la_categorie)):
                writer.writerow(info_livres_de_la_categorie[nb_livre])

        '''
        Téléchargement des images de chaque livre et nommées selon l'upc 
        '''
        for nb_livre in range(len(info_livres_de_la_categorie)):
            info_d_un_livre = info_livres_par_categorie[categorie][nb_livre]
            nom_de_l_image = 'data/images/' + info_d_un_livre['upc'] + '.jpg'
            reponse = requests.get(info_d_un_livre['image'])

            with open(nom_de_l_image, 'wb') as img_file:
                img_file.write(reponse.content)

if __name__ == '__main__':
    main()
