import pdfplumber
import sys
import os

def pdfs_dir():
    directorio = "C:/Users/Ronald/Downloads/Pruebas"
    return directorio

def lista_pdfs(pdfs):
    if not os.path.exists(pdfs):
        print("El directorio no existe.")
        return []
    archivos_pdf = [f for f in os.listdir(pdfs) if f.endswith(".pdf")]
    if not archivos_pdf:
        print("No se encontraron PDFs en la carpeta.")
    return archivos_pdf

# Función para seleccionar los pdfs encontrados
def seleccion_pdf(pdfs):
    print("Estos fueron los PDFs encontrados, ingresa el número del PDF seleccionado")
    for i, pdf in enumerate(pdfs, start=1):
        print(f"{i}. {pdf}")

    pdf = True
    errores = 0

    while pdf:
        try:
            seleccionado = int(input("Elige el PDF que quieras convertir:")) - 1 
            if 0 <= seleccionado < len(pdfs):
                return pdfs[seleccionado]
            else:
                errores += 1
                print("No se pudo encontrar el número de ese PDF.")
        except (ValueError, IndexError):
            errores += 1
            print("No se pudo encontrar el número de ese PDF.")

        if errores == 3: 
            salir_del_programa() 

def salir_del_programa():
    respuesta = input("¿Quieres salir del programa? (Si/No):").strip().lower()
    if respuesta == "si":
        print('El programa se detuvo')
        sys.exit()
    elif respuesta == "no":
        errores = 0
        seleccion_pdf(lista_pdfs(pdfs_dir())) 
    else:
        print("La respuesta que diste es inválida, responde solamente con un Si o un No ")
        return salir_del_programa()

def group_words_into_paragraphs(words):
    paragraphs = []
    current_paragraph = []
    last_y0 = None
    last_y1 = None

    for word in words:
        if 'text' in word:
            if word['text'] == '.':
                current_paragraph.append(word)
                paragraphs.append(" ".join([w['text'] for w in current_paragraph]) + "\n")
                current_paragraph = []
                last_y0 = word.get('y0', None)
                last_y1 = word.get('y1', None)
            else:
                if last_y0 is not None and last_y1 is not None:
                    if word.get('y0', None) == last_y0 and word.get('y1', None) == last_y1:
                        current_paragraph.append(word)
                    else:
                        if current_paragraph:
                            paragraphs.append(" ".join([w['text'] for w in current_paragraph]))
                            current_paragraph = []
                        current_paragraph.append(word)
                        last_y0 = word.get('y0', None)
                        last_y1 = word.get('y1', None)
                else:
                    current_paragraph.append(word)
                    last_y0 = word.get('y0', None)
                    last_y1 = word.get('y1', None)

    if current_paragraph:
        paragraphs.append(" ".join([w['text'] for w in current_paragraph]))

    return paragraphs

def extract_and_group_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            print(f"Página {page_num + 1}")

            words = page.extract_words()
            paragraphs = group_words_into_paragraphs(words)

            for paragraph in paragraphs:
                print(paragraph)
                print("\n")  # Línea en blanco para separar párrafos

directorio_pdfs = pdfs_dir()
pdfs_encontrados = lista_pdfs(directorio_pdfs)

if pdfs_encontrados:
    pdf_seleccionado = seleccion_pdf(pdfs_encontrados)
    pdf_path = os.path.join(directorio_pdfs, pdf_seleccionado)
    extract_and_group_text_from_pdf(pdf_path)
    salir_del_programa()
else:
    print("No se encontró ningún archivo PDF en la carpeta especificada.")
