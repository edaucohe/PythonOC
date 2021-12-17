import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/i-had-a-nice-time-and-other-lies-how-to-find-love-sht-like-that_814/index.html'
reponse = requests.get(url)

def fetch_html(url):
    pass

def extract_book_info(html_content: str):
    pass

extract_book_info(1)

if reponse.ok:
    print("Le request marche bien\n")
    soup = BeautifulSoup(reponse.text, "html.parser")
    soup.find
    ### titre du livre ###
    titre = soup.find('h1')
    print("Titre: ",titre.string)

    ### UPC, Prix sans taxe, Prix avec taxe, disponibilité et Review ###
    td = soup.findAll('td') # UPC, les prix, la dispo et les reviews se trouvent dans les seuls "td" qu'il y a dans le code
    # print(td)
    upc = td[0]
    prixExc = td[2]
    prixInc = td[3]
    dispo = td[5]
    review = td[6]
    # print(type(dispo))
    prixExc = prixExc.text.replace('Â','')
    prixInc = prixInc.text.replace('Â', '')
    dispo = dispo.text.replace('In stock (','') # Au début, dispo a un type : <class 'bs4.element.Tag'>
    dispo = dispo.replace(' available)','') # Mais après avoir utilisé "replace", c'est du type <class 'str'>, c'est pour ça qu'il accepte pas .text

    # print(type(dispo))
    print("UPC : ", upc.string)
    print("Prix sans taxe : ", prixExc)
    print("Prix avec taxe : ", prixInc)
    print("Disponibilité : ", dispo + " livres")
    print("Reviews : ", review.string + " reviews")

    ### Description ###
    p = soup.find_all('p')
    description = p[3]
    print("Description : ", description.string)

    ### Categorie ###
    a = soup.find_all('a')
    categorie = a[3]
    print("Categorie : ", categorie.string)

    ### URL Image ###
    img = soup.find_all('img')
    image = img[0]
    image_url = image['src'] # Pour recuperer un attribut
    image_url = image_url.replace('../../', '')
    # print("image : ",img)
    # print("image : ",image_url)
    # image = str(image)
    # print("image : ",image)

    # for i in range(len(image)):
    #     if image[i:i+5] == "media":
    #         # print("valor de media encontrado en :", i)
    #         src = image[i:len(image)-3]
    #         break
    #
    URL = 'http://books.toscrape.com/'
    print("URL de l'image : ", URL + image_url)

    # print(soup)

else:
    print("Il y a un problème de request")