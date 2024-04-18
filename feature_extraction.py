import requests
from bs4 import BeautifulSoup
import whois
import re
import time
import string
import datetime
import tldextract
import favicon
from favicon import get
from datetime import datetime
from datetime import date
from tldextract import extract
from const import constant

# instance for constant class
constitems = constant()


# checking ip adress found or not in the url
def having_ip_address(domain):

    if domain == "" or domain == None:
        return -1

    else:
        split_url = domain.replace(".", "")
        counter_hex = 0

        for i in split_url:
            for i in string.hexdigits:
                counter_hex += 1

        total_len = len(split_url)
        having_ip_address = 1

        if counter_hex >= total_len:
            having_ip_address - 1

        return having_ip_address


def url_length(url):
    if len(url) < 100:
        return 1
    elif len(url) >= 54 and len(url) <= 400:
        return -1
    else:
        return 0


def shortening_service(domain):
    if domain == "" or domain == None:
        return -1

    else:
        # use of the instance
        famous_short_urls = constitems.famous_short_urls

        status = 1
        if domain in famous_short_urls:
            status = -1
        return status


def at_in_url(url):
    label = 1
    find_at_symbol = url.find('@')
    # print(find_at_symbol)
    if find_at_symbol != -1:
        label = -1

    return label


def double_slash_redirecting(url):
    list = [x.start(0) for x in re.finditer('//', url)]
    # print(list)
    l = len(list)-1
    # print(list[l])
    if list[l] > 6:
        if list[l] > 7:
            return -1

    return 1


def prefix_suffix(domain):
    counter = 0

    if domain == "" or domain == None:
        return -1

    else:
        y = 1
        # prefix
        index = domain.find("-")
        # print(index)
        if index != -1:
            y = -1
        # suffix
        else:
            for x in domain:
                if x == '.':
                    counter += 1
            # print(counter)
            if counter >= 2:
                y = -1
    return y


def having_sub_domain(domain):
    if domain == "" or domain == None:
        return -1

    else:

        index = domain.rfind(".")
        print(index)
        if index != -1:
            split_url = domain[:index]
            # print(split_url)
        counter = 0
        for i in split_url:
            if i == ".":
                counter += 1

        label = 1
        if counter == 2:
            label = 0
        elif counter >= 3:
            label = -1

        return label


def ssl_final_state(url):
    print("hello")


def domain_registration_length(whois_response):
    try:
        expiration_date = whois_response.expiration_date
        registration_length = 0
        list_check = isinstance(expiration_date, list)
        if (list_check == True):
            expiration_date = min(expiration_date)
        # print("Expiration date = ", expiration_date)
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        registration_length = abs((expiration_date - today).days)
        # print(registration_length/365)
        # print(registration_length)

        if registration_length / 365 <= 1:
            return -1

        else:
            return 1

    except:
        return -1


def favicon(url, soup, response):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        # print(response)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)

        favicon_tag = soup.find('link', "rel='icon'") or soup.find(
            'link', "rel='shortcut icon'")
        # print(favicon_tag)

        if favicon_tag:
            return 1  # Favicon found
        else:
            return -1  # Favicon not found
    except Exception as e:
        print("Error:", e)
        return -1


def port(domain):
    # print(domain)

    if domain == "" or domain == None:
        return -1

    else:

        try:
            port = domain.split(":")[1]
            # print(port)
            if port:
                return -1
            else:
                return 1
        except:
            return 1


def https_token(domain):
    if domain == "" or domain == None:
        return -1
    else:
        index = domain.find('//https')
        if index != -1:
            return -1
            
        else:
            return 1
            


