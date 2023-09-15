import requests
import bs4
import fake_headers


def find_key_wards(name_tag_text, articles_body_item_text, hub_tags_text):
    all_information = f'{name_tag_text}, {articles_body_item_text}, {hub_tags_text}'
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    for keyword in KEYWORDS:
        if all_information.find(keyword) != -1:
            return True


headers_gen = fake_headers.Headers(browser='opera', os='win')
resource = requests.get('https://habr.com/ru/articles/', headers=headers_gen.generate())
html_data = resource.text
soup = bs4.BeautifulSoup(html_data, features='lxml')
div_articles_list_tag = soup.find('div', class_='tm-articles-list')
articles_tags = div_articles_list_tag.find_all('article')

for articles_tag in articles_tags:
    time_tag = articles_tag.find('time')
    name_tag = articles_tag.find('a', class_='tm-title__link')
    articles_body_item = articles_tag.find('p')  # body
    if articles_body_item is None:
        articles_body_item = articles_tag.find('br')
        articles_body_item_text = articles_body_item.text  # text body
    else:
        articles_body_item_text = articles_body_item.text  # text body
    id_tag = articles_tag['id']
    name_tag_span = name_tag.find('span')
    name_tag_text = name_tag_span.text  # name
    time_tag_date = time_tag['title']  # date
    link = name_tag['href']  # link
    hub_tags = articles_tag.find('div', class_='tm-publication-hubs__container')
    hub_tags_text = hub_tags.text
    if find_key_wards(name_tag_text, articles_body_item_text, hub_tags_text) is True:
        print(f'{time_tag_date} {name_tag_text} https://habr.com{link}')

