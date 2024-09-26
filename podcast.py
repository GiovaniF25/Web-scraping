from os import sep
import requests
from bs4 import BeautifulSoup as bs
import logging
import pandas as pd

# URL da página de podcasts
url = 'https://portalcafebrasil.com.br/todos/podcasts/'

# Faz a requisição para a URL
ret = requests.get(url)

# Cria um objeto BeautifulSoup a partir do texto da resposta
soup = bs(ret.text, 'html.parser')

# Encontra todos os elementos <h5> que contêm informações dos podcasts
lst_podcast = soup.find_all('h5')

# Exibe o nome e o link de cada episódio
for item in lst_podcast:
    print(f"EP: {item.text} - Link: {item.a['href']}")

# URL para páginas adicionais de podcasts
url = 'https://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true'

# Função para coletar podcasts a partir de uma URL
def get_podcast(url):
    ret = requests.get(url)
    soup = bs(ret.text, 'html.parser')
    return soup.find_all('h5')

# Configuração de logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

# Inicializa contagem de páginas e lista de podcasts
i = 1
lst_podcast = []
lst_get = get_podcast(url.format(i))
log.debug(f"Coletado {len(lst_get)} episódios do link: {url.format(i)}")
while len(lst_get) > 0:
    lst_podcast = lst_podcast + lst_get
    i += 1
    lst_get = get_podcast(url.format(i))
    log.debug(f"Coletado {len(lst_get)} episódios do link: {url.format(i)}")

# Exibe a quantidade total de episódios coletados
len(lst_podcast)

# Cria um DataFrame para armazenar os nomes e links dos podcasts
df = pd.DataFrame(columns=['nome', 'link'])
for item in lst_podcast:
    df.loc[df.shape[0]] = [item.text, item.a['href']]

# Exibe a forma do DataFrame
df.shape

# Salva o DataFrame em um arquivo CSV
df.to_csv('banco_de_podcast.csv', sep=';', index=False)
