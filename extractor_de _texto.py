import pdfplumber
def pdfs_dir():
    directorio = "C:/Users/Ronald/Downloads/Universidad_pdf/Ing de software M22T5.pdf"
    return directorio


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

            print("Columna Izquierda:")
            for paragraph in left_paragraphs:
                print(paragraph)
                print("\n")

            print("Columna Derecha:")
            for paragraph in right_paragraphs:
                print(paragraph)
                print("\n")

# Ruta al archivo PDF
pdf_path = pdfs_dir()
extract_and_group_text_from_pdf(pdf_path)