def request_url(url, domain, soup):
    i = 0
    success = 0

    try:

        if soup == -999:
            # print("Request URL : Soup -999")
            #print("hellokool")
            return -1
            # data['Request_URL']=-1

        else:
            # print("hai")
            for img in soup.find_all('img', src=True):
                dots = [x.start(0) for x in re.finditer('\.', img['src'])]
                # print(dots)
                if url in img['src'] or domain in img['src'] or len(dots) == 1:
                    success = success + 1
                    #print("1:"+str(success))
                i = i+1

            for audio in soup.find_all('audio', src=True):
                dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
                #print(dots)
                if url in audio['src'] or domain in audio['src'] or len(dots) == 1:
                    success = success + 1
                    #print("2:"+str(success))
                i = i+1

            for embed in soup.find_all('embed', src=True):
                dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
                if url in embed['src'] or domain in embed['src'] or len(dots) == 1:
                    success = success + 1
                    #print("3:"+str(success))
                i = i+1

            for iframe in soup.find_all('iframe', src=True):
                dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
                if url in iframe['src'] or domain in iframe['src'] or len(dots) == 1:
                    success = success + 1
                    #print("4:"+str(success))
                i = i+1
            #print(success)
            # print(dots)
            #print(i)
            try:
                percentage = success/float(i) * 100
                print("Request URL percentage = ", percentage)

                if percentage < 22.0:
                    return 1
                    
                elif ((percentage >= 22.0) and (percentage < 61.0)):
                    return 0
                    
                else:
                    #print("hello887")
                    return -1

                    
            except:
                return 1
                

    except Exception as e:
        #print("hellosee", e)
        return -1


def url_of_anchor(url, domain, soup):
    print("hello")


def links_in_tags(url, domain, soup):
    print("hello")


def sfh(url):
    print("hello")


def check_submit_to_email(response):
    print("hello")


def abnormal_url(url):
    print("hello")


def web_forwarding(response):
    print("hello")


def on_mouseover(response):
    print("hello")


def right_click(response):
    print("hello")


def popup_window(response):
    print("hello")


def iframe(response):
    print("hello")


def age_of_domain(whois_response):
    print("hello")


def check_dns_record(url):
    print("hello")


def website_traffic(url):
    print("hello")


def page_rank(domain):
    print("hello")


def google_index(url):
    print("hello")


def links_pointing_to_page(response):
    print("hello")


def statistical_report(domain):
    print("hello")


# Dataset generation function
def generate_dataset(url):

    # initialize the dataset list
    dataset = [0] * 30


# convert the url in to standard format
    if not re.match(r"https?", url):
        url = "https://" + url

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
        print(whois_respo)
        domain = whois_respo.domain_name
        print(domain)
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
    dataset[9] = favicon(url, soup, response)
    dataset[10] = port(domain)
    dataset[11] = https_token(domain)
    dataset[12] = request_url(url, domain, soup)
    dataset[13] = url_of_anchor(url, domain, soup)
    dataset[14] = links_in_tags(url, domain, soup)
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

    data = {}
    data['having_ip_address'] = dataset[0]
    data['url_length'] = dataset[1]
    data['shortening_service'] = dataset[2]
    data['at_in_url'] = dataset[3]
    data['double_slash_redirecting'] = dataset[4]
    data['prefix_suffix'] = dataset[5]
    data['having_sub_domain'] = dataset[6]
    data['ssl_final_state'] = dataset[7]
    data['domain_registration_length'] = dataset[8]
    data['favicon'] = dataset[9]
    data['port'] = dataset[10]
    data['https_token'] = dataset[11]
    data['request_url'] = dataset[12]
    data['url_of_anchor'] = dataset[13]
    data['links_in_tags'] = dataset[14]
    data['sfh'] = dataset[15]
    data['check_submit_to_email'] = dataset[16]
    data['abnormal_url'] = dataset[17]
    data['web_forwarding'] = dataset[18]
    data['on_mouseover'] = dataset[19]
    data['right_click'] = dataset[20]
    data['popup_window'] = dataset[21]
    data['iframe'] = dataset[22]
    data['age_of_domain'] = dataset[23]
    data['check_dns_record'] = dataset[24]
    data['website_traffic'] = dataset[25]
    data['page_rank'] = dataset[26]
    data['google_index'] = dataset[27]
    data['links_pointing_to_page'] = dataset[28]
    data['statistical_report'] = dataset[29]

    count = 0
    l = []
    l.append(dataset)
    l.append(end-start)
    # print(l)

    for i in dataset:
        count += 1

    print("Enter URL : ", url)
    print("\nNumber of features extracted = ", count)
    print("Time taken to generate dataset =%.2f" % l[1], " seconds")
    print("The generated dataset is : ")
    print(dataset)
    print("\n")
    # [print (key,':',value) for key,value in data.items()]
    print("\n")
    return l


url = input("enter url : ")
generate_dataset(url)
