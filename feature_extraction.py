import requests
from bs4 import BeautifulSoup
import whois
import re

# Dataset generation function
def generate_dataset(url):

# initialize the dataset list
    dataset = [0] * 30



# convert the url in to standard format    
    if not re.match(r"https?",url):
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

# get all the domain information about the url    
    try:
        whois_respo = whois.whois(url)
        #print(whois_respo)
        domain = whois_respo.domain_name
        #print(domain)
        list_ckeck = isinstance(domain,list)
        if(list_ckeck==True):
            domain = domain[1].lower()
            print(domain)
    except:
        whois_respo = ""
        domain = ""


