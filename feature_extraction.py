import requests
from bs4 import BeautifulSoup
import whois
import re
import time

def having_ip_address(domain):
    print("")


def url_length(url):
    print("")

# Dataset generation function
def generate_dataset(url):

    # initialize the dataset list
    dataset = [0] * 30


# convert the url in to standard format
    if not re.match(r"https?", url):
        url = "http://" + url

# get and store the response of the inputed url
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
    except:
        response = ""
        soup = -999
        # print(soup)

# get all the domain information about the url
    try:
        whois_respo = whois.whois(url)
        # print(whois_respo)
        domain = whois_respo.domain_name
        # print(domain)
        list_ckeck = isinstance(domain, list)
        if (list_ckeck == True):
            domain = domain[1].lower()
            print(domain)
    except:
        whois_respo = ""
        domain = ""

# calculate the starting time of dataset creation
    start = time.time()

    dataset[0] = having_ip_address(domain)
    dataset[1] = url_length(url)
    dataset[2] =
    dataset[3] =
    dataset[4] =
    dataset[5] =
    dataset[6] =
    dataset[7] =
    dataset[8] =
    dataset[9] =
    dataset[10] =
    dataset[11] =
    dataset[12] =
    dataset[13] =
    dataset[14] =
    dataset[15] =
    dataset[16] =
    dataset[17] =
    dataset[18] =
    dataset[19] =
    dataset[20] =
    dataset[21] =
    dataset[22] =
    dataset[23] =
    dataset[24] =
    dataset[25] =
    dataset[26] =
    dataset[27] =
    dataset[28] =
    dataset[29] =

# calculate the ending time of dataset creation
    end = time.time()
