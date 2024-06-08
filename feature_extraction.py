import requests
from bs4 import BeautifulSoup
import whois
import re
import time
import ssl
import string
import datetime
import tldextract
import favicon
import socket
import api_keys
from googlesearch import search
from pytz import utc
from favicon import get
from datetime import datetime, timezone
from datetime import date
from subprocess import *
from tldextract import extract
from urllib.parse import urljoin, urlparse
from requests_html import HTMLSession
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
        # print(index)
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
    try:
        # check wheather contains https

        # print(index)
        if re.match(r"^https?", url):
            https = 1
        else:
            https = 0
        # print(https)

        # getting the certificate issuer to later compare with trusted issuer
        # getting host name
        subDomain, domain, suffix = extract(url)
        host_name = domain + "." + suffix
        context = ssl.create_default_context()
        sct = context.wrap_socket(socket.socket(), server_hostname=host_name)
        sct.connect((host_name, 443))
        certificate = sct.getpeercert()
        # print("certificate : ",certificate)
        issuer = dict(x[0] for x in certificate['issuer'])
        certificate_Auth = str(issuer['organizationName'])
        certificate_Auth = certificate_Auth.split()
        # print(certificate_Auth)

        if (certificate_Auth[0] == "Network" or certificate_Auth[0] == "Deutsche" or certificate_Auth[0] == "Entrust"):
            certificate_Auth = certificate_Auth[0] + " " + certificate_Auth[1]

        else:
            certificate_Auth = certificate_Auth[0]

        trusted_Auth = ['Amazon', 'Comodo', 'Cybertrust', 'Symantec', 'GoDaddy.com,', 'GlobalSign', 'DigiCert', 'StartCom', 'Entrust', 'Verizon', 'Trustwave', 'Unizeto', 'Buypass',
                        'QuoVadis', 'Deutsche Telekom', 'Network Solutions', 'SwissSign', 'IdenTrust', 'Secom', 'TWCA', 'GeoTrust', 'Thawte',
                        'Doster', 'VeriSign', 'LinkedIn', 'Let\'s', 'Sectigo', 'RapidSSLonline', 'SSL.com', 'Entrust Datacard', 'Google', 'Facebook']

        # getting age of certificate
        start_date = str(certificate['notBefore'])
        end_date = str(certificate['notAfter'])
        start_year = int(start_date.split()[3])
        end_year = int(end_date.split()[3])
        age_of_certificate = end_year-start_year
        # print(age_of_certificate)

        # checking final conditions
        if ((https == 1) and (certificate_Auth in trusted_Auth) and (age_of_certificate >= 1)):
            return 1  # legitimate

        elif ((https == 1) and (certificate_Auth in trusted_Auth)):
            return 0  # suspicious

        else:
            return -1  # phishing

    except Exception as e:
        print("SSL Exception", e)
        return -1


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
            # print("hellokool")
            return -1
            # data['Request_URL']=-1

        else:
            # print("hai")
            for img in soup.find_all('img', src=True):
                dots = [x.start(0) for x in re.finditer('\.', img['src'])]
                # print(dots)
                if url in img['src'] or domain in img['src'] or len(dots) == 1:
                    success = success + 1
                    # print("1:"+str(success))
                i = i+1

            for audio in soup.find_all('audio', src=True):
                dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
                # print(dots)
                if url in audio['src'] or domain in audio['src'] or len(dots) == 1:
                    success = success + 1
                    # print("2:"+str(success))
                i = i+1

            for embed in soup.find_all('embed', src=True):
                dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
                if url in embed['src'] or domain in embed['src'] or len(dots) == 1:
                    success = success + 1
                    # print("3:"+str(success))
                i = i+1

            for iframe in soup.find_all('iframe', src=True):
                dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
                if url in iframe['src'] or domain in iframe['src'] or len(dots) == 1:
                    success = success + 1
                    # print("4:"+str(success))
                i = i+1
            # print(success)
            # print(dots)
            # print(i)
            try:
                percentage = success/float(i) * 100
                # print("Request URL percentage = ", percentage)

                if percentage < 22.0:
                    return 1

                elif ((percentage >= 22.0) and (percentage < 61.0)):
                    return 0

                else:
                    # print("hello887")
                    return -1

            except:
                return 1

    except Exception as e:
        # print("hellosee", e)
        return -1


