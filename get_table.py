import whois
import re
from datetime import datetime
from datetime import date
import time
from dateutil.parser import parse as date_parse

def gettable(url):
    # Converts the given URL into standard format
    if not re.match(r"^https?", url):
        url = "http://" + url

     # url length
    length = len(url)

    try:
        # Requests all the information about the domain
        whois_response = whois.whois(url)
        # print(whois_response)

        # Domain name
        domain = whois_response.domain_name
        list_check = isinstance(domain, list)
        if (list_check == True):
            domain = domain[1].lower()

        # Creation Date
        c_date = whois_response.creation_date

        list_check = isinstance(c_date, list)
        if (list_check == True):
            c_date = min(c_date)

         # Expiration Date
        e_date = whois_response.expiration_date

        list_check = isinstance(e_date, list)
        if (list_check == True):
            e_date = min(e_date)

         # Registrar
        reg = whois_response.registrar




    except Exception as e:
        domain = '-'
        c_date = '-'
        e_date = '-'
        reg = '-'

    # Domian Registration Length
    reg_length = 0

    try:
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        reg_length = abs((e_date - today).days)
        print("Registration length = ", reg_length)

    except Exception as e:
        reg_length = '-'

    l = []
    l.append(domain)
    l.append(c_date)
    l.append(e_date)
    l.append(reg)
    l.append(length)
    l.append(reg_length)

    for i in range(len(l)):
        if l[i] == "" or l[i] == None:
            l[i] = '-'
    #print(l)

    for i in range(len(l)):
        print(l[i])

    return l
#url = input(str("enter url"))
#gettable(url=url)