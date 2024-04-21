import requests
from bs4 import BeautifulSoup
import whois
import re
import time
import string
import datetime
import tldextract
import favicon
from pytz import utc
from favicon import get
from datetime import datetime, timezone
from datetime import date
from tldextract import extract
from urllib.parse import urljoin, urlparse
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
                print("Request URL percentage = ", percentage)

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
                print("Links in tags percentage = ", percentage)

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
            print(action)
            if action and action.lower().startswith("mailto:"):
                print("hello")
                return 1

        # Look for presence of email input fields or elements named "email"
        for form in soup.find_all('form'):
            for element in form.find_all(['input', 'textarea']):
                if element.get('type') == 'email' or element.get('name') == 'email':
                    print(element.get('type') == 'email')
                    print(element.get('name') == 'email')
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

        # Look for event handlers that prevent default right-click behavior
        # (replace with more comprehensive checks)
        blocking_scripts = soup.find_all(
            "script", text=lambda x: x and "oncontextmenu" in x and "return false" in x
        )

        # True if at least one script is found
        if len(blocking_scripts) > 0:
            return -1
        else:
            return 1

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
        print(response)
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


url = input("enter url : ")
generate_dataset(url)
