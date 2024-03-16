import requests
from bs4 import BeautifulSoup
import json
import os

url = 'https://bikzg.ru/'

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}
result = []
list_links_content = []
list_links_manu = []

req  = requests.get(url,headers=headers)
soup = BeautifulSoup(req.content,'lxml')

link = soup.find_all(class_='product__header')
for i in link:
    links = i.find('a').get('href')
    list_links_manu.append('https://bikzg.ru' + links)

for url_menu in list_links_manu:
    req_2  = requests.get(url_menu,headers=headers)
    soup = BeautifulSoup(req_2.content,'lxml')
    product__title = soup.find_all(class_='product__title')
    for i_2 in product__title:
        links_content = i_2.find('a').get('href')
        list_links_content.append('https://bikzg.ru' + links_content)

for url_content in list_links_content:
    req_3  = requests.get(url_content, headers=headers)
    soup = BeautifulSoup(req_3.content,'lxml')

    try:
        name__title = soup.find(class_='shop-item__title h1').text
        if name__title is not None:
            list_name = name__title
        else:
           list_name = '-' 
    except AttributeError:
        list_name = '-'



    r = ['/']
    for item in r:
        if item in list_name:
            list_name = list_name.replace(item,'_')

    
    try:
        item_price = soup.find(class_='item-price')
        if item_price is not None:
            list_price = item_price.text
        else:
            list_price = '-'
    except AttributeError:
        list_price = '-'
    try:
        img_url = soup.find(class_='media-box').find('a').get('href')
        img = 'https://bikzg.ru' + img_url
    except AttributeError:
        continue

    directory = 'bikzg.ru/data/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Запрашиваем изображение и записываем его в файл
    img_path = os.path.join(directory, f'{list_name}.jpg')
    req = requests.get(img)
    with open(img_path, 'wb') as file:
        file.write(req.content)

    result.append({
        'name': list_name,
        'price': list_price,
        'url': url_content,
    })
        
    with open(f'bikzg.ru/1.json', 'w', encoding='utf-8') as file:  
        json.dump(result, file, indent=4, ensure_ascii=False)