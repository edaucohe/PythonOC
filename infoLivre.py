#### LIBRARIES ####
import requests
from bs4 import BeautifulSoup
import csv
import sys
# import codecs

#### CONSTANTS ####
url_livre = 'http://books.toscrape.com/catalogue/i-had-a-nice-time-and-other-lies-how-to-find-love-sht-like-that_814/index.html'

#### FUNCTIONS ####
## Récupérer le code html du site web ##
def fetch_html(url):
    contenu = requests.get(url)
    return contenu

## Récupérer l'info du livre et le retourner comme un dictionnaire ##
def extract_book_info(html_contenu: str):
    if html_contenu.ok:
        print("Le request marche bien\n")
        soup = BeautifulSoup(html_contenu.text, "html.parser")

        ### titre du livre ###
        titre = soup.find('h1')
        titre = titre.text
        print("Titre: ", titre)

        ### UPC, Prix sans taxe, Prix avec taxe, disponibilité et Review ###
        td = soup.findAll(
            'td')  # UPC, les prix, la dispo et les reviews se trouvent dans les seuls "td" qu'il y a dans le code
        # print(td)
        upc = td[0].text
        prix_exc = td[2]
        prix_inc = td[3]
        dispo = td[5]
        review = td[6].text
        # print(type(dispo))
        prix_exc = prix_exc.text.replace('Â', '')
        prix_inc = prix_inc.text.replace('Â', '')
        dispo = dispo.text.replace('In stock (', '')  # Au début, dispo a un type : <class 'bs4.element.Tag'>
        dispo = dispo.replace(' available)',
                              '')  # Mais après avoir utilisé "replace", c'est du type <class 'str'>, c'est pour ça qu'il accepte pas .text

        # print(type(dispo))
        print("UPC : ", upc)
        print("Prix sans taxe : ", prix_exc)
        print("Prix avec taxe : ", prix_inc)
        print("Disponibilité : ", dispo + " livres")
        print("Reviews : ", review + " reviews")

        ### Description ###
        p = soup.find_all('p')
        description = p[3].text
        print("Description : ", description)

        ### Categorie ###
        a = soup.find_all('a')
        categorie = a[3].text
        print("Categorie : ", categorie)

        ### URL Image ###
        img = soup.find_all('img')
        image = img[0]
        image_url = image['src']  # Pour recuperer un attribut
        image_url = image_url.replace('../../', '')
        image_url = 'http://books.toscrape.com/' + image_url
        # URL = 'http://books.toscrape.com/'
        print("URL de l'image : ", image_url)

        info_livre = {
            'titre' : titre,
            'upc' : upc,
            'prix_exc' : prix_exc,
            'prix_inc' : prix_inc,
            'stock' : dispo,
            'review' : review,
            'description' : description,
            'categorie' : categorie,
            'image' : image_url
        }

        return info_livre

        # print(soup)

    else:
        print("Il y a un problème de request")

## Créer un fichier csv ##
# def csv():
#     with open('livre.csv', 'w', newline='') as csvfile:
#         livre.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
#         spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

#### MAIN FUNCTION ####

def main():
    reponse = fetch_html(url_livre)
    print(reponse.text)

    print(sys.getdefaultencoding())

    info = extract_book_info(reponse)
    print(info)
    # csv()
    # with open('egg.csv', 'w', newline='') as csvfile:
    #     spamwriter = csv.writer(csvfile, delimiter=' ',
    #                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     spamwriter.writerows(['Spam'] * 5 + ['Baked Beans'])
    #     spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    #
    # with open('names.csv', 'w', newline='') as csvfile:
    #     fieldnames = ['first_name', 'last_name']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #
    #     writer.writeheader()
    #     writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    #     writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    #     writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})



    with open('livre.csv', 'w', encoding = 'utf8', newline='') as csvfile:
        tetes = list(info.keys())
        print(tetes)
        donnes_livres = list(info.values())
        print(donnes_livres)

        writer = csv.DictWriter(csvfile, fieldnames=tetes)
        writer.writeheader()
        writer.writerow({tetes[0]:donnes_livres[0],tetes[1]:donnes_livres[1],tetes[2]:donnes_livres[2],tetes[3]:donnes_livres[3],tetes[4]:donnes_livres[4],tetes[5]:donnes_livres[5],tetes[6]:donnes_livres[6],tetes[7]:donnes_livres[7],tetes[8]:donnes_livres[8]})

if __name__ == '__main__':
    main()