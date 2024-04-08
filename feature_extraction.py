import requests
from bs4 import BeautifulSoup

# Dataset generation function
def generate_dataset(url):
    url = "http://" + url

# get and store the response of the inputed url
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        #print(soup)
    except:
        response = ""
        soup = -999
        #print(soup)

