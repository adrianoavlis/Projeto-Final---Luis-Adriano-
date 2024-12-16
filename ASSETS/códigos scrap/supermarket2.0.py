from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import logging


# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_html(url):
    try:
        response = urlopen(url)
        return response.read()
    except Exception as e:
        logging.error(f"Erro ao buscar HTML: {e}")
        return None

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('article', class_='card-product')

def extract_data(anuncios):
    cards = []
    for anuncio in anuncios:
        card = {}
        
        # Selos
        seal_tag = anuncio.find('span', class_='card-product__seal-inner')
        card['seal'] = seal_tag.get_text(strip=True) if seal_tag else 'N/A'

        # Imagem
        image_tag = anuncio.find('figure', class_='card-product__image').find('img')
        card['image'] = image_tag['src'] if image_tag else 'N/A'
        
        # Título do Produto
        title_tag = anuncio.find('h3', class_='card-product__title')
        card['name'] = title_tag.get_text(strip=True) if title_tag else 'N/A'
        
        # Preço
        price_tag = anuncio.find('span', class_='card-product__price')
        card['price'] = price_tag.get_text(strip=True).replace('\n', '').replace(' ', '') if price_tag else 'N/A'
        
        # Adicionando resultado à lista cards
        cards.append(card)
    return cards

def save_to_files(dataset, path):
    dataset.to_csv(f'{path}/datasetSupermarket.csv', sep=';', index=False, encoding='utf-8-sig')
    dataset.to_excel(f'{path}/datasetSupermarket.xlsx', index=False)



def main():
    url = 'https://redesupermarket.com.br/ofertas/'
    html = fetch_html(url)
    if html:
        anuncios = parse_html(html)
        data = extract_data(anuncios)
        dataset = pd.DataFrame(data)
        save_path = r'C:\\Users\\PC\\Projetos\\Projeto-Final---Luis-Adriano-\\ASSETS\\data\\WebData\\supermarket2.0'
        save_to_files(dataset, save_path)
        
        print(dataset)

if __name__ == '__main__':
    main()
