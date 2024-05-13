import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image

image = Image.open("nino.jpg")
nueva_imagen = image.resize((200, 200))

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("estilos.css")

def scrape_website(url):
    # Obtener el contenido HTML de la página
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrar todos los elementos con la clase 'box-text'
    items = soup.find_all(class_='box-text')

    # Dividir la pantalla en dos columnas
    col1, col2 = st.columns(2)

    # Mostrar los datos de cada producto en las columnas
    for idx, item in enumerate(items, start=1):
        category = item.find(class_='category').text.strip()
        product_name = item.find(class_='product-title').text.strip()
        price_imported = float(item.find(class_='price').text.strip().replace('$', '').replace(',', ''))

        # Calcular el precio final con un aumento del 40%
        price_final = price_imported * 1.4

        # Distribuir los productos en las columnas de forma intercalada
        if idx % 2 == 0:
            with col2:
                st.markdown(
                    f'<div class="product-box">'
                    f'<div style="font-size: larger; font-weight: bold;">Producto:</div>'
                    f'<div style="margin-left: 20px;">{product_name}</div>'
                    f'<div style="font-size: larger; font-weight: bold;">Precio:</div>'
                    f'<div style="margin-left: 20px;">${price_final:.2f}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            with col1:
                st.markdown(
                    f'<div class="product-box">'
                    f'<div style="font-size: larger; font-weight: bold;">Producto:</div>'
                    f'<div style="margin-left: 20px;">{product_name}</div>'
                    f'<div style="font-size: larger; font-weight: bold;">Precio:</div>'
                    f'<div style="margin-left: 20px;">${price_final:.2f}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

# Definir las URLs
urls = {
    'Accesorios': 'https://dazimportadora.com.ar/categoria-producto/accesorios/',
    'Audio y Video': 'https://dazimportadora.com.ar/categoria-producto/audio-y-video/'
}

st.title("Aicito- STORE")
st.title("25 De Mayo 1360")
st.sidebar.image(nueva_imagen)
# Crear los tabs
selected_tab = st.sidebar.radio("Selecciona una categoría:", list(urls.keys()))
listita = st
# Obtener la URL seleccionada
selected_url = urls[selected_tab]

# Scraping y mostrar resultados
scrape_website(selected_url)
