#https://github.com/googleapis/python-vision/blob/HEAD/samples/snippets/detect/detect.py

from google.cloud import vision
from functools import partial
import io
import os
import json

def detect_text(path):
    """Detects text in the file."""
    #from google.cloud import vision
    #import io
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    #print('Texts:')
    words_with_bounds = []#vai ser uma lista no formato [(bbox,palavra), (bbox,palavra)...]
    for text in texts[1:]:
        #print('\n"{}"'.format(text.description))
        #if text.description.__contains__('\n'):
        #    continue
        
        vertices = [[vertex.x, vertex.y] for vertex in text.bounding_poly.vertices]
        words_with_bounds.append( (vertices, text.description) )
        #print('bounds: {}'.format(','.join(vertices)))
    
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    full_text = texts[0].description.replace('\n','')
    return full_text, words_with_bounds#full_text é o formato como a api retorna; transcription é a forma 
                                    #criada por mim padrao: {palavra1: [[x,y],[x,y],[x,y],[x,y]], palavra2...}
    # [END vision_python_migration_text_detection]
# [END vision_text_detection]



def words_with_bounds_to_unique_string(words_with_bounds):
    y_linhas = []
    range_y_linhas = []
    for tupla in words_with_bounds:
        bounds = tupla[0]
        y = bounds[0][1]
        if any([y>=a and y<=b for (a,b) in range_y_linhas]):
            continue
        y_linhas.append(y)
        range_y_linhas.append([y-6, y+6])
    #vamos criar uma lista de vários dicionários, cada dicionário é da forma {"text":texto, "bounds": bounds}
    lista_de_textos = [{"text": texto, "bounds":bounds} for (bounds,texto) in words_with_bounds]
    def isin_range(texto, range_linha):
        #texto deve ser um dicionário da forma {"text":texto, "bounds":bounds}
        #range_linha é da forma (y_inf, y_sup)
        return texto['bounds'][0][1]>=range_linha[0] and texto['bounds'][0][1]<=range_linha[1]
    unique_string = ""
    for i,range_linha in enumerate(range_y_linhas):
        #filtrar os textos da transcrição que pertencem a este range de linha
        isin_range_partial = partial(isin_range, range_linha=range_linha)
        textos_na_linha_atual = list(filter(isin_range_partial, lista_de_textos))#contém também os bounds
        #print('Textos na linha',i,":",list(textos_na_linha_atual))
        textos_na_linha_atual.sort(key = lambda texto: texto['bounds'][0][0])
        palavras_na_linha_atual = list(map(lambda texto: texto['text'], textos_na_linha_atual))#não contém mais os bounds
        linha_atual = " ".join(palavras_na_linha_atual)
        unique_string += linha_atual
    return unique_string

def vision_detect_text_plus_sorting(path_to_img, output_directory):
    _, words_with_bounds = detect_text(path_to_img)
    nome_img = path_to_img.split('/')[-1].split('.')[0]
    with open(f'{output_directory}/{nome_img}.json', 'w') as arquivo_json:
        js = json.dumps(words_with_bounds)
        arquivo_json.write(js)
    #agora vamos criar a transcription a partir do words_with_bounds
    transcription = words_with_bounds_to_unique_string(words_with_bounds)
    with open(f'{output_directory}/{nome_img}_transcription.txt', 'w') as arquivo:
        arquivo.write(transcription)

def vision_detect_text(path_to_img, output_directory):
    full_text, _ = detect_text(path_to_img)
    nome_img = path_to_img.split('/')[-1].split('.')[0]
    with open(f'{output_directory}/{nome_img}_fulltext.txt', 'w') as arquivo:
        arquivo.write(full_text)


"""
def ocr_entire_directory(directory, output_directory):
    for img in os.listdir(directory):
        if not img.endswith('jpg'):
            continue
        full_text, json_of_texts = detect_text(f'{directory}/{img}')
        nome_arquivo = img.split('.')[0]
        with open(f'{output_directory}/{nome_arquivo}.json', 'w') as arquivo_json:
            arquivo_json.write(json_of_texts)
        with open(f'{output_directory}/{nome_arquivo}_fulltext.txt', 'w') as arquivo:
            arquivo.write(full_text)
"""

"""
def convert_all_jsons_of_words_with_bounds_in_directory_to_strings(directory):
    for words_with_bounds in os.listdir(directory):
        if not words_with_bounds.endswith('json'):
            continue
        unique_string = words_with_bounds_to_unique_string(f'{directory}/{words_with_bounds}')
        nome_arquivo = f'{words_with_bounds.split(".")[0]}_transcription.txt'
        with open(f'{directory}/{nome_arquivo}', 'w') as transcription:
            transcription.write(unique_string)
"""

