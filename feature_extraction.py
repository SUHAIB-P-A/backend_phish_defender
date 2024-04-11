import requests
from bs4 import BeautifulSoup
import whois
import re
import time

def having_ip_address(domain):
    print("")


def url_length(url):
    print("")


def shortening_service(url):
    print("")


def at_in_url(url):
    print("")


def double_slash_redirecting(url):
    print("")


def prefix_suffix(domain):
    print("")


def having_sub_domain(domain):
    print("")


def ssl_final_state(url):
    print("")


def domain_registration_length(whois_response):
    print("")


def favicon(url):
    print("")


def port(domain):
    print("")


def https_token(domain):
    print("")


def request_url(url, domain, soup):
    print("")


def url_of_anchor(url, domain, soup):
    print("")


def links_in_tags(url, domain, soup):
    print("")


def sfh(url):
    print("")


def check_submit_to_email(response):
    print("")


def abnormal_url(url):
    print("")


def web_forwarding(response):
    print("")


def on_mouseover(response):
    print("")


def right_click(response):
    print("")


def popup_window(response):
    print("")


def iframe(response):
    print("")


def age_of_domain(whois_response):
    print("")


def check_dns_record(url):
    print("")


def website_traffic(url):
    print("")


def page_rank(domain):
    print("")


def google_index(url):
    print("")


def links_pointing_to_page(response):
    print("")


def statistical_report(domain):
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
    dataset[2] = shortening_service(domain)
    dataset[3] = at_in_url(url)
    dataset[4] = double_slash_redirecting(url)
    dataset[5] = prefix_suffix(domain)
    dataset[6] = having_sub_domain(domain)
    dataset[7] = ssl_final_state(url)
    dataset[8] = domain_registration_length(whois_respo)
    dataset[9] = favicon(url)
    dataset[10] = port(domain)
    dataset[11] = https_token(domain)
    dataset[12] = request_url(url,domain,soup)
    dataset[13] = url_of_anchor(url,domain,soup)
    dataset[14] = links_in_tags(url,domain,soup)
    dataset[15] = sfh(url)
    dataset[16] = check_submit_to_email(response)
    dataset[17] = abnormal_url(url)
    dataset[18] = web_forwarding(response)
    dataset[19] = on_mouseover(response)
    dataset[20] = right_click(response)
    dataset[21] = popup_window(response)
    dataset[22] = iframe(response)
    dataset[23] = age_of_domain(whois_respo)
    dataset[24] = check_dns_record(url)
    dataset[25] = website_traffic(url)
    dataset[26] = page_rank(domain)
    dataset[27] = google_index(url)
    dataset[28] = links_pointing_to_page(response)
    dataset[29] = statistical_report(domain)

# calculate the ending time of dataset creation
    end = time.time()