def url_of_anchor(url, domain, soup):
    percentage = 0
    i = 0
    unsafe = 0

    try:

        if soup == -999:
            return -1

        else:
            for a in soup.find_all('a', href=True):
                # 2nd condition was 'JavaScript ::void(0)' but we put JavaScript because the space between javascript and :: might not be
                # there in the actual a['href']
                if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
                    unsafe = unsafe + 1
                    # print(unsafe)
                i = i + 1
                # print(i)

            try:
                percentage = unsafe / float(i) * 100
                # print("URL of Anchor percentage = ", percentage)

                if percentage < 31.0:
                    return 1

                elif ((percentage >= 31.0) and (percentage <= 67.0)):
                    return 0

                else:
                    return -1

            except:
                return 1

    except:
        return -1


def links_in_tags(url, domain, soup):
    i = 0
    success = 0
    try:

        if soup == -999:
            return -1

        else:
            for link in soup.find_all('link', href=True):
                dots = [x.start(0) for x in re.finditer('\.', link['href'])]
                if url in link['href'] or domain in link['href'] or len(dots) == 1:
                    success = success + 1
                i = i+1

            for script in soup.find_all('script', src=True):
                dots = [x.start(0) for x in re.finditer('\.', script['src'])]
                if url in script['src'] or domain in script['src'] or len(dots) == 1:
                    success = success + 1
                i = i+1
            try:
                percentage = success / float(i) * 100
                # print("Links in tags percentage = ", percentage)

                if percentage < 17.0:
                    return 1

                elif ((percentage >= 17.0) and (percentage <= 81.0)):
                    return 0

                else:
                    return -1

            except:
                return 1

    except:
        return -1


def sfh(url):
    try:
        response = requests.get(url)
        # print(response)
        soup = BeautifulSoup(response.text, "lxml")
        # print(soup)

        # Check for multiple forms and handle relative URLs
        for form in soup.find_all('form'):
            action = form.get('action')
            # print(action)
            if action:
                # Handle relative URLs based on the original URL
                full_action = urljoin(url, action)
                # print(full_action)
                parsed_url = urlparse(full_action)
                # print(parsed_url)
                form_domain = parsed_url.netloc.lower()  # Extract and lowercase domain
                # print(form_domain)

                # Check for empty or "about:blank" action
                if not full_action or full_action.lower() == "about:blank":
                    return -1

                # Check domain match (heuristic)
                if urlparse(url).netloc.lower() in form_domain:  # Subdomain match
                    # print("helo")
                    return 1
                else:
                    return 0  # Different domain

        # No form found
        return -1

    except requests.exceptions.RequestException as e:
        print(f"Error getting URL info: {e}")
        return -1


def check_submit_to_email(url, response):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        # Look for form action containing "mailto"
        for form in soup.find_all('form'):
            action = form.get('action')
            # print(action)
            if action and action.lower().startswith("mailto:"):
                # print("hello")
                return 1

        # Look for presence of email input fields or elements named "email"
        for form in soup.find_all('form'):
            for element in form.find_all(['input', 'textarea']):
                if element.get('type') == 'email' or element.get('name') == 'email':
                    # print(element.get('type') == 'email')
                    # print(element.get('name') == 'email')
                    return 1

        # Look for specific keywords (less reliable)
        if any(keyword in response.text.lower() for keyword in ["mail", "email", "contact", "inquiry"]):
            # print(response.text.lower())
            # print(keyword in response.text.lower()

            return 1

        return -1

    except requests.exceptions.RequestException as e:
        print(f"Error getting URL info: {e}")
        return -1


def abnormal_url(url):
    index = url.find("://")
    split_url = url[index + 3:]

    index = split_url.find("/")
    if index != -1:
        split_url = split_url[:index]

    if re.match(r"^www.", split_url):
        split_url = split_url.replace("www.", "")

    split_url = split_url.lower()

    try:
        whois_response = whois.whois(url)
        d = whois_response.domain_name

        if d == "" or d is None:
            return -1  # Hostname not found in WHOIS data

        list_check = isinstance(d, list)

        if list_check:
            d = d[1].lower()
            if d == split_url:
                return 1
            else:
                return -1

        else:
            d = d.lower()
            if d == split_url:
                return 1
            else:
                return -1

    except Exception as e:
        # print("Error:", e)
        return -1


