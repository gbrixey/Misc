import requests
from bs4 import BeautifulSoup

def soup():
    '''This is a reminder of how to use BeautifulSoup because I keep forgetting.'''
    req = requests.get('https://www.google.com')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    # example of using find_all by class
    spans = soup.find_all('span', class_='some-class')
    print(spans)
