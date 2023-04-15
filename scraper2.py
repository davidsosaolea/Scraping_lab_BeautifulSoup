import requests
from bs4 import BeautifulSoup
import os
import datetime

HOME_URL = 'https://rpp.pe/ultimas-noticias'
ARTICLE_LINK_SELECTOR = 'h2 a'
ARTICLE_TITLE_SELECTOR = 'header h1'
ARTICLE_SUMMARY_SELECTOR = 'header div h2'
ARTICLE_BODY_SELECTOR = '#article-body > p:not([class])'

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = BeautifulSoup(notice, 'html.parser')
            
            try:
                title = parsed.select_one(ARTICLE_TITLE_SELECTOR).text.strip()
                title = title.replace('\"','')
                title = title.replace('S/','PEN')
                summary = parsed.select_one(ARTICLE_SUMMARY_SELECTOR).text.strip()
                body = [p.text.strip() for p in parsed.select(ARTICLE_BODY_SELECTOR)]
            except AttributeError:
                return
            
            with open(f'{today}/{title}.txt','w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = BeautifulSoup(home, 'html.parser')
            links_to_notices = parsed.select(ARTICLE_LINK_SELECTOR)
            
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notices:
                parse_notice(link['href'], today)
            
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
    
def run():
    parse_home()
    
if __name__ == "__main__":
    run()
