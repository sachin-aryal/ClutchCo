import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs


# output = open("output.csv", "w")
# output.write("Company Name, Category, Contact\n")


def get_content(url):
    print("Get Request for {}".format(url))
    try:
        response = requests.get(url=url)
        return response.content
    except Exception as ex:
        print("Error occurred: {}".format(str(ex)))


def get_contact_us_link(link):
    content = get_content(link)
    bs = BeautifulSoup(content, parser="lxml", features="lxml")
    contact_link = link
    try:
        a_tags = bs.findAll("a")
        for a in a_tags:
            text = str(a.text).lower()
            if text.startswith("contact"):
                contact_link = a["href"]
                if len(contact_link) < len(link):
                    link = link[:link.find('?')]
                    contact_link = link+""+contact_link
                break
    except:
        pass
    return contact_link


def get_brand_data(category, link):
    page = 0
    print("Fetching Data for {}".format(category))
    while True:
        url = "https://clutch.co/{}?page={}".format(link, page)
        bs = BeautifulSoup(get_content(url=url), parser="lxml", features="lxml")
        companies = bs.findAll("li", {"class": "provider-row"})
        not_found = True
        for company in companies:
            not_found = False
            company_name = company.find("h3", {"class": "company-name"})
            company_name = company_name.text
            company_link = company.find("li", {"class": "website-link"})
            company_link = company_link.find("a")
            company_link = company_link["href"]
            if len(company_name.strip()) > 1:
                output.write(company_name+", "+category+", "+get_contact_us_link(company_link))
        if not_found:
            break
        page += 1
        time.sleep(1)

def get_brands():
    response = requests.get("https://clutch.co/sitemap")
    bs = BeautifulSoup(response.content, parser="lxml", features="lxml")
    content = bs.find("ul", {"class": "site-map-menu"})
    lis = content.findAll("li", recursive=False)
    links = {}
    for li in lis:
        my_tag = li.find("ul")
        second_lis = my_tag.findAll("li", recursive=False)
        for each_li in second_lis:
            try:
                my_tag = each_li.find("ul")
                my_tag = my_tag.find("li")
                my_tag = my_tag.find("a")
                link = my_tag["href"]
                if len(links) > 0 and list(links.keys())[-1] == "All Supply Chain & Logistics Companies":
                    break
                category = my_tag.text
                links[category] = link
            except:
                pass
    return links

# brands = get_brands()
# for category, link in brands.items():
#     get_brand_data(category, link)
#     break
# output.close()

# print(get_contact_us_link("https://www.venthio.com/?utm_source=clutch&utm_medium=referral&utm_campaign=ad-agencies"))