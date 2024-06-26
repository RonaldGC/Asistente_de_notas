import fitz  
import pdfplumber
import sys
import os


#Carpeta donde estan los archivos 
def pdfs_dir():
    directorio = "C:/Users/Ronald/Downloads/Pruebas"
    return directorio

#Crea lista de los archivos existentes 
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

#Funcion para salir del programa
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

# Abre el documento PDF mitz
def inspect_pdf_structure(pdf_path):
    
    document = fitz.open(pdf_path)

    # Itera a través de todas las páginas del documento
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        print(f"Página {page_num + 1}")
        
        # Obtiene los bloques de texto (cada bloque es una unidad de texto continuo)
        blocks = page.get_text("blocks")
        for block in blocks:
            print(f"Bloque de texto: {block}")
        
        # Obtiene los detalles de las imágenes
        images = page.get_images(full=True)
        for img in images:
            print(f"Imagen: {img}")
        
        # Obtiene los enlaces (si hay)
        links = page.get_links()
        for link in links:
            print(f"Enlace: {link}")

        print("\n" + "="*80 + "\n")
    
    # Cierra el documento
    document.close()

    # Abre el documento PDF con pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        # Itera a través de todas las páginas del documento
        for page_num, page in enumerate(pdf.pages):
            print(f"Página {page_num + 1}")
            
            # Obtiene los objetos de la página (texto, líneas, rectángulos, etc.)
            objects = page.objects
            for obj_type, objs in objects.items():
                print(f"Tipo de objeto: {obj_type}")
                for obj in objs:
                    print(f"Objeto: {obj}")
            
            # Obtiene las palabras con su posición
            words = page.extract_words()
            for word in words:
                print(f"Palabra: {word}")
            
            print("\n" + "="*80 + "\n")


directorio_pdfs = pdfs_dir()
pdfs_encontrados = lista_pdfs(directorio_pdfs)

if pdfs_encontrados:
    pdf_seleccionado = seleccion_pdf(pdfs_encontrados)
    pdf_path = os.path.join(directorio_pdfs, pdf_seleccionado)
    inspect_pdf_structure(pdf_path)
    salir_del_programa()
else:
    print("No se encontro ningun archivo")

