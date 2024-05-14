import os

def save_uploaded_image(uploaded_file, product_name):
    # Verificar si la carpeta uploads existe, si no, crearla
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    
    # Guardar la imagen en la carpeta uploads con el nombre del producto
    file_path = os.path.join("uploads", f"{product_name}.png")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    st.success(f"Imagen guardada correctamente como {product_name}.png")