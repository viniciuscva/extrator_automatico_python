from ocr import perform_various_ocr_methods

#REALIZAR OCR NOS CAMPOS MATRICULA
directory = 'campos/matricula'
output_directory_for_tesseract = 'ocr/matricula/tesseract'
output_directory_for_vision_dtext = 'ocr/matricula/vision_text_detection'
output_directory_for_vision_dtext_plus_sorting = 'ocr/matricula/vision_text_detection_plus_sorting'
output_directory_for_vision_ddocument = 'ocr/matricula/vision_document_detection'
output_directory_for_vision_ddocument_plus_sorting = 'ocr/matricula/vision_document_detection_plus_sorting'
perform_various_ocr_methods(directory,
                            output_directory_for_tesseract,
                            output_directory_for_vision_dtext,
                            output_directory_for_vision_dtext_plus_sorting,
                            output_directory_for_vision_ddocument,
                            output_directory_for_vision_ddocument_plus_sorting)
#TODOS OS RESULTADOS DOS OCR 'S FICARAM NA PASTA OCR/MATRICULA


#REALIZAR OCR NOS CAMPOS NOME
directory = 'campos/nome'
output_directory_for_tesseract = 'ocr/nome/tesseract'
output_directory_for_vision_dtext = 'ocr/nome/vision_text_detection'
output_directory_for_vision_dtext_plus_sorting = 'ocr/nome/vision_text_detection_plus_sorting'
output_directory_for_vision_ddocument = 'ocr/nome/vision_document_detection'
output_directory_for_vision_ddocument_plus_sorting = 'ocr/nome/vision_document_detection_plus_sorting'
perform_various_ocr_methods(directory,
                            output_directory_for_tesseract,
                            output_directory_for_vision_dtext,
                            output_directory_for_vision_dtext_plus_sorting,
                            output_directory_for_vision_ddocument,
                            output_directory_for_vision_ddocument_plus_sorting)
#TODOS OS RESULTADOS DOS OCR 'S FICARAM NA PASTA OCR/NOME