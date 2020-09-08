import requests
import queue
from bs4 import BeautifulSoup
from threading import Thread

URL = "https://cohami.online/product-category/t-shirts/"

def get_data(url):
    datas = requests.get(url)
    data = BeautifulSoup(datas.text, "lxml")
    return data

def get_product(data,q1):
    datas = data.find(class_="products columns-4")
    datas = datas.find_all('li')
    for data in datas:
        url = data.find('a').get('href').strip()
        q1.put(url)

def visit_product(q1):
    while not q1.empty():
        try:
            url = q1.get()
            a = requests.get(url)
            print(url)
            q.task_done()
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

def task(q):
    all_proc = []
    for i in range (4):
        proc = Thread(target=visit_product, args=(q,))
        all_proc.append(proc)
    for p in all_proc:
        p.start()
    for p in all_proc:    
        p.join()


def main():
    q1 = queue.Queue()
    data = get_data(URL)
    num_pages = get_num_pages(data)
    products = get_product(data, q1)
    task(q1)
    if (len(num_pages) != 0):
        for page in num_pages:
            data = get_data(URL)
            products = get_product(data, q1)
            task(q1)

if __name__ == "__main__":
    main()