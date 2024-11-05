import sys
import os 

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
        if errores == 3: 
            salir_del_programa("") 


def salir_del_programa(respuesta):
    respuesta = input("Quieres salir del programa? (Si/No):").strip().lower()
    match respuesta:
        case "si":
            print('El programa se detuvo')
            sys.exit()
        case "no":
            errores = 0
            seleccion_pdf(lista_pdfs(pdfs_dir()))
        case _:
            print("La respuesta que diste es invalida, responde solamente con un Si o  un No ")
            salir_del_programa(respuesta)

seleccion_pdf(lista_pdfs(pdfs_dir()))