import requests
from bs4 import BeautifulSoup
import json
import re

base_url = "http://books.toscrape.com/"
url = base_url + "catalogue/page-1.html"

pages_counter = 0 ### для подсчета количества обработанных веб-страниц
books = [] ### для сохранения распарсенных книг

while url:
    print("\nПроводится скрапинг страницы №", pages_counter+1)
    # Отправка GET запроса по URL
    response = requests.get(url)

    # Парсинг HTML страницы с использованием BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    h3_tags = soup.find_all("h3")

    for h3_tag in h3_tags:

        # Поиск тега <a> 
        a_tag = h3_tag.find("a", href=True)

        # Создание ссылки на страницу книги
        book_url = base_url + "catalogue/" + a_tag["href"]

        # Отправка запроса по ссылке на книгу
        book_response = requests.get(book_url)

        # Парсинг страницы книги
        book_soup = BeautifulSoup(book_response.text, "html.parser")

        ### экстракция требуемых данных о книге
        title = book_soup.find("h1").text.strip()
        price = float(book_soup.find("p", class_="price_color").text.strip().replace("Â\u00a3", ""))
        stock = int(re.findall(r'\d+', book_soup.find("p", class_="instock availability").text.strip())[0])
        description = book_soup.find("meta", attrs={"name": "description"})["content"]

        # Добавление информации о книге в общий список
        books.append({
                "Название": title,
                "Цена в фунтах стерлингов": price,
                "Количество в наличии": stock,
                "Описание": description
            })
        print("Добавили книгу", title)
    
    next_button = soup.find('a', string='next')
        
    ### Проверка, есть ли ссылка "next" на следующую страницу, делаем ограничение по количеству страниц (можно убрать, но будет долго) 
    if (next_button) and (pages_counter<9):
        url = base_url + "catalogue/" + next_button['href']
        pages_counter += 1
    else:
        url = None  # если ссылки нет - выходим из цикла while

print("\nСуммарное число книг: ", len(books)) 
### результат расчета суммарного числа распарсенных книг соответствует указанному на сайте

### сохранение общего списка в файл кодировкой, содержащей буквы русского алфавита
with open("books_from_books.toscrape.com.json", "w", encoding='utf-8') as f:
        json.dump(books, f, indent=4, ensure_ascii=False)