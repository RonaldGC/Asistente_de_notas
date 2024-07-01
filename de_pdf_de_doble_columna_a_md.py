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
        except (ValueError, IndexError):
            errores += 1
        print("No se pudo encontrar el número de ese pdf.")

        if errores == 3: 
            salir_del_programa() 

def salir_del_programa():
    respuesta = input("Quieres salir del programa? (Si/No):").strip().lower()
    if respuesta =="si":
        print('El programa se detuvo')
        sys.exit()
    elif respuesta == "no":
       errores = 0
       seleccion_pdf(lista_pdfs(pdfs_dir())) 
    else:
        print("La respuesta que diste es invalida, responde solamente con un Si o  un No ")
        return salir_del_programa()


def palabras_dentro_del_parrafo(palabras, umbral_de_linea=3):
    parrafo = []
    parrafo_actual = []
    ultima_abajo = None

    for palabra in palabras:
        if ultima_abajo is not None and (palabra['top'] - ultima_abajo) >umbral_de_linea:
            parrafo.append(" ".join([w['text'] for w in parrafo_actual]))
            parrafo_actual = []
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
        for numero_de_pag, pagina in enumerate(pdf.pages):
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
            f.write(f"# {pagina}\n\n")
            for parrafo in columnas["columna_izquierda"]:
                f.write(parrafo + "\n\n")
            for parrafo in columnas["columna_derecha"]:
                f.write(parrafo + "\n\n")
            f.write("---\n\n")


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
    salir_del_programa()  
else:
    print("No se encontraron archivos PDF para procesar revisa bien los archivos en la carpeta")
