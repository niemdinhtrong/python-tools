import requests
from bs4 import BeautifulSoup

URL = "https://cohami.online/product-category/t-shirts/"

def get_data(url):
    datas = requests.get(url)
    data = BeautifulSoup(datas.text, "lxml")
    return data

def get_product(data):
    datas = data.find(class_="products columns-4")
    datas = datas.find_all('li')
    return datas

def visit_product(datas):
    for data in datas:
        url = data.find('a').get('href').strip()
        try:
            a = requests.get(url)
        except:
            pass
def get_num_pages(data):
    try:
        datas = data.find(class_="page-numbers")
        datas = datas.find_all('li')
        if (len(datas) > 2):
            del datas[-1]
            del datas[0]
        else:
            datas = []

        num_pages = []
        if (len(datas) != 0):
            for data in datas:
                url = data.find('a').get('href').strip()
                num_pages.append(url)
        return num_pages
    except:
        num_pages = []
        return num_pages

def main():
    data = get_data(URL)
    num_pages = get_num_pages(data)
    products = get_product(data)
    visit_product(products)
    if (len(num_pages) != 0):
        for page in num_pages:
            data = get_data(URL)
            products = get_product(data)
            visit_product(products)

if __name__ == "__main__":
    main()