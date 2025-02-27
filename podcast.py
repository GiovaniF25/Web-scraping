import os
import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd

BASE_URL = 'https://portalcafebrasil.com.br/todos/podcasts/'

def get_podcasts(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all('h5')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

page = 1
all_podcasts = []
podcasts = get_podcasts(BASE_URL)

while podcasts:
    logging.debug(f"Página {page}: {len(podcasts)} episódios coletados")
    all_podcasts.extend(podcasts)
    page += 1
    podcasts = get_podcasts(f'https://portalcafebrasil.com.br/todos/podcasts/page/{page}/?ajax=true')

df = pd.DataFrame([(p.text, p.a['href']) for p in all_podcasts], columns=['Nome', 'Link'])

csv_file = 'banco_de_podcast.csv'
df.to_csv(csv_file, sep=';', index=False)
logging.info(f"Arquivo salvo: {csv_file}")

print(f"Total de episódios coletados: {df.shape[0]}")
