import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image

# Función para cargar imágenes y asociarlas a productos
def upload_images(product_name):
    uploaded_files = st.file_uploader(f"Subir imagen para {product_name}", accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.image(uploaded_file, caption=f"Imagen asociada a {product_name}", use_column_width=True)
            # Guardar la imagen con el nombre del producto en la carpeta 'images'
            save_image(uploaded_file, product_name)

def save_image(image_file, product_name):
    # Crear la carpeta 'images' si no existe
    if not os.path.exists('images'):
        os.makedirs('images')
    # Obtener la extensión del archivo
    ext = image_file.name.split('.')[-1]
    # Guardar la imagen con el nombre del producto en la carpeta 'images'
    image_path = os.path.join('images', f'{product_name}.{ext}')
    with open(image_path, 'wb') as f:
        f.write(image_file.read())  # Cambiado de getbuffer() a read()
    st.success(f"Imagen guardada como '{product_name}.{ext}'")

image = Image.open("nino.jpg")
nueva_imagen = image.resize((200, 200))
st.set_page_config(
    page_title="Ventas - Aicito",
    page_icon="🧊",
    initial_sidebar_state="expanded")

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

def clean_product_name(product_name):
    # Eliminar el carácter " (comillas dobles), ″ (comillas dobles prime), y / (slash)
    # si están presentes en el nombre del producto, pero no eliminarlos si están de forma aislada
    product_words = product_name.split()
    cleaned_words = []
    for word in product_words:
        if ('"' in word or '″' in word or '/' in word) and len(word) > 1:
            word = word.replace('"', '').replace('″', '').replace('/', '')
        cleaned_words.append(word)
    return ' '.join(cleaned_words)

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

        # Limpiar el nombre del producto si contiene los caracteres " (comillas dobles), ″ (comillas dobles prime), o / (slash)
        product_name = clean_product_name(product_name)

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
                upload_images(product_name)
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
                upload_images(product_name)

# Definir las URLs
urls = {
    'Accesorios': 'https://dazimportadora.com.ar/categoria-producto/accesorios/',
    'Audio y Video': 'https://dazimportadora.com.ar/categoria-producto/audio-y-video/'
}

st.title("25 STORE- 25 DE MAYO 1360")

st.sidebar.image(nueva_imagen)
# Crear los tabs
selected_tab = st.sidebar.radio("Selecciona una categoría:", list(urls.keys()))

# Obtener la URL seleccionada
selected_url = urls[selected_tab]

# Scraping y mostrar resultados
scrape_website(selected_url)
