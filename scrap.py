from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, SoupStrainer
import re
import csv
import threading

# extract all the links in the div copy from the page
def ext_links(link):
    '''Generator to return  all links in the page
    input: string (link)
    output: Generator'''

    req = Request("https://www.urparts.com/{}".format(link), headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req).read()

    soup = BeautifulSoup(response, 'html.parser')
    divs = soup.find_all('div', {'class': 'copy'})
    links = [div.find_all('a') for div in divs]
    result = [i.attrs['href'] for i in links[0]]

    yield result

# extract all the anchor's text in the div copy from the page
def get_text(link):
    '''Generator to return  all anchor's text in the page
    input: string (link)
    output: Generator'''

    req = Request("https://www.urparts.com/{}".format(link), headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req).read()

    soup = BeautifulSoup(response, 'html.parser')
    divs = soup.find_all('div', {'class': 'copy'})
    links = [div.find_all('a') for div in divs]

    txt = [i.get_text() for i in links[0]]
    yield txt


def scrap_website():
    '''Scrap the website and wirte the data in csv file '''
    # use BeautifulSoup to read the web page
    req = Request("https://www.urparts.com/index.cfm/page/catalogue", headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(response, 'html.parser')
    # Get the copy class from the web page
    divs = soup.find_all('div', {'class': 'copy'})
    # Get all links in copy class
    links = [div.find_all('a') for div in divs]

    # Get all manufactures's link in the catalogue page
    manufactures = []
    for i in links[0]:
        manufactures.extend(next(ext_links(i.attrs['href'])))

    # Get all the category's link for each manufactures
    cat = []
    for i in manufactures:
        cat.extend(next(ext_links(i)))

    # Get the part and part_category for each category
    # Get manufacturer, category and model by convert the link to list and get the data from it
    part = (k.split('/')[3:] + p.split(' - ') for k in cat for p in next(get_text(k)) if ' - ' in p)

    with open('catalogue.csv', 'w') as file:
        writer = csv.writer(file)
        header = ["manufacturer", "category", "model", "part", "part_category"]
        writer.writerow(header)
        for i in part:
            writer.writerow(i)
            # writer.writerow(item)
    file.close()


if __name__ == '__main__':
    # scrap_website()
    t = threading.Thread(target=scrap_website)
    t.start()
