import os
import re
import pdfplumber

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
            choice = int(input("Selecciona el número del PDF que quieras procesar")) - 1
            if 0 <= choice < len(pdfs):
                return pdfs[choice]
            else:
                print("Selección inválida, intenta de nuevo.")
        except ValueError:
            print("Entrada no válida. Por favor, introduce el número del pdf que quieras")

# Función para extraer texto en columnas
def extraer_texto_en_columnas(pagina, num_columnas=2):
    ancho_pagina = pagina.width
    altura_pagina = pagina.height
    columna_ancho = ancho_pagina / num_columnas
    textos_columnas = []

    for col in range(num_columnas):
        bbox = (
            columna_ancho * col,  # x0
            0,  # y0
            columna_ancho * (col + 1),  # x1
            altura_pagina  # y1
        )
        texto_columna = pagina.within_bbox(bbox).extract_text()
        if texto_columna:
            textos_columnas.append(texto_columna.strip())

    return textos_columnas

# Función para visualizar y procesar la estructura interna del PDF
def visualizar_estructura_pdf(ruta_pdf):
    with pdfplumber.open(ruta_pdf) as pdf:
        contenido_md = []
        ignore_page_numbers = {1, 2}
        ignore_until_bibliography = False

        for numero_pagina, pagina in enumerate(pdf.pages, start=1):
            if numero_pagina in ignore_page_numbers:
                continue

            textos_columnas = extraer_texto_en_columnas(pagina)
            texto_pag = "\n".join(textos_columnas)

            if "Bibliografía" in texto_pag:
                ignore_until_bibliography = True

            if ignore_until_bibliography:
                continue

            contenido_md.append(f"## Página {numero_pagina}\n")

            if texto_pag:
                # Añadir un salto de línea antes de cada [n] donde n es un número del 1 al 15
                texto_pag = re.sub(r'(?<=\s)\[(1[0-5]|[1-9])\]', r'\n[\1]', texto_pag)
                
                lineas = texto_pag.split('\n')
                parrafos = []
                parrafo_actual = []

                for linea in lineas:
                    linea_limpia = linea.strip()
                    if linea_limpia:
                        parrafo_actual.append(linea_limpia)
                    else:
                        if parrafo_actual:
                            parrafos.append(" ".join(parrafo_actual))
                            parrafo_actual = []

                if parrafo_actual:
                    parrafos.append(" ".join(parrafo_actual))

                for parrafo in parrafos:
                    # Añadir un salto de línea después de cada punto
                    parrafo = parrafo.replace('. ', '.\n')
                    contenido_md.append(parrafo)
                    contenido_md.append("\n")
            else:
                contenido_md.append("No se pudo extraer texto de esta página.")
            contenido_md.append("\n")

    return "\n".join(contenido_md)

# Función para guardar el contenido en un archivo .md
def guardar_como_md(contenido, ruta_md):
    with open(ruta_md, 'w', encoding='utf-8') as archivo_md:
        archivo_md.write(contenido)

# Obtener el directorio y los PDFs
directorio_pdfs = pdfs_dir()
pdfs_encontrados = lista_pdfs(directorio_pdfs)

# Seleccionar un PDF
pdf_seleccionado = seleccion_pdf(pdfs_encontrados)
ruta_pdf = os.path.join(directorio_pdfs, pdf_seleccionado)

# Visualizar la estructura interna del PDF y obtener el contenido en formato Markdown
contenido_md = visualizar_estructura_pdf(ruta_pdf)

# Guardar el contenido en un archivo .md
ruta_md = os.path.splitext(ruta_pdf)[0] + ".md"
guardar_como_md(contenido_md, ruta_md)

print(f"El contenido del PDF se ha guardado en {ruta_md}")
