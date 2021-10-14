from google.cloud import vision
import io
import json

def detect_document(path):
    """Detects document features in an image."""
    
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    full_text = ""
    words_with_bounds = []#na forma [(bbox,palavra), (bbox,palavra),...]
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            #print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                #print('Paragraph confidence: {}'.format(
                    #paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    bbox = []
                    for vertice in word.bounding_box.vertices:
                        bbox.append([vertice.x, vertice.y])
                    words_with_bounds.append(  (bbox, word_text)  )
                    full_text += word_text
                    #print('Word text: {} (confidence: {})'.format(
                    #    word_text, word.confidence))

                    #for symbol in word.symbols:
                     #   print('\tSymbol: {} (confidence: {})'.format(
                      #      symbol.text, symbol.confidence))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return full_text, words_with_bounds

def words_with_bounds_to_unique_string(words_with_bounds):
    ys_das_linhas = []
    range_y_linhas = []

    for tupla in words_with_bounds:#procura nas chaves do dict
        bound = tupla[0]
        y = bound[0][1]
        if any([y>=a and y<=b for (a,b) in range_y_linhas]):
            continue
        ys_das_linhas.append(y)
        range_y_linhas.append([y-6, y+6])
        
    #vamos criar uma lista de vários dicionários, cada dicionário é da forma {"text":texto, "bounds": bounds}
    lista_de_textos = [{"text": word, "bounds":bound} for (bound, word) in words_with_bounds]

    def isin_range(texto, range_linha):
        #texto deve ser um dicionário da forma {"text":texto, "bounds":bounds}
        #range_linha é da forma (y_inf, y_sup)
        return texto['bounds'][0][1]>=range_linha[0] and texto['bounds'][0][1]<=range_linha[1]

    unique_string = ""
    from functools import partial

    for i,range_linha in enumerate(range_y_linhas):
        #filtrar os textos da transcrição que pertencem a este range de linha
        isin_range_partial = partial(isin_range, range_linha=range_linha)
        textos_na_linha_atual = list(filter(isin_range_partial, lista_de_textos))#contém também os bounds
        #print('Textos na linha',i,":",list(textos_na_linha_atual))
        textos_na_linha_atual.sort(key = lambda texto: texto['bounds'][0][0])
        palavras_na_linha_atual = list(map(lambda texto: texto['text'], textos_na_linha_atual))#não contém mais os bounds
        linha_atual = " ".join(palavras_na_linha_atual)
        unique_string += linha_atual
    #unique_string = unique_string.replace('NOME','')
    #unique_string = unique_string.replace(' ','')
    return unique_string

def vision_detect_document_plus_sorting(path_to_img, output_directory):
    _, words_with_bounds = detect_document(path_to_img)
    nome_img = path_to_img.split('/')[-1].split('.')[0]
    with open(f'{output_directory}/{nome_img}.json', 'w') as arquivo_json:
        js = json.dumps(words_with_bounds)
        arquivo_json.write(js)
    #agora vamos criar a transcription a partir do words_with_bounds
    transcription = words_with_bounds_to_unique_string(words_with_bounds)
    with open(f'{output_directory}/{nome_img}_transcription.txt', 'w') as arquivo:
        arquivo.write(transcription)

def vision_detect_document(path_to_img, output_directory):
    full_text, _ = detect_document(path_to_img)
    nome_img = path_to_img.split('/')[-1].split('.')[0]
    with open(f'{output_directory}/{nome_img}_fulltext.txt', 'w') as arquivo:
        arquivo.write(full_text)