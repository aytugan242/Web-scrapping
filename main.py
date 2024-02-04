import bs4
import fake_headers
import requests
import json

URL = "https://spb.hh.ru/search/vacancy"

def gen_headers():
    headers_gen = fake_headers.Headers(os="win", browser="chrome")
    return headers_gen.generate()

# указываем параметры ('area', '1') - Москва, ('area', '2') - Санкт-Петербург, ('text', 'python+django+flask') - поиск
params = {
    'text': 'python django flask',
    'area': ['1', '2']
}

response = requests.get(URL, headers=gen_headers(), params=params)

main_html = response.text
main_page = bs4.BeautifulSoup(main_html, "lxml")

article_list_tag = main_page.find("main", class_="vacancy-serp-content")
articles_tags_div = article_list_tag.find_all("div", class_='vacancy-serp-item-body__main-info')

data = {}
data['Vacancies'] = []
for articles_tag_div in articles_tags_div:
    href = articles_tag_div.find("a", class_='bloko-link')['href']
    if articles_tag_div.find("span", class_='bloko-header-section-2'):
        price = articles_tag_div.find("span", class_='bloko-header-section-2').text
    else:
        price = 'Price не указан'
    company = articles_tag_div.find("a", class_='bloko-link bloko-link_kind-tertiary').text
    city = articles_tag_div.find("div", {'class': 'bloko-text', 'data-qa': 'vacancy-serp__vacancy-address'}).text.split(',')[0]

    data['Vacancies'].append({
        'href': href,
        'price': price,
        'company': company,
        'city': city
    })

if __name__ == '__main__':
    # print(data)
    with open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
        print('Данные записаны в файл data.json')
