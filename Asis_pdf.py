import os
import pdfplumber
import re

# Función para el directorio de los pdf
def pdfs_dir():
    directorio = "C:/Users/Ronald/Downloads/Universidad_pdf"
    return directorio

# Función para crear lista de los pdf
def lista_pdfs(pdfs):
    if not os.path.exists(pdfs):
        print("El directorio no existe.")
        return []
    archivos_pdf = [f for f in os.listdir(pdfs) if f.endswith(".pdf")]
    if not archivos_pdf:
        print("No se encontraron PDFs en la carpeta.")
    return archivos_pdf

# Función para que el usuario pueda seleccionar un pdf
def seleccion_pdf(pdfs):
    print("PDFs encontrados:")
    for i, pdf in enumerate(pdfs, start=1):
        print(f"{i}. {pdf}")

    while True:
        try:
            choice = int(input("Selecciona el número del PDF que quieras procesar: ")) - 1
            if 0 <= choice < len(pdfs):
                return pdfs[choice]
            else:
                print("Selección inválida, intenta de nuevo.")
        except ValueError:
            print("Entrada no válida. Por favor, introduce el número del pdf que quieras")

# Función para detectar bloques de texto del PDF
def detectar_bloques_texto(ruta_pdf, distancia_maxima=20):
    bloques_texto = []
    with pdfplumber.open(ruta_pdf) as pdf:
        for page in pdf.pages:
            # Detecta las columnas usando heurísticas simples 
            left_column = page.within_bbox((0, 0, page.width / 2, page.height))
            right_column = page.within_bbox((page.width / 2, 0, page.width, page.height))

            # Extrae texto de ambas columnas
            left_text = left_column.extract_text(x_tolerance=distancia_maxima) if left_column else ""
            right_text = right_column.extract_text(x_tolerance=distancia_maxima) if right_column else ""

            # Combina el texto de ambas columnas manteniendo el orden
            if left_text and right_text:
                lineas_texto = left_text.split("\n") + right_text.split("\n")
            else:
                lineas_texto = (left_text or right_text).split("\n")

            for linea in lineas_texto:
                bloques_texto.append(linea.strip())

    return bloques_texto

# Función mejorada para eliminar saltos de línea dentro de párrafos
def eliminar_saltos_de_linea(bloques_texto):
    texto_unido = " ".join(bloques_texto)
    return re.sub(r'\s*\n\s*', ' ', texto_unido)

# Función para insertar saltos de página después de cada punto
def insertar_saltos_de_pagina(texto):
    return texto.replace('. ', '.\n\n')

# Función para convertir texto a formato Markdown
def texto_a_md(ruta_pdf, ruta_md):
    bloques_texto = detectar_bloques_texto(ruta_pdf)
    texto_sin_saltos = eliminar_saltos_de_linea(bloques_texto)
    texto_con_saltos = insertar_saltos_de_pagina(texto_sin_saltos)

    with open(ruta_md, 'w', encoding='utf-8') as f:
        f.write(texto_con_saltos)

# Ruta del archivo PDF seleccionado
directorio_pdfs = pdfs_dir()
pdfs_encontrados = lista_pdfs(directorio_pdfs)


if pdfs_encontrados:
    pdf_seleccionado = seleccion_pdf(pdfs_encontrados)
    ruta_pdf = os.path.join(directorio_pdfs, pdf_seleccionado)

    # Procesar el archivo PDF y guardar como Markdown
    nombre_md = os.path.basename(ruta_pdf).replace('.pdf', '.md')
    ruta_md = os.path.join(directorio_pdfs, nombre_md)
    texto_a_md(ruta_pdf, ruta_md)

    print(f"El PDF ha sido convertido y guardado como {ruta_md}")
else:
    print("No se encontraron PDFs para procesar.")

