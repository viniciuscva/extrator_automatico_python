try:
    from PIL import Image
except ImportError:
    import Image
    
import pytesseract
import os


def detect_text(path_to_img):
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    #pytesseract.image_to_string(img, lang="por")
    # Simple image to string
    #print(pytesseract.image_to_string(Image.open('test.png'), lang="por"))
    transcription = pytesseract.image_to_string(Image.open(path_to_img), lang='por')
    return transcription


def tesseract_detect_text(path_to_img, output_directory):
    transcription = detect_text(path_to_img)
    nome_img = path_to_img.split('/')[-1].split('.')[0]
    with open(f'{output_directory}/{nome_img}_transcription.txt', 'w') as arquivo:
        arquivo.write(transcription)
