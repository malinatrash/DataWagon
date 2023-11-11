import requests
from bs4 import BeautifulSoup
import json

tenders_url = set()
for i in range(1, 50):

    url = f'https://www.roseltorg.ru/search/44fz?section=44fz&source[]=1&status[]=5&status[]=0&currency=all&page={i}'

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep - alive",
        "Cache-Control": "no-cache, no-store",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv: 109.0) Gecko/20100101 Firefox/119.0"
    }

    r = requests.get(url=url, headers=headers)
    result = r.content

    soup = BeautifulSoup(result, 'lxml')
    tenders = set(soup.find_all(class_= 'search-results__link'))
    print(i)
    for tender in tenders:
        tender_page_url = tender.get('href')
        tenders_url.add(f'https://www.roseltorg.ru{tender_page_url}')

with open('tenders_url.txt', 'a') as file:
    for line in tenders_url:
        file.write(f'{line}\n')



with open('tenders_url.txt') as file:
     lines = [line.strip() for line in file.readlines()]

     data_dict = []
     count = 0

     for line in lines:
         headers = {
             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
             "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
             "Accept-Encoding": "gzip, deflate, br",
             "Connection": "keep - alive",
             "Cache-Control": "no-cache, no-store",
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv: 109.0) Gecko/20100101 Firefox/119.0"
         }
         r = requests.get(url=line, headers=headers)
         result = r.content

         soup = BeautifulSoup(result, 'lxml')
         tender_time = soup.find(class_='lot-item__time')
         tender_name = soup.find(class_='data-table__info').text
         tender_from_name = soup.find(class_='search-results__tooltip').text
         tender_price = soup.find(class_='lot-item__sum').find('p').text
         tender_time_text = tender_time.text.strip()
         tender_time_text = " ".join(tender_time_text.split())
         data = {
             'tender_name': tender_name,
             'tender_from_name': tender_from_name,
             'tender_time': tender_time_text,
             'tender_price': tender_price
         }

         count += 1
         print(f'#{count}: {line} is done!')
         data_dict.append(data)
         with open('tenders_data.json', 'w') as json_file:
             json.dump(data_dict, json_file, ensure_ascii=False, indent=4)