def web_forwarding(url, response):
    try:
        response = requests.get(url, allow_redirects=True)  # Allow redirects
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        # Extract domain names from original and final URLs
        original_parsed = urlparse(url)
        original_domain = original_parsed.netloc.lower()
        final_parsed = urlparse(response.url)
        # print(final_parsed)
        netloc_without_www = final_parsed.netloc[4:]
        final_domain = netloc_without_www.lower()

        # Check if final URL matches original URL
        if response.url == url:
            return 1  # No redirection occurred

        # Check if final URL has the same domain (ignoring subdomains)
        if original_domain == final_domain:
            # print(original_domain)
            # print(final_domain)
            return 1  # Redirection within the same domain
        else:

            return -1  # Redirection to a different domain

    except requests.exceptions.RequestException as e:
        print(f"Error checking redirect for {url}: {e}")
        return -1


def on_mouseover(soup):
    try:

        # print(soup)

        # Find all elements with the 'onmouseover' attribute
        elements = soup.find_all(attrs={'onmouseover': True})

        # True if at least one element has onmouseover
        if len(elements) > 0:
            return -1
        else:
            return 1
    except requests.exceptions.RequestException as e:
        print(f"Error fetching url: {e}")
        return -1


def right_click(soup):
    try:

        # Improved script detection using string attribute
        blocking_scripts = soup.find_all(
            "script", string=lambda x: x and "oncontextmenu" in x and "return false" in x
        )

        # Check for blocking scripts and return appropriate value
        if blocking_scripts:
            return -1
        else:
            return 0

    except requests.exceptions.RequestException as e:
        print(f"Error fetching url: {e}")
        return -1


def popup_window(soup):
    try:

        # Look for common pop-up indicators (replace with more comprehensive checks):
        # - Specific tags and attributes (e.g., links with '#', popup classes)
        # - Known JavaScript libraries or functions associated with pop-ups
        potential_indicators = [
            # Example: Link triggering a pop-up
            soup.find_all("a", href="#", class_="popup-trigger"),
            # Example: Script for pop-up
            soup.find_all("script", src=lambda x: x and "pop_up.js" in x),
            # Add more checks as needed
        ]

        # Check if any indicators are found
        for indicator in potential_indicators:
            if indicator:
                return -1

        # If no specific indicators are found, consider using a regular expression
        # for a broader (but less reliable) check (optional):
        # alert_usage = re.findall(r"alert\(", response.text)
        # if alert_usage:
        #     return True

            else:
                return 1  # No clear indicators found

    except requests.exceptions.RequestException as e:
        print(f"Error fetching or analyzing website code: {e}")
        return -1


def iframe(soup):
    try:

        # Look for all iframe tags
        iframes = soup.find_all("iframe")
        # True if at least one iframe is found
        if len(iframes) > 0:
            return -1
        else:
            return 1

    except requests.exceptions.RequestException as e:
        print(f"Error fetching or analyzing website code: {e}")
        return -1


def age_of_domain(whois_response):
    try:
        # Check for missing creation or expiration date
        if not whois_response.creation_date or not whois_response.expiration_date:
            return -1

        # Extract creation and expiration dates, handling potential lists
        creation_date = min(whois_response.creation_date) if isinstance(
            whois_response.creation_date, list) else whois_response.creation_date
        expiration_date = min(whois_response.expiration_date) if isinstance(
            whois_response.expiration_date, list) else whois_response.expiration_date

        # Convert to datetime objects if necessary
        if not creation_date.tzinfo:
            creation_date = creation_date.replace(tzinfo=utc)

        if not expiration_date.tzinfo:
            expiration_date = expiration_date.replace(tzinfo=utc)

        # Calculate approximate age in months (assuming 30 days per month)
        today = datetime.now(timezone.utc)
        age_in_days = abs((expiration_date - creation_date).days)
        age_in_months = int(age_in_days / 30)

        # Determine active or expired status based on expiration date
        if age_in_months > 6:
            return 1
        else:
            return -1  # Negative for expired domains

    except Exception as e:
        print("Age of domain exception:", e)
        return -1


def check_dns_record(url):
    try:
        # Extract domain and suffix using tldextract
        extracted_parts = extract(url)
        domain_suffix = f"{extracted_parts.domain}.{extracted_parts.suffix}"
        # print(domain_suffix)

        # Check for missing domain or suffix
        if not domain_suffix:
            # print("Invalid URL format. Unable to check DNS records.")
            return -1

        # Fetch WHOIS information
        whois_response = whois.whois(domain_suffix)

        # Check if WHOIS response contains creation_date
        if not hasattr(whois_response, "creation_date"):
            # print("WHOIS response lacks creation_date information.")
            return -1

        # Presence of DNS records indicates a potential website
        # print(f"DNS records found for: {domain_suffix}")
        return 1

    except whois.Exception as e:
        print(f"Error fetching WHOIS information: {e}")
        return -1

    except Exception as e:
        print(f"Unexpected error: {e}")
        return -1


