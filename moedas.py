import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

BASE_URL = 'https://www.vivareal.com.br/venda/parana/curitiba/apartamento_residencial/?pagina={}'

def get_total_properties():
    response = requests.get(BASE_URL.format(1))
    soup = BeautifulSoup(response.text, 'html.parser')
    total = soup.find('strong', {'class': 'results-summary__count'}).text.replace('.', '')
    return int(total)

def get_properties(page):
    response = requests.get(BASE_URL.format(page))
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all('a', {'class': 'property-card__content-link js-card-title'})

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

total_properties = get_total_properties()
pages = (total_properties // 36) + 1

df = pd.DataFrame(columns=['descricao', 'endereco', 'area', 'quartos', 'wc', 'vagas', 'valor', 'condominio', 'wlink'])

for page in range(1, pages + 1):
    logging.info(f"Coletando página {page}/{pages}")
    properties = get_properties(page)

    for prop in properties:
        descricao = prop.find('span', {'class': 'property-card__title'})
        endereco = prop.find('span', {'class': 'property-card__address'})
        area = prop.find('span', {'class': 'js-property-card-detail-area'})
        quartos = prop.find('li', {'class': 'property-card__detail-room'})
        wc = prop.find('li', {'class': 'property-card__detail-bathroom'})
        vagas = prop.find('li', {'class': 'property-card__detail-garage'})
        valor = prop.find('div', {'class': 'property-card__price'})
        condominio = prop.find('strong', {'class': 'js-condo-price'})
        wlink = prop.get('href')

        df.loc[df.shape[0]] = [
            descricao.text.strip() if descricao else None,
            endereco.text.strip() if endereco else None,
            area.text.strip() if area else None,
            quartos.span.text.strip() if quartos and quartos.span else None,
            wc.span.text.strip() if wc and wc.span else None,
            vagas.span.text.strip() if vagas and vagas.span else None,
            valor.p.text.strip() if valor and valor.p else None,
            condominio.text.strip() if condominio else None,
            f'https://www.vivareal.com.br{wlink}' if wlink else None
        ]

df.to_csv('banco_de_imoveis.csv', sep=';', index=False)
logging.info(f"Arquivo salvo com {df.shape[0]} imóveis coletados.")
