import requests
from bs4 import BeautifulSoup

def soup():
    '''This is a reminder of how to use BeautifulSoup because I keep forgetting.'''
    req = requests.get('https://www.google.com')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    # example of using find_all by class
    links = soup.find_all('a', class_='some-class')
    first_link = links[0]
    # example of getting an attribute from an element
    first_link_url = first_link['href']
