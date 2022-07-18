import requests
from bs4 import BeautifulSoup
import csv

URL = "https://cars.kg/offers/?vendor=57fa24ee2860c45a2a2c093b"

HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "accept": "*/*",
}

LINK = "https://www.cars.kg"
FILE = "toyota.csv"


def get_html(headers, url, params=None):
    respons = requests.get(url, params=params, headers=headers)
    return respons


# def get_last_page_number(url):
#     url_numb = 1
#     action = True
#     while action:
#         url1 = url+str(url_numb)+'?vendor=57fa24ee2860c45a2a2c093b'
#         print(url1)
#         response = requests.get(url1)
#         print(response.status_code)
#         if response.status_code == 200:
#             url_numb += 1
#         else:
#             action = False
#     return url_numb


def get_all_urls(last_page):
    urls = []
    for i in range(1, last_page+1):
        urls.append('https://cars.kg/offers/'+str(i)+'?vendor=57fa24ee2860c45a2a2c093b')
    return urls

def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("a", class_="catalog-list-item")
    cars = []
    for i in items:
        try:
            cars.append({
                "title": i.find("span", class_="catalog-item-caption").get_text(),
                "image": i.find("img").get("src"),
                "discription": i.find("span", class_="catalog-item-descr").get_text().replace("\n\n", ""),
                "price": i.find("span", class_="catalog-item-price").get_text().replace("\n", "")
            })
        except Exception as ex:
            cars.append({
                "title": i.find("span", class_="catalog-item-caption").get_text(),
                "image": 'no photo',
                "discription": i.find("span", class_="catalog-item-descr").get_text().replace("\n\n", ""),
                "price": i.find("span", class_="catalog-item-price").get_text().replace("\n", "")
            })
    return cars


def save_file(content, file):
    with open(file, "a+") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Название машины", "Картинка", "Описание", "Цена"])
        for i in content:
            writer.writerow([i['title'], i['image'], i['discription'], i['price']])



def get_parse_result():
    urls = get_all_urls(29)
    for url in urls:
        html = get_html(url=url, headers=HEADERS)
    # print(html.text)
        content = get_content(html.text)
        save_file(content, FILE)
    # print(content)


get_parse_result()



# def activate_post_pagination(page):
#     URL = 'https://www.house.kg/snyat'
#     PAGE_URL = URL + f'?page={page}'
#     html = get_response(PAGE_URL)
#     post_links = get_links(html)
#     for link in post_links:
#             page = get_response(link)
#             data = get_page_data(page)
#             write_csv(data)