def website_traffic(url):
    API_KEY = api_keys.api_key2
    # api_keys.api_key1
    try:
        # Check for API key
        if not API_KEY or not isinstance(API_KEY, str):
            print("Error: Please provide a valid API key as a string.")
            return -1

        # Get domain name from WHOIS
        whois_response = whois.whois(url)
        domain_name = whois_response.domain_name

        # Handle potential list output and convert to lowercase
        if isinstance(domain_name, list):
            domain_name = domain_name[0].lower()
        else:
            domain_name = domain_name.lower()

        # Construct API endpoint URL
        api_endpoint = f'https://api.similarweb.com/v1/similar-rank/{domain_name}/rank?api_key={API_KEY}'

        # Make API request
        response = requests.get(api_endpoint)

        # Check for successful response
        if response.status_code == 200:
            data = response.json()
            similar_rank_data = data['similar_rank']
            rank = similar_rank_data['rank']

            # Interpret SimilarRank
            if rank < 100000:
                # print("hello001")
                return 1  # Likely significant traffic
            else:
                return 0  # Low SimilarRank
        else:
            # print(
            # f"Error: API request failed with status code {response.status_code}")
            return -1

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


def page_rank(domain):
    if domain == "" or domain == None:
        return -1

    else:

        try:

            session = HTMLSession()
            res = session.get('https://checkpagerank.net/')
            soup = BeautifulSoup(res.html.html, "html.parser")
            forms = soup.find_all("form")
            new_form = forms[1]

            details = {}
            action = new_form.attrs.get("action").lower()
            method = new_form.attrs.get("method", "get").lower()

            inputs = []
            for input_tag in new_form.find_all("input"):
                # get type of input form control
                input_type = input_tag.attrs.get("type", "text")
                # get name attribute
                input_name = input_tag.attrs.get("name")
                # get the default value of that input tag
                input_value = input_tag.attrs.get("value", "")
                # add everything to that list
                inputs.append(
                    {"type": input_type, "name": input_name, "value": input_value})

            # put everything to the resulting dictionary
            details["action"] = action
            details["method"] = method
            details["inputs"] = inputs

            data = {}
            data[input_tag["name"]] = domain

            load = urljoin('https://checkpagerank.net/', details["action"])
            res = session.post(load, data=data)
            page_rank = re.findall(
                r"Google PageRank: <span style=\"color:#000099;\">([0-9]+)", res.text)
            # print(global_rank)
            page_rank = int(page_rank[0])
            # print("Google PageRank = ",page_rank)

            if page_rank > 2:
                return 1
            else:
                return -1

        except:
            print("Google Page Rank Exception")
            return -1


def google_index(url):
    try:
        site = search(url, 5)
        # print("Site = ", site)

        if site:
            return 1

        else:
            return -1

    except:
        return -1


def links_pointing_to_page(response):
    if response == "":
        return -1

    else:
        number_of_links = len(re.findall(r"<a href=", response.text))
        if number_of_links == 0:
            return -1

        elif number_of_links > 0 and number_of_links <= 2:
            return 0

        else:
            return 1


def statistical_report(domain):
    if domain == "" or domain == None:
        return -1
    else:

        url_match = re.search(constant.url_match, domain)

        try:
            ip_address = socket.gethostbyname(domain)
            ip_match = re.search('146\.112\.61\.108 | 213\.174\.157\.151 | 121\.50\.168\.88 | 192\.185\.217\.116 | 78\.46\.211\.158 | 181\.174\.165\.13 | 46\.242\.145\.103 | 121\.50\.168\.40 | 83\.125\.22\.219 | 46\.242\.145\.98|'
                                 '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                                 '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                                 '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                                 '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                                 '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42', ip_address)
            if url_match:
                return -1

            elif ip_match:
                return -1

            else:
                return 1

        except Exception as e:

            print('Connection problem. Please check your internet connection!', e)
            return -1


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
        # print(response)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
    except:
        response = ""
        soup = BeautifulSoup("", "html.parser")
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
            # print(domain)
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
    dataset[16] = check_submit_to_email(url, response)
    dataset[17] = abnormal_url(url)
    dataset[18] = web_forwarding(url, response)
    dataset[19] = on_mouseover(soup)
    dataset[20] = right_click(soup)
    dataset[21] = popup_window(soup)
    dataset[22] = iframe(soup)
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


#url = input("enter url : ")
#generate_dataset(url)
