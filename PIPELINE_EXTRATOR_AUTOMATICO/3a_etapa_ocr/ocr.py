from ocr_with_detect_document import vision_detect_document, vision_detect_document_plus_sorting
from ocr_with_detect_text import vision_detect_text, vision_detect_text_plus_sorting
from ocr_with_tesseract import tesseract_detect_text
import os


def perform_various_ocr_methods(directory, 
                                output_directory_for_tesseract,
                                output_directory_for_vision_dtext,
                                output_directory_for_vision_dtext_plus_sorting,
                                output_directory_for_vision_ddocument,
                                output_directory_for_vision_ddocument_plus_sorting):


    for img in os.listdir(directory):
        if not img.endswith('.jpg'):
            continue
        tesseract_detect_text(f'{directory}/{img}', output_directory_for_tesseract)#OCR COM TESSERACT
        vision_detect_text(f'{directory}/{img}', output_directory_for_vision_dtext)#OCR COM VISION_TEXT_DETECTION
        vision_detect_text_plus_sorting(f'{directory}/{img}', output_directory_for_vision_dtext_plus_sorting)#OCR COM VISION_TEXT_DETECTION_PLUS_SORTING
        vision_detect_document(f'{directory}/{img}', output_directory_for_vision_ddocument)#OCR COM VISION_DOCUMENT_DETECTION
        vision_detect_document_plus_sorting(f'{directory}/{img}', output_directory_for_vision_ddocument_plus_sorting)#OCR COM VISION_DOCUMENT_DETECTION_PLUS_SORTING

