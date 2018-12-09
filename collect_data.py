import threading
import requests
from bs4 import BeautifulSoup
import re

def thread_find_links(nr_listing_page):
    """
    This function is collecting all interesting links from the given url.
    Input: the number of the listing page (Integer Type)
    Output: list with collected links
    """
    content = requests.get("https://www.immobiliare.it/vendita-case/roma/?criterio=rilevanza&pag="+str(nr_listing_page))
    soup = BeautifulSoup(content.text, 'html.parser')
    #find all links
    for link in soup.find_all('a', href=True):
        url = link['href']
        if url.startswith('https://www.immobiliare.it/') and url.endswith('.html'):
            link_threads.append(url)
    return

def scrap_data(soup):
    """
    This function is retrieving data about :
            price, locali, superficie, bagni, piano, description.
    Input: The Beautiful Soup object.
    Output: The dictionary object with integer values.
    """
    # find the html tag with the whole description
    tag_description = soup.findAll("div", {"id": "description"})
    # preprocess the description text
    description = tag_description[0].text.replace('\n', '').strip().split("            ")[-2]
    description = description.replace(",", "")
    # find the html tag with price
    price = soup.find_all('li',class_='features__price')[0].get_text()
    # extract and preprocess string to get price
    price = price.replace("€", "").replace(" ", "").replace(".", "")
    # find the html tag with the info about: locali, superficie, bagni, piano
    data = soup.find_all('ul','list-inline list-piped features__list')[0].get_text()
    # preprocess string and find numbers for: locali, superficie, bagni, piano
    data = data.replace('m2','')
    data = re.compile('\d+(?:\.\d+)?').findall(data)
    # if found all numbers:
    if len(data)==4:
        # output strcture -> [price, locali, superficie, bagni, piano, description]
        return [int(price), int(data[0]), int(data[1]), int(data[2]), int(data[3]), description]
