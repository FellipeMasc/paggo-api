import pytesseract
from pdf2image import convert_from_bytes
import cv2
import pandas as pd
import numpy as np
import os

def extract_text_from_file(file_bytes : bytes, file_type_pdf : bool) -> str:
    image = None
    if file_type_pdf:
        page = convert_from_bytes(file_bytes, 200)[0]
        image = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2GRAY)
    else:
        np_arr = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(image)

    return text