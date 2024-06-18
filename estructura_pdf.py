import fitz  # PyMuPDF
import pdfplumber

def pdfs_dir():
    directorio = "C:/Users/Ronald/Downloads/Universidad_pdf/Ing de software M22T5.pdf"
    return directorio


def inspect_pdf_structure(pdf_path):
    print("== Usando PyMuPDF ==")
    # Abre el documento PDF con PyMuPDF
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

    print("== Usando pdfplumber ==")
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

# Ruta al archivo PDF
pdf_path = pdfs_dir()
inspect_pdf_structure(pdf_path)
