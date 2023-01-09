import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint
import json

HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

def get_headers():
    return Headers(browser='firefox', os='win').generate()


hh_main_html = requests.get(HOST, headers=get_headers()).text
soup = BeautifulSoup(hh_main_html, features='lxml')
# pprint(soup)

vacancy_list_tag = soup.find(id='a11y-main-content')
vacancy_tags = vacancy_list_tag.find_all(class_='serp-item')
# pprint(vacancy_tags)

vacancies = []

for vacancy in vacancy_tags:
    link_tag = vacancy.find('a', class_='serp-item__title')
    link = link_tag['href']  # Ссылка на вакансию
    # pprint(link)
    vacancy_html = requests.get(link, headers=get_headers()).text
    vacancy_body = BeautifulSoup(vacancy_html, features='lxml').find(class_='vacancy-section').text  # Текст вакансии
    # pprint(vacancy_body)
    if "Django" in vacancy_body or "Flask" in vacancy_body:
        company_name_tag = vacancy.find(attrs={"data-qa": "vacancy-serp__vacancy-employer"}).text
        company_name = company_name_tag.replace(u'\xa0', u' ')  # Название компании
        # pprint(company_name)
        city_tag = vacancy.find(attrs={"data-qa": "vacancy-serp__vacancy-address"}).text
        city_list = city_tag.split(',')
        city = city_list[0]  # Название города
        # pprint(city)
        salary_tag = BeautifulSoup(vacancy_html, features='lxml').find(attrs={"data-qa": "vacancy-salary"}).text
        salary = salary_tag.replace(u'\xa0', u' ')  # Зарплата
        # pprint(salary)
        vacancies.append({
            'link': link,
            'salary': salary,
            'company_name': company_name,
            'city': city
        })
# pprint(vacancies)

with open('data.json', 'w', encoding="utf-8") as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)

