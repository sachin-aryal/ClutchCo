import requests
from bs4 import BeautifulSoup
import time
import threading


def get_content(url):
    print("Get Request for {}".format(url))
    try:
        response = requests.get(url=url)
        return response.content
    except Exception as ex:
        print("Error occurred: {}".format(str(ex)))


def get_brand_data(category, link):
    page = 0
    print("Fetching Data for {}".format(category))
    output = open(category+".csv", "w")
    output.write("Company Name, Category, Contact\n")
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
            try:
                company_link = company_link.find("a")
                company_link = company_link["href"]
            except AttributeError:
                company_link = ""
            if len(company_name.strip()) > 1:
                output.write(company_name+", "+category+", "+company_link)
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

brands = get_brands()
all_threads = []
for category, link in brands.items():
    thread = threading.Thread(target=get_brand_data, args=(category, link, ))
    thread.start()
    all_threads.append(thread)

for th in all_threads:
  th.join()