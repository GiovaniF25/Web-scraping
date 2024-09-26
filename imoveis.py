from os import WCONTINUED, link, sep
from typing import AsyncIterable
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# URL base do site onde os apartamentos estão listados, com placeholder para a página
url = 'https://www.vivareal.com.br/venda/parana/curitiba/apartamento_residencial/?pagina={}'

# Inicializa a variável da página
i = 1 
# Faz a requisição para a primeira página e obtém o conteúdo HTML
ret = requests.get(url.format(i))
soup = bs(ret.text, 'html.parser')  # Adicionando o parser para o BeautifulSoup

# Encontra todos os links de imóveis na página
houses = soup.find_all(
    'a', {'class': 'property-card__content-link js-card-title'})
# Obtém a quantidade total de imóveis listados na página
qtd_imoveis = float(soup.find('strong', {'class': 'results-summary__count'}).text.replace('.', ''))

# Exibe o número de imóveis encontrados
len(houses)

# Calcula a quantidade de páginas necessárias (36 imóveis por página)
qtd_imoveis / 36

# Seleciona o primeiro imóvel da lista
house = houses[0]

# Exibe o objeto do primeiro imóvel
house

# Cria um DataFrame vazio com colunas especificadas
df = pd.DataFrame(
    columns=[
        'descricao',
        'endereco',
        'area',
        'quartos',
        'wc',
        'vagas',
        'valor',
        'condominio',
        'wlink'
    ]
)
# Inicializa o contador de páginas
i = 0

# Loop para continuar extraindo dados até que todos os imóveis sejam coletados
while qtd_imoveis > df.shape[0]:
    i += 1  # Incrementa o número da página
    print(f"valor i: {i} \t\t qtd_imoveis: {df.shape[0]}")  # Exibe o progresso
    ret = requests.get(url.format(i))  # Faz a requisição para a página atual
    soup = bs(ret.text, 'html.parser')  # Faz a análise do HTML da página
    houses = soup.find_all(
        'a', {'class': 'property-card__content-link js-card-title'})  # Encontra os imóveis

    # Loop para extrair informações de cada imóvel
    for house in houses:
        try:
            descricao = house.find('span', {'class': 'property-card__title'}).text.strip()  # Obtém a descrição
        except:
            descricao = None  # Caso ocorra erro, atribui None
        try:
            endereco = house.find('span', {'class': 'property-card__address'}).text.strip()  # Obtém o endereço
        except:
            endereco = None
        try:
            area = house.find('span', {'class': 'js-property-card-detail-area'}).text.strip()  # Obtém a área
        except:
            area = None
        try:
            quartos = house.find('li', {'class': 'property-card__detail-room'}).span.text.strip()  # Obtém o número de quartos
        except:
            quartos = None
        try:
            wc = house.find('li', {'class': 'property-card__detail-bathroom'}).span.text.strip()  # Obtém o número de banheiros
        except:
            wc = None
        try:
            vagas = house.find('li', {'class': 'property-card__detail-garage'}).span.text.strip()  # Obtém o número de vagas
        except:
            vagas = None
        try:
            valor = house.find('div', {'class': 'property-card__price'}).p.text.strip()  # Obtém o valor do imóvel
        except:
            valor = None
        try:
            condominio = house.find('strong', {'class': 'js-condo-price'}).text.strip()  # Obtém o valor do condomínio
        except:
            condominio = None
        try:
            wlink = 'https://www.vivareal.com.br' + house['href']  # Obtém o link do imóvel
        except:
            wlink = None

        # Adiciona os dados coletados ao DataFrame
        df.loc[df.shape[0]] = [
            descricao,
            endereco,
            area,
            quartos,
            wc,
            vagas,
            valor,
            condominio,
            wlink
        ]

# Exibe os dados do último imóvel coletado
print(descricao)
print(endereco)
print(area)
print(quartos)
print(wc)
print(vagas)
print(valor)
print(condominio)
print(wlink)

# Salva o DataFrame em um arquivo CSV
df.to_csv('banco_de_imoveis.csv', sep=';', index=False)
