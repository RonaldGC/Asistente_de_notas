import pdfplumber
import sys
import os

def pdfs_dir():
    directorio = "C:/Users/Ronald/Downloads/Pruebas "
    return directorio

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

def group_words_into_paragraphs(words, line_threshold=3):
    paragraphs = []
    current_paragraph = []
    last_bottom = None

    for word in words:
        if last_bottom is not None and (word['top'] - last_bottom) > line_threshold:
            paragraphs.append(" ".join([w['text'] for w in current_paragraph]))
            current_paragraph = []
        current_paragraph.append(word)
        last_bottom = word['bottom']

    if current_paragraph:
        paragraphs.append(" ".join([w['text'] for w in current_paragraph]))

    return paragraphs

def split_into_columns(words, column_threshold):
    left_column = []
    right_column = []

    for word in words:
        if word['x1'] < column_threshold:
            left_column.append(word)
        else:
            right_column.append(word)

    return left_column, right_column

def extract_and_group_text_from_pdf(pdf_path, column_threshold=300):
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            print(f"Página {page_num + 1}")

            words = page.extract_words()

            # Dividir palabras en dos columnas
            left_column, right_column = split_into_columns(words, column_threshold)

            # Agrupar palabras en párrafos dentro de cada columna
            left_paragraphs = group_words_into_paragraphs(left_column)
            right_paragraphs = group_words_into_paragraphs(right_column)

            for paragraph in left_paragraphs:
                print(paragraph)
                print("\n")

            for paragraph in right_paragraphs:
                print(paragraph)
                print("\n")


directorio_pdfs = pdfs_dir()
pdfs_encontrados = lista_pdfs(directorio_pdfs)

if pdfs_encontrados:
    pdf_seleccionado = seleccion_pdf(pdfs_encontrados)
    pdf_path = os.path.join(directorio_pdfs, pdf_seleccionado)
    extract_and_group_text_from_pdf(pdf_path)
    salir_del_programa()
else:
    print("No se encontro ningun archivo")
