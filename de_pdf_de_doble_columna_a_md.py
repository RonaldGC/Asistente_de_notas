import os
import sys
import pdfplumber 

#Define la ubicacion de la carpeta
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

#Función para seleccionar los pdfs encontrados
def seleccion_pdf(pdfs):
    print("Estos fueron los PDFs encontrados, ingresa el numero del pfd seleccionado")
    for i, pdf in enumerate (pdfs, start=1):
        print(f"{i}. {pdf}")

    pdf = True
    errores = 0

    while pdf:
        try:
            seleccionado = int(input("Elige el PDF que quieras convertir:"))- 1 
            if 0 <= seleccionado < len(pdfs):
                return pdfs[seleccionado]
            else:
                errores += 1
                print("No se pudo encontrar el número de ese pdf.")
                salir_del_programa("")
        except (ValueError, IndexError):
            errores += 1
        print("No se pudo encontrar el número de ese pdf.")
        salir_del_programa("")
        if errores == 2: 
            salir_del_programa("") 

def salir_del_programa(respuesta):
    respuesta = input("Quieres salir del programa? (Si/No):").strip().lower()
    match respuesta:
        case "si":
            print('El programa se detuvo')
            sys.exit()
        case "no":
            errores = 0
            pdf_seleccionado = seleccion_pdf(pdfs_encontrados)
            ruta_pdf = os.path.join(directorio_pdfs, pdf_seleccionado)

            # Procesar el archivo PDF y guardar como Markdown
            nombre_md = os.path.basename(ruta_pdf).replace('.pdf', '.md')
            ruta_md = os.path.join(directorio_pdfs, nombre_md)
            text_a_md(ruta_pdf, ruta_md)
            print("El pdf ha sido convertido")
            salir_del_programa("")  
        case _:
            print("La respuesta que diste es invalida, responde solamente con un Si o  un No ")
            salir_del_programa(respuesta)

def preguntar_paginas_a_ignorar(total_paginas):
    paginas_a_ignorar = []
    print(f"El documento tiene {total_paginas} páginas.")
    while True:
        respuesta = input("¿Desea ignorar alguna página? (Si/No): ").strip().lower()
        if respuesta == 'no':
            break
        elif respuesta == 'si':
            paginas = input(f"Ingrese los números de página a ignorar separados por espacios (1-{total_paginas}): ").strip()
            paginas_lista = paginas.split()
            for num_pagina in paginas_lista:
                if num_pagina.isdigit():
                    num_pagina = int(num_pagina)
                    if 1 <= num_pagina <= total_paginas:
                        paginas_a_ignorar.append(num_pagina)
                    else:
                        print(f"Número de página inválido: {num_pagina}. Por favor ingrese un número entre 1 y {total_paginas}.")
                else:
                    print(f"Entrada inválida: {num_pagina}. Por favor ingrese números válidos.")
        else:
            print("Respuesta inválida. Por favor ingrese 's' para sí o 'n' para no.")
    return paginas_a_ignorar


def palabras_dentro_del_parrafo(palabras, umbral_de_linea=3, umbral_de_altura=18):
    parrafo = []
    parrafo_actual = []
    ultima_abajo = None
    primera_palabra_modificada = False

    for palabra in palabras:
        if ultima_abajo is not None and (palabra['top'] - ultima_abajo) > umbral_de_linea:
            parrafo.append(" ".join([w['text'] for w in parrafo_actual]))
            parrafo_actual = []
            primera_palabra_modificada = False  # Resetear la bandera para el siguiente párrafo

        if '•' in palabra['text']:
            palabra['text'] = palabra['text'].replace('•', '- ')

        # Modificar la palabra si su altura es mayor al umbral_de_altura y aún no se ha modificado ninguna palabra en este párrafo
        if palabra['height'] >= umbral_de_altura:
            if not primera_palabra_modificada:
                palabra['text'] = "## " + palabra['text'].capitalize()
                primera_palabra_modificada = True  # Marcar que ya se ha modificado la primera palabra
            else:
                palabra['text'] = palabra['text'].lower()

        parrafo_actual.append(palabra)
        ultima_abajo = palabra['bottom']

    if parrafo_actual:
        parrafo.append(" ".join([w['text'] for w in parrafo_actual]))

    return parrafo

def dividir_en_columnas(palabras, umbral_de_columna):
    columna_izquierda = []
    columna_derecha = []

    for palabra in palabras:
        if palabra['x1'] < umbral_de_columna:
            columna_izquierda.append(palabra)
        else:
            columna_derecha.append(palabra)

    return columna_izquierda, columna_derecha

def extractor_y_agrupamiento_del_text(ruta_pdf, umbral_de_columna=300):
    resultado = {}
    with pdfplumber.open(ruta_pdf) as pdf:
        total_paginas = len(pdf.pages)
        paginas_a_ignorar = preguntar_paginas_a_ignorar(total_paginas)
        
        for numero_de_pag, pagina in enumerate(pdf.pages):
            if (numero_de_pag + 1) in paginas_a_ignorar:
                print(f"Ignorando la página {numero_de_pag + 1}")
                continue

            palabras = pagina.extract_words()

            # Dividir palabras en dos columnas
            columna_izquierda, columna_derecha = dividir_en_columnas(palabras, umbral_de_columna)

            # Agrupar palabras en párrafos dentro de cada columna
            parrafos_de_la_izquierda = palabras_dentro_del_parrafo(columna_izquierda)
            parrafos_de_la_derecha = palabras_dentro_del_parrafo(columna_derecha)

            resultado[f"Página {numero_de_pag + 1}"] = {
                "columna_izquierda": parrafos_de_la_izquierda,
                "columna_derecha": parrafos_de_la_derecha
            }
    return resultado

def text_a_md(ruta_pdf, ruta_md):
    text = extractor_y_agrupamiento_del_text(ruta_pdf)
    with open(ruta_md, 'w', encoding='utf-8') as f:
        for pagina, columnas in text.items():
            for parrafo in columnas["columna_izquierda"]:
                f.write(parrafo + "\n\n")
            for parrafo in columnas["columna_derecha"]:
                f.write(parrafo + "\n\n")
            


directorio_pdfs = pdfs_dir()
pdfs_encontrados = lista_pdfs(directorio_pdfs)

if pdfs_encontrados:
    pdf_seleccionado = seleccion_pdf(pdfs_encontrados)
    ruta_pdf = os.path.join(directorio_pdfs, pdf_seleccionado)

    # Procesar el archivo PDF y guardar como Markdown
    nombre_md = os.path.basename(ruta_pdf).replace('.pdf', '.md')
    ruta_md = os.path.join(directorio_pdfs, nombre_md)
    text_a_md(ruta_pdf, ruta_md)
    print("El pdf ha sido convertido")
    salir_del_programa("")  
else:
    print("No se encontraron archivos PDF para procesar revisa bien los archivos en la carpeta")
