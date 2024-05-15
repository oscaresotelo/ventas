import streamlit as st
import requests
from bs4 import BeautifulSoup
import os  # Importar el módulo os para manejar archivos y carpetas
from PIL import Image
import math  # Importar la librería math para redondear hacia arriba

st.set_page_config(
    page_title="Ventas - Aicito",
    page_icon="🧊",
    initial_sidebar_state="expanded")
st.title("25 STORE - 25 de mayo 1360")
st.header("Consultas")
whatsapp_icon = '''
<a href="https://api.whatsapp.com/send?phone=5493814644703" target="_blank">
  <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp" width="80">
</a>
'''
st.markdown(whatsapp_icon, unsafe_allow_html=True)
image = Image.open("nino.jpg")
nueva_imagen = image.resize((200, 200))

css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.5rem;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
                     .container {
                display: flex;
            }
            .logo-text {
                font-weight:700 !important;
                font-size:30px !important;
                color: black !important;
                padding-top: 50px !important;
            }
            .logo-img {
                float:right;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


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
        # Obtener el nombre del producto y reemplazar caracteres no deseados
        product_name = item.find(class_='product-title').text.strip().replace('″', '').replace('/', '')
        price_imported = float(item.find(class_='price').text.strip().replace('$', '').replace(',', ''))

        # Calcular el precio final con un aumento del 40%
        price_final = price_imported * 1.4

        # Redondear el precio final hacia arriba y ajustar la decena y la unidad a cero
        price_final = math.ceil(price_final / 100) * 100  # Redondear hacia arriba y ajustar a múltiplo de 100

        # Obtener la ruta de la imagen del producto
        image_path = os.path.join('images', f'{product_name}.png')  # Cambiar extensión a '.png'
        
        # Verificar si la imagen existe en la carpeta 'images'
        if os.path.exists(image_path):
            product_image = Image.open(image_path)
        else:
            product_image = None  # Establecer product_image como None si no hay imagen

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
                if product_image:
                    st.image(product_image, caption=f'Imagen de {product_name}', width=200)
                else:
                    st.write("No existe imagen disponible")

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
                if product_image:
                    st.image(product_image, caption=f'Imagen de {product_name}', width=200)
                else:
                    st.write("No existe imagen disponible")

# Definir las URLs

rutaaccesorios = 'https://dazimportadora.com.ar/categoria-producto/accesorios/'
rutaaudiovido = 'https://dazimportadora.com.ar/categoria-producto/audio-y-video/'
rutatecnologia =  'https://dazimportadora.com.ar/categoria-producto/tecnologia/'
tab1, tab2, tab3 = st.tabs(["Audio y Video", "Accesorios", "Tecnologia"])

with tab1:

    scrape_website(rutaaudiovido)
with tab2:

    scrape_website(rutaaccesorios)
with tab3:
   
    scrape_website('https://dazimportadora.com.ar/categoria-producto/tecnologia/')

